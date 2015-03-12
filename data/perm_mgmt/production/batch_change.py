#coding: utf-8
__author__ = 'sunzhennan'

import lbedb

SQL_SELECT_VALIDATE = 'select `title`, `perm_%s_suggest`, `perm_%s_description` from `permission`.`permission_suggest` where `finished` = 1 and `approved` = 1 order by install_count'

def change_btconnectivity(db):

    sqlstr = "select `perm_btconnectivity_description` from `permission`.`permission_suggest` where `perm_btconnectivity_description` = '用于开启或关闭蓝牙'"
    db.cur.execute(sqlstr)
    for row in db.cur.fetchall():
        print row[0]

    # sqlstr = "UPDATE `permission`.`permission_suggest` set `perm_btconnectivity_suggest` = '', `perm_btconnectivity_description` = NULL where `perm_btconnectivity_description` = '用于开启或关闭蓝牙'"
    # db.cur.execute(sqlstr)


db = lbedb.MySQL('192.168.1.15', 'root', '111111')
change_btconnectivity(db)