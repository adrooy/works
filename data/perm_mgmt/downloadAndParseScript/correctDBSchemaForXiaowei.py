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


if __name__ == '__main__':

    perm_list = ["perm_sendsms_suggest",
                   "perm_callphone_suggest",
                   "perm_smsdb_suggest",
                   "perm_contact_suggest",
                   "perm_calllog_suggest",
                   "perm_location_suggest",
                   "perm_phoneinfo_suggest",
                   "perm_netdefault_suggest",
                   "perm_netwifi_suggest",
                   "perm_root_suggest",
                   "perm_callstate_suggest",
                   "perm_callmonitor_suggest",
                   "perm_recorder_suggest",
                   "perm_settings_suggest",
                   "perm_autostart_suggest",
                   "perm_notification_suggest",
                   "perm_audiorecorder_suggest",
                   "perm_mmsdb_suggest",
                   "perm_sendmms_suggest",
                   "perm_mobileconnectivity_suggest",
                   "perm_wificonnectivity_suggest",
                   "perm_btconnectivity_suggest"]

    db_host = "192.168.1.15"
    db_user = "root"
    db_passwd = "!LBE_Privacy#"
    db_name = "permission"
    my = MySQL(db_host, db_user, db_passwd, db_name)
    sql_str = "select id," + ",".join(perm_list) + " from permission_suggest where finished=0"
    print sql_str
    my.cur.execute(sql_str)
    while True:
        row = my.cur.fetchone()
        if row is None:
            break
        sql_tmp = []
        for i in range(1, perm_list.__len__()+1):
            if row[i] == "" or row[i] is None:
                sql_tmp.append(perm_list[i-1]+"='-'")
        if sql_tmp.__len__() == 0:
            continue
        sql_update = "update permission_suggest set " + ",".join(sql_tmp) + " where id="+str(row[0])
        print sql_update
        my1 = None
        try:
            my1 = MySQL(db_host, db_user, db_passwd, db_name)
            my1.cur.execute(sql_update)
            my1.con.commit()
        except Exception as e:
            print("Cannot insert this record into DB: " + str(e))
            continue
        finally:
            my1.close()
    my.close()