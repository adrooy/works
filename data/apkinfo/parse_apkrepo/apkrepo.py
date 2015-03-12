#-*- coding: utf-8 -*-
# __author__ = 'sunzhennan'

import sys, time
import lbedb, parse_folder


#BASE_DIR=r"D:\backup\google_play_apks"
#TABLE_NAME="`szn`.`lbe_apkrepo_googleplay`"
#DB_HOST="192.168.227.138"
#DB_USER="root"
#DB_PASSWD="111111"
#PROGRESS_DISPLAY_STEP = 100

BASE_DIR = u"/mnt/nas2/apk/apkrepo"
TABLE_NAME="`szn1`.`lbe_apkrepo`"
DB_HOST="192.168.1.18"
DB_USER="root"
DB_PASSWD="!LBE_Privacy#"

def get_parsed_filenames(db):
    l = {}
    db.cur.execute("select `file_name` from %s;" % TABLE_NAME)
    while True:
        row = db.cur.fetchone()
        if row is None:
            break
        l[row[0]] = 1
    return l

db = lbedb.MySQL(DB_HOST, DB_USER, DB_PASSWD)
print "Start @ %s" % time.asctime()
parsed_files = get_parsed_filenames(db)
print "Done retrieve parsed files @ %s. (total: %d)" % (time.asctime(), len(parsed_files))
parse_folder.do(BASE_DIR, db, TABLE_NAME, parsed_files)
db.close()
