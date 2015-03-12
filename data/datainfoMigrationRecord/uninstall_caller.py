__author__ = 'sunzhennan'

import lbedb, lbeymd

DB_HOST="192.168.1.18"
DB_USER="root"
DB_PASSWD="!LBE_Privacy#"

DB_IN  = "datainfoMigrationRecord"
TABLE_IN = "lbe_backend_record_package_uninstall_%s"
DB_OUT = "szn1"
TABLE_OUT = "uninstall_caller_log"
TABLE_BOOKMARK = "uninstall_caller_log_bookmark"

def init_bookmark(db):
    db.cur.execute("select * from `%s`.`%s`" % (DB_OUT, TABLE_BOOKMARK))
    if db.cur.rowcount != 1:
        raise Exception("Invalid bookmark rowcount")
    row = db.cur.fetchone()

    bookmark = dict()
    bookmark["ymd"] = lbeymd.lbeymd(row["ymd"])
    if not bookmark["ymd"].valid:
        raise Exception("Invalid bookmark table name")
    bookmark["id"] = row["max_id"]
    return bookmark

def save_bookmark(db, bookmark):
    sqlstr = "update`%s`.`%s` set `ymd` = '%s' , `max_id` = %d" % (DB_OUT, TABLE_BOOKMARK, bookmark["ymd"].toString(), bookmark["id"])
    db.cur.execute(sqlstr)
    #print sqlstr
    db.commit()

def update_result(db, pkgname, uninstall_caller):
    db.cur.execute("insert into `%s`.`%s` values ('%s', '%s', 1) ON DUPLICATE KEY UPDATE `cnt` = `cnt`+1" % (DB_OUT, TABLE_OUT, uninstall_caller, pkgname))

def parse_table(dbin, dbout, bookmark):
    sqlstr = "SELECT `id`, `package_name`, `uninstall_caller` FROM `%s`.`%s` WHERE `uninstall_caller` IS NOT NULL AND LENGTH(`uninstall_caller`) > 0 AND `id` > %d ORDER BY id;" \
                     % (DB_IN, TABLE_IN % bookmark["ymd"].toString(), bookmark["id"])
    print sqlstr
    dbin.cur.execute(sqlstr)

    while True:
        row = dbin.cur.fetchone()
        if row is None:
            break
        pkgname = row["package_name"]
        uninstall_callers = set(row["uninstall_caller"].split("\n"))
        for uninstall_caller in uninstall_callers:
            update_result(dbout, pkgname, uninstall_caller)

        # save bookmark every 1000 records (not 1000 records with valid uninstall_caller)
        if bookmark["id"] + 1000 < row["id"]:
            bookmark["id"] = row["id"]
            save_bookmark(dbout, bookmark)


if __name__ == "__main__":
    dbin = lbedb.MySQL(DB_HOST, DB_USER, DB_PASSWD)
    dbout = lbedb.MySQL(DB_HOST, DB_USER, DB_PASSWD)
    bookmark = init_bookmark(dbout)
    print bookmark["ymd"].toString(), bookmark["id"]
    print lbeymd.lbeymd().toString()

    while int(bookmark["ymd"].toString()) < int(lbeymd.lbeymd().toString()) - 2: # out backend data are 2 days behind the ready date
        parse_table(dbin, dbout, bookmark)
        bookmark["ymd"].inc()
        bookmark["id"] = 0
        save_bookmark(dbout, bookmark)

