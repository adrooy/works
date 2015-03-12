__author__ = 'sunzhennan'

import sys, time, traceback
import lbedb
import userinfo_pb2

tables = [
     "lbe_backend_userdatainfo_original_20140110",
     "lbe_backend_userdatainfo_original_20140111",
     "lbe_backend_userdatainfo_original_20140112",
     "lbe_backend_userdatainfo_original_20140113",
     "lbe_backend_userdatainfo_original_20140114",
     "lbe_backend_userdatainfo_original_20140115",
     "lbe_backend_userdatainfo_original_20140116"
    # "lbe_backend_userdatainfo_original_20140109",
    # "lbe_backend_userdatainfo_original_20140108",
    # "lbe_backend_userdatainfo_original_20140107",
    # "lbe_backend_userdatainfo_original_20140106",
    # "lbe_backend_userdatainfo_original_20140105",
    # "lbe_backend_userdatainfo_original_20140104",
    # "lbe_backend_userdatainfo_original_20140103",
    # "lbe_backend_userdatainfo_original_20140102",
    # "lbe_backend_userdatainfo_original_20140101",
    # "lbe_backend_userdatainfo_original_20131231",
    # "lbe_backend_userdatainfo_original_20131230",
    # "lbe_backend_userdatainfo_original_20131229",
    # "lbe_backend_userdatainfo_original_20131228",
    # "lbe_backend_userdatainfo_original_20131227",
    # "lbe_backend_userdatainfo_original_20131226",
    # "lbe_backend_userdatainfo_original_20131225",
    # "lbe_backend_userdatainfo_original_20131224",
    # "lbe_backend_userdatainfo_original_20131223",
    # "lbe_backend_userdatainfo_original_20131222",
    # "lbe_backend_userdatainfo_original_20131221",
    # "lbe_backend_userdatainfo_original_20131220",
    # "lbe_backend_userdatainfo_original_20131219",
    # "lbe_backend_userdatainfo_original_20131218",
    # "lbe_backend_userdatainfo_original_20131217",
    # "lbe_backend_userdatainfo_original_20131216",
    # "lbe_backend_userdatainfo_original_20131215",
    # "lbe_backend_userdatainfo_original_20131214",
    # "lbe_backend_userdatainfo_original_20131213",
    # "lbe_backend_userdatainfo_original_20131212",
    # "lbe_backend_userdatainfo_original_20131211",
    # "lbe_backend_userdatainfo_original_20131210",
    # "lbe_backend_userdatainfo_original_20131209",
    # "lbe_backend_userdatainfo_original_20131208",
    # "lbe_backend_userdatainfo_original_20131207",
    # "lbe_backend_userdatainfo_original_20131206",
    # "lbe_backend_userdatainfo_original_20131205",
    # "lbe_backend_userdatainfo_original_20131204",
    # "lbe_backend_userdatainfo_original_20131203",
    # "lbe_backend_userdatainfo_original_20131202",
    # "lbe_backend_userdatainfo_original_20131201",
    # "lbe_backend_userdatainfo_original_20131130",
    # "lbe_backend_userdatainfo_original_20131129",
    # "lbe_backend_userdatainfo_original_20131128",
    # "lbe_backend_userdatainfo_original_20131127",
    # "lbe_backend_userdatainfo_original_20131126",
    # "lbe_backend_userdatainfo_original_20131125",
    # "lbe_backend_userdatainfo_original_20131124",
    # "lbe_backend_userdatainfo_original_20131123",
    # "lbe_backend_userdatainfo_original_20131122",
    # "lbe_backend_userdatainfo_original_20131121",
    # "lbe_backend_userdatainfo_original_20131120",
    # "lbe_backend_userdatainfo_original_20131119",
    # "lbe_backend_userdatainfo_original_20131118",
    # "lbe_backend_userdatainfo_original_20131117",
    # "lbe_backend_userdatainfo_original_20131116",
    # "lbe_backend_userdatainfo_original_20131115",
    # "lbe_backend_userdatainfo_original_20131114",
    # "lbe_backend_userdatainfo_original_20131113",
    # "lbe_backend_userdatainfo_original_20131112",
    # "lbe_backend_userdatainfo_original_20131111",
    # "lbe_backend_userdatainfo_original_20131110",
    # "lbe_backend_userdatainfo_original_20131109",
    # "lbe_backend_userdatainfo_original_20131108",
    # "lbe_backend_userdatainfo_original_20131107",
    # "lbe_backend_userdatainfo_original_20131106",
    # "lbe_backend_userdatainfo_original_20131105",
    # "lbe_backend_userdatainfo_original_20131104",
    # "lbe_backend_userdatainfo_original_20131103",
    # "lbe_backend_userdatainfo_original_20131102",
    # "lbe_backend_userdatainfo_original_20131101",
    # "lbe_backend_userdatainfo_original_20131031",
    # "lbe_backend_userdatainfo_original_20131030",
    # "lbe_backend_userdatainfo_original_20131029",
    # "lbe_backend_userdatainfo_original_20131028",
    # "lbe_backend_userdatainfo_original_20131027",
    # "lbe_backend_userdatainfo_original_20131026",
    # "lbe_backend_userdatainfo_original_20131025",
    # "lbe_backend_userdatainfo_original_20131024"
]

g_row_exception = 0
g_table_exception = 0

def log_exception(msg):
    errf = open("error.log", "ab")
    errf.write("---------- %s\n" % msg)
    errf.write(traceback.format_exc())
    errf.write("\n\n\n")
    errf.close()

def parse_row(row):
    userinfo = userinfo_pb2.UserDataInfo()
    userinfo.ParseFromString(row[0])
    if userinfo.battery is not None and len(userinfo.battery.fingerprint) > 0 and userinfo.battery.capacity > 0:
        resultf = open("result.csv", "ab")
        resultf.write("%s,%d\n" % (userinfo.battery.fingerprint, userinfo.battery.capacity))
        resultf.close()

def parse_table(table):
    global g_row_exception

    row_count = 0
    print "Table %s Start @ %s" % (table, time.asctime())
    db = lbedb.MySQL("127.0.0.1", "root", "")
    db.cur.execute("select `data` from `datainfoOriginal`.`%s`" % table)
    row = db.cur.fetchone()
    while row is not None:
        try:
            row_count += 1
            if (row_count % 100000) == 0:
                print "Table %s parsed %d @ %s" % (table, row_count, time.asctime())
            parse_row (row)
        except Exception as e:
            g_row_exception += 1
            log_exception("RowException of %s (%d)" % (table, g_row_exception))
        row = db.cur.fetchone()
    db.close()
    print "Table %s Done @ %s" % (table, time.asctime())

for table in tables:
    global g_table_exception

    print "Start @ %s" % time.asctime()
    try:
        parse_table(table)
    except Exception as e:
        g_table_exception += 1
        log_exception("TableException of %s (%d)" % (table, g_table_exception))
    print "Done @ %s" % time.asctime()
