#-*- coding: utf-8 -*-

import lbedb
DB_HOST="192.168.1.15"
DB_USER="root"
DB_PASSWD="!LBE_Privacy#"
TABLE_NAME="`packagepermissions`.`lbe_backend_recommend_package_permissions_2014`"

def convert_all(in_db):
    out_db = lbedb.SQLite("static_cache_all.db")
    in_db.cur.execute("select * from %s where `permissions_accept` <> 0 or `permissions_reject` <> 0" % TABLE_NAME)
    id = 1
    for row in in_db.cur.fetchall():
        sqlstr = "insert into cached values(%d,'%s',1,%d,'',%d,0,%d,0,'')" % (id,row["package_name"], 0x7fffffff, row["permissions_accept"], row["permissions_reject"])
        id += 1
        #print sqlstr
        out_db.cur.execute(sqlstr)
    out_db.commit()
    out_db.close()
    return

def convert_top(in_db):
    out_db = lbedb.SQLite("static_cache_top10000.db")
    in_db.cur.execute("select * from %s where `permissions_accept` <> 0 or `permissions_reject` <> 0 order by `total_number` desc limit 10000" % TABLE_NAME)
    id = 1
    for row in in_db.cur.fetchall():
        sqlstr = "insert into cached values(%d,'%s',1,%d,'',%d,0,%d,0,'')" % (id,row["package_name"], 0x7fffffff, row["permissions_accept"], row["permissions_reject"])
        id += 1
        #print sqlstr
        out_db.cur.execute(sqlstr)
    out_db.commit()
    out_db.close()
    return


if __name__ == "__main__":
    in_db = lbedb.MySQL(DB_HOST, DB_USER, DB_PASSWD)
    convert_all(in_db)
    convert_top(in_db)
    in_db.close()
