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


def parseApk(filename):
    if filename is not None:
        ret_type = androconf.is_android(filename)
        vm = None
        a = None
        # md5 = None
        if ret_type == 'APK':
            a = apk.APK(filename)
            # md5 = a.md5

        if a.is_valid_APK():
            vm = dvm.DalvikVMFormat(a.get_dex())
        vmx = analysis.VMAnalysis(vm)

        # if "NOTIFICATION" in vmx.get_permissions([]):
        if "PACKAGE_INFO" in vmx.get_permissions([]):
            return True
        else:
            return False


if __name__ == '__main__':

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

    dirpath = "app-apk"

    file_entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    file_entries = ((os.stat(file_path), file_path) for file_path in file_entries)
    file_entries = ((file_stat.st_ctime, file_path) for file_stat, file_path in file_entries)
    for cdate, file in sorted(file_entries):
        file_prop = os.path.basename(file).split("_&_")
        parse_result = ""
        perm_number = 0
        try:
            parse_result = parseApk(file)
        except Exception as e:
            print(str(e))
            print("Analyze error, process next one")
            continue
        if not parse_result:
            continue

        # sql_str = "update permission_suggest set perm_notification_suggest ='?' where package_name ='"+file_prop[1]+"' and perm_notification_suggest='-'"
        sql_str = "update permission_suggest set perm_packageinfo_suggest ='?' where package_name ='"+file_prop[1]+"'"
        print("Update DB records")
        print(sql_str)
        try:
            my.cur.execute(sql_str)
            my.con.commit()
        except Exception as e:
            print("Cannot insert this record into DB: " + str(e))
            continue
    my.close()