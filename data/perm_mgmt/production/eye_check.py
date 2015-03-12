#coding: utf-8

import lbedb

SQL_SELECT_VALIDATE = 'select `title`, `perm_%s_suggest`, `perm_%s_description` from `permission`.`permission_suggest` where `finished` = 1 and `approved` = 1 order by install_count'

def check_perm(db, perm):
    global g_count, g_y_count, g_n_count, g_p_count, g_invalid_count, g_distinct_desc

    sqlstr = SQL_SELECT_VALIDATE % (perm, perm)
    db.cur.execute(sqlstr)

    for row in db.cur.fetchall():
        if row[2] is None:
            continue
        desc = row[2].strip().rstrip();
        suggest = row[1].strip().rstrip();
        if len(desc) > 0 and desc != '无' and desc != 'None' and desc != 'to do':
            print row[0], ",", suggest, ",", desc


db = lbedb.MySQL('192.168.1.15', 'root', '111111')
# check_perm(db, 'settings')
# check_perm(db, 'sendsms')
# check_perm(db, 'callphone')
# check_perm(db, 'smsdb')
# check_perm(db, 'contact')
# check_perm(db, 'calllog')
# check_perm(db, 'location')
# check_perm(db, 'phoneinfo')
# check_perm(db, 'netdefault')
# check_perm(db, 'netwifi')
# check_perm(db, 'recorder')
# check_perm(db, 'notification')
# check_perm(db, 'audiorecorder')
# check_perm(db, 'mmsdb')
# check_perm(db, 'sendmms')
# check_perm(db, 'mobileconnectivity')
# check_perm(db, 'wificonnectivity')
# check_perm(db, 'btconnectivity')
# check_perm(db, 'packageinfo')



# check_perm(db, 'callstate') # ignore
# check_perm(db, 'callmonitor') # ignore
# check_perm(db, 'autostart') # ignore
# check_perm(db, 'installpackage') # ignore
# check_perm(db, 'root') # ignore
