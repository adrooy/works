import sqlite3

def compare_db(db1, db2):
    
    con1 = sqlite3.connect(db1)
    con1.row_factory = sqlite3.Row
    con1.text_factory = str
    cur1 = con1.cursor()
    
    con2 = sqlite3.connect(db2)
    con2.row_factory = sqlite3.Row
    con2.text_factory = str
    cur2 = con2.cursor()
    
    # android_metadata, single value compare
    am_sql = "select `locale` from `android_metadata`"
    am1 = cur1.execute(am_sql).fetchone()
    am2 = cur2.execute(am_sql).fetchone()
    if am1['locale'] != am2['locale']:
        print "android_metadata Mismatch: %s, %s" % (am1['locale'] , am2['locale'])
 
    # content, set vs set
    content_sql = "select * from `content`"
    content1 = set()
    content2 = set()
    for row in cur1.execute(content_sql):
        content1.add(row)
        #content1.add((row['areacode'],row['operator']))
    for row in cur2.execute(content_sql):
        content2.add(row)
        #content2.add((row['areacode'],row['operator']))
    if len(content1 ^ content2) > 0:
        print "content Mismatch"
    if len(content1 & content2) != len(content1):
        print "content Mismatch"
            
    # operator, set vs set
    op_sql = "select * from `lbe_operator`"
    op1 = set()
    op2 = set()
    for row in cur1.execute(op_sql):
        op1.add(row)
    for row in cur2.execute(op_sql):
        op2.add(row)
    if len(op1 ^ op2) > 0:
        print "lbe_operator Mismatch"

if __name__ == "__main__":
    compare_db("D:/workspace/lbesecv3/trunk/assets/operator_new.db", "D:/workspace/lbesecv3/trunk/assets/operator.db") 