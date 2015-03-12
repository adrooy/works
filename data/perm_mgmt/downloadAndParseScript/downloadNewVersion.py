__author__ = 'zz'
# coding=utf-8
import os
# import datetime
import urllib2
import sys
import MySQLdb

from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis, ganalysis
from androguard.core import androconf


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
        if ret_type == 'APK':
            a = apk.APK(filename)

            if a.is_valid_APK():
                vm = dvm.DalvikVMFormat(a.get_dex())
            else:
                print 'INVALID APK'
                return "Error"
        else:
            print 'INPUT ERROR'
            return "Error"

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
                   "PERM_ID_AUTOSTART":"perm_autostart_suggest",
                   "PERM_ID_NOTIFICATION":"perm_notification_suggest",
                   "PERM_ID_INSTALL_PACKAGE":"perm_installpackage_suggest",
                   "PERM_ID_AUDIO_RECORDER":"perm_audiorecorder_suggest",
                   "PERM_ID_MMSDB":"perm_mmsdb_suggest",
                   "PERM_ID_SENDMMS":"perm_sendmms_suggest",
                   "PERM_ID_MOBILE_CONNECTIVITY":"perm_mobileconnectivity_suggest",
                   "PERM_ID_WIFI_CONNECTIVITY":"perm_wificonnectivity_suggest",
                   "PERM_ID_BT_CONNECTIVITY":"perm_btconnectivity_suggest"}

    category = sys.argv[0]
    title = sys.argv[1]
    package_name = sys.argv[2]
    version_code = sys.argv[3]
    download_url = sys.argv[4]
    md5 = sys.argv[5]

    db_host = "localhost"
    db_user = "root"
    db_passwd = "!LBE_Privacy#"
    db_name = "permission"

    #table = "permission_suggest"
    my = MySQL(db_host, db_user, db_passwd, db_name)
    if my.con is None:
        print("Cannot connect to DB, please check.")
        sys.exit()
    else:
        my.close()

    save_path = "download/"+category+"/"+title+"_"+package_name+"_"+str(version_code)+".apk"
    save_path = os.path.join(os.getcwd(), save_path)
    # save_path = "/home/zz/PycharmProjects/androguard/download/票务/美历_cn.etouch.ecalendar.ladies_11.apk"
    print("Downloading "+title+" "+package_name+"...")

    #urllib.urlretrieve(downloadUrl1, save_path)
    try:
        f = urllib2.urlopen(download_url, None, 180)
        data = f.read()
        with open(save_path, "wb") as code:
            code.write(data)
    except Exception as e:
        print(e)
        print("Cannot download  apk, process next one")

    #after download apk, analyze and write into db
    print("Analyze apk...")
    sql_str = "insert into permission_suggest (title, package_name, version_code, md5, category"
    perm_number = 0
    parse_result = ""
    try:
        parse_result = parseApk(save_path, permissions)
    except Exception as e:
        print(str(e))
        print("Analyze error, process next one")
        sys.exit()
    print parse_result
    if parse_result == "Error":
        print("Analyze error, process next one")
        sys.exit()
    for perm_lbe in parse_result:
        sql_str += ", "+perm_dict[perm_lbe]+" "
        perm_number += 1
    sql_tmp = "', '".join([title, package_name, str(version_code), md5, category])
    sql_str += ") values ('"+sql_tmp+"'"
    for i in range(0, perm_number):
        sql_str += ",'?'"
    sql_str += ")"
    print(sql_str)
    print("Insert DB records")
    try:
        my = MySQL(db_host, db_user, db_passwd, db_name)
        my.cur.execute(sql_str)
        my.con.commit()
    except Exception as e:
        print("Cannot insert this record into DB: " + str(e))
        sys.exit()
    finally:
        my.close()