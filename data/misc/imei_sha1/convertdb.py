import MySQLdb as mdb 
import re, hashlib, sys, time, traceback

pat = re.compile(r"^[0-9a-fA-F]{40}$")

def getsha1(imei):
    global pat
    if pat.match(imei):
        return imei
    return hashlib.sha1(imei).hexdigest().upper()
    
def convert_table(con, table_name):
    global pat
    
    print "----------------- %s @ %s" % (table_name, time.asctime())

    cur = con.cursor(mdb.cursors.DictCursor)
    curupdate = con.cursor(mdb.cursors.Cursor);
    
    start = time.clock()

    sqlstr = "show columns from %s" % table_name
    print sqlstr
    cur.execute(sqlstr)
    
    has_imei = False
    has_rimei = False
    pk = ""
    for i in range(cur.rowcount):
        row = cur.fetchone()
        print row
        if row["Field"] == "imei":
            has_imei = True
        elif row["Field"] == "rimei":
            has_rimei = True
        if row["Key"] == "PRI":
            pk = row["Field"]
    
    if not has_imei:
        print "%s has no `imei` column" % table_name
        return
    
    if len(pk) > 0:
        print "use primary key: `%s`" % pk
    else:
        print "use imei as primary key"

    sys.stdout.flush()
    
    if not has_rimei:
        sqlstr = "alter table %s add column `rimei` char(40) NULL" % table_name
        print sqlstr
        cur.execute(sqlstr)
    else:
        print "already has rimei column"
    
    sys.stdout.flush()

    if len(pk) > 0:
        sqlstr = "select `imei`, `rimei`, `%s` from %s " % (pk, table_name)
        print sqlstr
    else:
        sqlstr = "select `imei`, `rimei` from %s " % table_name
        print sqlstr
        
    sys.stdout.flush()
    cur.execute(sqlstr)

    percent = 0
    for i in range(cur.rowcount):
        try:
            row = cur.fetchone()
            if not (row["imei"] is None):
                if pat.match(row["imei"]):
                    continue

            if len(pk) > 0:
                sqlstr = "update %s set `rimei`='%s', `imei`='%s' where `%s`='%s'" % (table_name, row["imei"], getsha1(row["imei"]), pk, row[pk])
                if i == 0:
                    print sqlstr
                curupdate.execute(sqlstr)
            else: 
                sqlstr = "update %s set `rimei`='%s', `imei`='%s' where `%s`='%s'" % (table_name, row["imei"], getsha1(row["imei"]), "imei", row["imei"])
                if i == 0:
                    print sqlstr
                curupdate.execute(sqlstr)
        except Exception, err:
                print traceback.format_exc()
                continue

        j = int(float(i)/float(cur.rowcount/100))
        if j != percent:
            percent = j
            print "%s%% (%s/%s) @ %s" % (percent, i, cur.rowcount, time.asctime()) 
        sys.stdout.flush()
        
        if i == cur.rowcount:
            print "100%% (%s/%s) @ %s" % (i, cur.rowcount, time.asctime())
    
    print "time cost: %s" % (time.clock() - start)
    curupdate.close()
    cur.close()
    
if __name__ == "__main__":
    
    try:
        con = mdb.connect('192.168.1.18', 'root', '!LBE_Privacy#')
        con.set_character_set('utf8')
	tables = open("tables","r")
        
        for table in tables:
            try:
                convert_table(con, table.rstrip().strip())
                sys.stdout.flush()
            except Exception, err:
                print traceback.format_exc()
                continue
            
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:
        if 'con' in locals():
            if con:
                con.close()
        else:
            print "open  db connection fail"        
