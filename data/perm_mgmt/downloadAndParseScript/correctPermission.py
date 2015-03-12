__author__ = 'zz'
# coding=utf-8
import os

import MySQLdb

from androguard.core.bytecodes import apk, dvm
from androguard.core import androconf
from androguard.core.analysis import analysis


class MySQL():
    # def open(self, host, user, passwd, db, cursorclass):
    def open(self, host, user, passwd, db):
        try:
            # self.con = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, cursorclass=cursorclass)
            self.con = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
            self.con.set_character_set('utf8')
            self.cur = self.con.cursor()
        except Exception:
            print("Cannot connect to db")
            self.close()

    # def __init__(self, host, user, passwd, db, cursorclass):
    def __init__(self, host, user, passwd, db):
        self.open(host, user, passwd, db)

    def close(self):
        if self.cur is not None:
            self.cur.close()
        if self.con is not None:
            self.con.close()


def parseApk(filename, permissions):
    if filename is not None:
        ret_type = androconf.is_android(filename)
        vm = None
        a = None
        md5 = None
        if ret_type == 'APK':
            a = apk.APK(filename)
            md5 = a.md5

        outs = {}
        for and_permission in a.get_permissions():
            and_permission = and_permission.rsplit('.', 1)[-1]
            if and_permission in permissions:
                if isinstance(permissions[and_permission], basestring):
                    outs.setdefault(permissions[and_permission])
                elif isinstance(permissions[and_permission], list):
                    for and_perm in permissions[and_permission]:
                        outs.setdefault(and_perm)
        if a.is_valid_APK():
            vm = dvm.DalvikVMFormat(a.get_dex())
        vmx = analysis.VMAnalysis(vm)
        for str in vm.get_strings():
            if "IMAGE_CAPTURE" in str:
                outs.setdefault("PERM_ID_RECORDER")

        for and_permission in vmx.get_permissions([]):
            if and_permission in permissions:
                if isinstance(permissions[and_permission], basestring):
                    outs.setdefault(permissions[and_permission])
                elif isinstance(permissions[and_permission], list):
                    for and_perm in permissions[and_permission]:
                        outs.setdefault(and_perm)

        return outs.keys()


if __name__ == '__main__':
    permissions = {}
    with open("PERMISSIONS") as perm_file:
        for line in perm_file:
            line_info = line.strip('\r\n').split(',')
            lbe_permission = line_info[0]
            and_permission = line_info[1]
            if and_permission in permissions:
                perm_tmp = []
                perm_tmp.append(permissions[and_permission])
                perm_tmp.append(lbe_permission)
                permissions[and_permission] = perm_tmp
            else:
                permissions[and_permission] = lbe_permission
    perm_dict = {"PERM_ID_SENDSMS":"perm_sendsms_suggest",
                   "PERM_ID_CALLPHONE":"perm_callphone_suggest",
                   "PERM_ID_SMSDB":"perm_smsdb_suggest",
                   "PERM_ID_CONTACT":"perm_contact_suggest",
                   "PERM_ID_CALLLOG":"perm_calllog_suggest",
                   "PERM_ID_LOCATION":"perm_location_suggest",
                   "PERM_ID_PHONEINFO":"perm_phoneinfo_suggest",
                   "PERM_ID_NETDEFAULT":"perm_netdefault_suggest",
                   "PERM_ID_NETWIFI":"perm_netwifi_suggest",
                   "PERM_ID_ROOT":"perm_root_suggest",
                   "PERM_ID_CALLSTATE":"perm_callstate_suggest",
                   "PERM_ID_CALLMONITOR":"perm_callmonitor_suggest",
                   "PERM_ID_RECORDER":"perm_recorder_suggest",
                   "PERM_ID_SETTINGS":"perm_settings_suggest",
                   "PERM_ID_AUDIO_RECORDER":"perm_audiorecorder_suggest",
                   "PERM_ID_MMSDB":"perm_mmsdb_suggest",
                   "PERM_ID_SENDMMS":"perm_sendmms_suggest",
                   "PERM_ID_MOBILE_CONNECTIVITY":"perm_mobileconnectivity_suggest",
                   "PERM_ID_WIFI_CONNECTIVITY":"perm_wificonnectivity_suggest",
                   "PERM_ID_BT_CONNECTIVITY":"perm_btconnectivity_suggest"}
    """
    db_host = "localhost"
    db_user = "zz"
    db_passwd = "123qwe"
    db_name = "zzdev"
    """
    db_host = "192.168.1.15"
    db_user = "root"
    db_passwd = "!LBE_Privacy#"
    db_name = "permission"
    my = MySQL(db_host, db_user, db_passwd, db_name)

    # for fn in os.listdir('download'):
    #     for file in os.listdir(os.path.join('download', fn)):
    #         file_path = os.path.join('download', fn, file)
    #         file_prop = file.split("_")
    #         print file_path, fn, file_prop[0], file_prop[1], file_prop[2].split(".")[0]

    dirpath = "download"
    folder_entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    folder_entries = ((os.stat(folder_path), folder_path) for folder_path in folder_entries)
    folder_entries = ((folder_stat.st_ctime, folder_path) for folder_stat, folder_path in folder_entries)
    for cdate, folder in sorted(folder_entries):
        file_entries = (os.path.join(folder, fn) for fn in os.listdir(folder))
        file_entries = ((os.stat(file_path), file_path) for file_path in file_entries)
        file_entries = ((file_stat.st_ctime, file_path) for file_stat, file_path in file_entries)
        for cdate, file in sorted(file_entries):
            file_category = os.path.basename(folder)
            file_prop = os.path.basename(file).split("_")
            parse_result = ""
            perm_number = 0
            try:
                parse_result = parseApk(file, permissions)
            except Exception as e:
                print(str(e))
                print("Analyze error, process next one")

            # sql_str = "insert into permission_suggest (title, package_name, version_code, md5, category"
            sql_str = "select id"
            for perm_lbe in parse_result:
                sql_str += ", "+perm_dict[perm_lbe]
            sql_str += " from permission_suggest where package_name like '" + file_prop[1] +"%'"
            sql_tmp = []
            try:
                my.cur.execute(sql_str)
                row = my.cur.fetchone()

                for i in range(1, parse_result.__len__()+1):
                    if row[i] == "-":
                        sql_tmp.append(perm_dict[parse_result[i-1]]+"='?'")
                sql_update = "update permission_suggest set " + ",".join(sql_tmp) + " where id="+str(row[0])
                print sql_update
                my.cur.execute(sql_update)
                my.con.commit()
            except Exception as e:
                print e
                continue
    my.close()