#coding: utf-8
__author__ = 'sunzhennan'

import lbedb

name_mapping = {
    'sendsms'       : 1,
    'callphone'     : 2,
    'smsdb'         : 3,
    'contact'       : 4,
    'calllog'       : 5,
    'location'      : 6,
    'phoneinfo'     : 7,
    'netdefault'    : 8,
    'netwifi'       : 9,
    'recorder'      : 13,
    'settings'      : 14,
    'notification'  : 16,
    'audiorecorder' : 18,
    'mmsdb'         : 19,
    'sendmms'       : 20,
    'mobileconnectivity'    : 21,
    'wificonnectivity'      : 22,
    'btconnectivity'        : 23,
    'packageinfo'           : 29
}

action_mapping = {
    '?' : 'prompt',
    'p' : 'prompt',
    'P' : 'prompt',
    'y' : 'accept',
    'Y' : 'accept',
    'n' : 'reject',
    'N' : 'reject'
}


SQL_SELECT_VALIDATE = 'select `package_name`, `perm_%s_suggest`, `perm_%s_description` from `permission`.`permission_suggest` where `finished` = 1 and `approved` = 1 order by install_count'
SQL_INSERT = "INSERT INTO `pkgperm`.`lbe_backend_recommend_package_permissions_manual` VALUES('%s','default',"\
                "NULL,0,0,0,NULL,NULL,NULL,NULL,NULL,NULL,"\
                "NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,"\
                "NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,"\
                "NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,"\
                "NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,"\
                "NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,"\
                "NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,"\
                "NULL)"
SQL_UPDATE = "UPDATE `pkgperm`.`lbe_backend_recommend_package_permissions_manual` set `permissions_%s`=`permissions_%s`|(1<<(%d-1)), `desc_perm%d`='%s' where `package_name`='%s'"

def update(srcdb, dstdb, name):
    global name_mapping

    sqlstr = SQL_SELECT_VALIDATE % (name, name)
    srcdb.cur.execute(sqlstr)

    for row in srcdb.cur.fetchall():
        if row[2] is None:
            continue
        pkgname = row[0].strip().rstrip()
        suggest = row[1].strip().rstrip();
        desc = row[2].strip().rstrip();
        if len(desc) > 0 and desc != '无' and desc != 'None' and desc != 'to do':
            try:
                dstdb.cur.execute(SQL_INSERT % pkgname)
            except:
                pass    # we might have insert the same package for more than 1 permission
            sqlstr = SQL_UPDATE % (action_mapping[suggest], action_mapping[suggest], name_mapping[name], name_mapping[name], desc, pkgname)
            dstdb.cur.execute(sqlstr)


srcdb = lbedb.MySQL("192.168.1.15", "root", "111111")
dstdb = lbedb.MySQL("192.168.1.18", "root", "!LBE_Privacy#")
dstdb.cur.execute("truncate `pkgperm`.`lbe_backend_recommend_package_permissions_manual`")

for name in name_mapping:
    update(srcdb, dstdb, name)

srcdb.close()

dstdb.commit()
dstdb.close()
