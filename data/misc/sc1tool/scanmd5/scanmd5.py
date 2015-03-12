#!/usr/bin/python

import MySQLdb as mdb
import sys, time, json, operator, re

def get_level(level_str):
    return {"NORMAL" : "0", "MEDIUM" : "1", "HIGH" : "3"}.get(level_str, "0")

def parse_all(con, fname):

    errfile = open(fname + ".error.txt", "w")
    notfoundfile = open(fname + ".notfound.csv", "w")
    outfile = open(fname + ".result.json", "w")

    cur = con.cursor(mdb.cursors.DictCursor)
    count = 0
    for line in open(fname + ".csv","r"):
        count += 1
        if count % 10000 == 0:
            print "%s  %d procced @%s" % (fname, count, time.asctime())
        csv = line.strip().rstrip().split(",")
        if len(csv) != 3:
            errfile.write(line)
            continue
        pkgname = csv[0]
        md5 = csv[2]
        try:
            sqlstr = "select * from `szn1`.`lbe_apkvirusscan_apk_scan_result` where `md5` = '%s'" % md5
            #print sqlstr
            cur.execute(sqlstr)
            if cur.rowcount == 0:
                #print "no result"
                notfoundfile.write(line)
                continue
            row = cur.fetchone()
            virus_details = row["virus_details"]
            adware_details = row["adware_details"]
            jdata = {}
            jdata[u"packageName"] = pkgname.decode('utf-8')
            jdata[u"apkMd5"] = md5.decode('utf-8')
            jdata[u"level"] = get_level(row["level"]).decode('utf-8')
            if (virus_details is not None and len(virus_details) > 0) or (adware_details is not None and len(adware_details) > 0):
                jdata[u"description"] = {}
                if virus_details is not None and len(virus_details) > 0:
                    jdata[u"description"][u"virus"] = json.loads(virus_details.decode('utf-8'))
                if adware_details is not None and len(adware_details) > 0:
                    jdata[u"description"][u"adwares"] = json.loads(adware_details.decode('utf-8'))
            jstr = json.dumps(jdata, ensure_ascii=False)
            outfile.write(jstr.encode('utf-8') + "\n")
            #print jstr.encode('utf-8')
        except Exception as e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            errfile.write(line)
            continue

if __name__ == "__main__":
    
    try:
        print "Start at: %s" % time.asctime()
        
        con = mdb.connect('192.168.1.18', 'root', '!LBE_Privacy#')
        con.set_character_set('utf8')
        parse_all(con, "file_list_1")
        parse_all(con, "file_list_2")
            
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if 'con' in locals():
            if con:
                con.close()
        else:
            print "open  db connection fail"        

