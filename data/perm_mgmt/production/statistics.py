#coding: utf-8

import lbedb

SQL_SELECT_VALIDATE = 'select `title`, `perm_%s_suggest`, `perm_%s_description` from `permission`.`permission_suggest` where `finished` = 1 and `approved` = 1'

g_count = 0
g_y_count = 0
g_n_count = 0
g_p_count = 0
g_invalid_count = 0
g_distinct_desc = []

def check_perm(db, perm):
    global g_count, g_y_count, g_n_count, g_p_count, g_invalid_count, g_distinct_desc

    sqlstr = SQL_SELECT_VALIDATE % (perm, perm)
    db.cur.execute(sqlstr)

    count = 0
    y_count = 0
    n_count = 0
    p_count = 0
    invalid_count = 0

    for row in db.cur.fetchall():
        if row[2] is None:
            continue
        desc = row[2].strip().rstrip();
        suggest = row[1].strip().rstrip();
        if len(desc) > 0 and desc != '无' and desc != 'None' and desc != 'to do':
            if suggest == 'y':
                y_count += 1
            elif suggest == 'n':
                n_count += 1
            elif suggest == '?' or suggest == 'p':
                p_count += 1
            else:
                print "invalid:", row[0], suggest, row[2]
                invalid_count += 1
            #print row[0], ",", row[1], ",", row[2]
            count += 1
            g_distinct_desc.append(desc)
        else:
            if suggest == 'y' or suggest == 'n':
                print row[0], ":", perm, ":", suggest, ":", desc

    #print perm, ":", "total:" , count, "yes:", y_count, "no:", n_count, "prompt:", p_count, "invalid:", invalid_count

    g_count += count
    g_y_count += y_count
    g_n_count += n_count
    g_p_count += p_count
    g_invalid_count += invalid_count


db = lbedb.MySQL('192.168.1.15', 'root', '111111')
check_perm(db, 'settings')
check_perm(db, 'sendsms')
check_perm(db, 'callphone')
check_perm(db, 'smsdb')
check_perm(db, 'contact')
check_perm(db, 'calllog')
check_perm(db, 'location')
check_perm(db, 'phoneinfo')
check_perm(db, 'netdefault')
check_perm(db, 'netwifi')
check_perm(db, 'callstate')
check_perm(db, 'callmonitor')
check_perm(db, 'recorder')
check_perm(db, 'autostart')
check_perm(db, 'notification')
check_perm(db, 'installpackage')
check_perm(db, 'audiorecorder')
check_perm(db, 'mmsdb')
check_perm(db, 'sendmms')
check_perm(db, 'mobileconnectivity')
check_perm(db, 'wificonnectivity')
check_perm(db, 'btconnectivity')
check_perm(db, 'root')
check_perm(db, 'packageinfo')

g_distinct_desc = set(g_distinct_desc)
print ""
print "GRAND TOTAL:", "total:" , g_count, "distinct:", len(g_distinct_desc), "yes:", g_y_count, "no:", g_n_count, "prompt:", g_p_count, "invalid:", g_invalid_count

longest_desc = ""
for desc in g_distinct_desc:
    if len(desc.decode("utf-8")) > len(longest_desc.decode("utf-8")):
        longest_desc = desc

print "longest desc:", longest_desc
print "lognest length;", len(longest_desc.decode("utf-8"))