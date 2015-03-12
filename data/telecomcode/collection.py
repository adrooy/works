# -*- coding: GBK -*-

import sqlite3, json, traceback

# 当前的文本与360保持一致，便于解析
Operators = {
             0 : ["TELECOM", "中国电信".decode("GBK"), "电信".decode("GBK")],
             1 : ["UNICOM", "中国联通".decode("GBK"), "联通3G".decode("GBK")],
             2 : ["UNICOM", "中国联通".decode("GBK"), "联通2G".decode("GBK")],
             3 : ["CMCC", "中国移动".decode("GBK"), "动感地带".decode("GBK")],
             4 : ["CMCC", "中国移动".decode("GBK"), "全球通".decode("GBK")],
             5 : ["CMCC", "中国移动".decode("GBK"), "神州行".decode("GBK")]
             }

Messages = {}

AreaNames = {}

def init_area_names():
    global AreaNames
    f = open('normailzed.csv','r')
    for line in f:
        line = line.decode("GBK")
        csv = line.rstrip().strip().split(',')
        if len(csv) >= 3:
            AreaNames[int(csv[0])] = (csv[1],csv[2])
        else:
            print "------------------------------------" + line
    f.close()

def init_msg_map():
    global Messages
    
    con = sqlite3.connect("D:/workspace/lbesecv3/trunk/assets/operator.old.db")
    con.row_factory = sqlite3.Row
    con.text_factory = str
    cur = con.cursor()
    
    for row in cur.execute("select * from lbe_operator"):
        for key in Messages:
            if (row['number'], row['content']) == Messages[key]:
                print "WARNING: duplicate message content in `lbe_operator`: %d and %d, content: %d, %s" % (key, row['id'], row['number'], row['content'])
        Messages[row['id']] = (row['number'], row['content'])
    
    cur.close()
    con.close()

def print_msg_map():
    global Messages
    
    for key in Messages:
        print "%d: %d, %s" % (key, Messages[key][0], Messages[key][1])
          
def get_lbe_collection():
  
    con = sqlite3.connect("D:/workspace/lbesecv3/trunk/assets/operator.old.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    area_and_ops_mapping = {}
    for row in cur.execute("select * from content"):
            longi = row['operator']
            for operator in Operators.keys():
                area_and_ops_mapping[(int(row['areacode']), operator)] = (longi >> (operator * 8)) & 0xff  
    
    cur.close()
    con.close()
    return area_and_ops_mapping

def get_360_collection():
    global Messages
    
    f = open("360GBK.txt","r")
    area_and_ops_mapping = {}
    line_count = 0
    invalid_count = 0
    dup_count = 0
    newmsg_count = 0
    
    for line in f:
        line_count += 1
        try:
            line = line.rstrip().strip().decode("GBK")
            csv = line.split(',')
            if len(csv) < 6:
                print "----------------invalid 360 input line--------------------" + line
                invalid_count += 1
                continue
    
            areacode = int(csv[0])
                            
            operator = -1
            for op_key in Operators:
                if Operators[op_key][1] == csv[3] and Operators[op_key][2] == csv[4]:
                    operator = op_key
            
            if operator == -1:
                print "--------------invalid operator + brand----------------------" + line
                invalid_count += 1
                continue
            
            #print ",".join(csv[5:])
            traffic_map = json.loads(",".join(csv[5:]))
            traffic_map["traffic_code"] = traffic_map["traffic_code"].replace('"', '')
            #print traffic_map["traffic_number"] + traffic_map["traffic_code"]
            if traffic_map["traffic_number"] == "NULL" or traffic_map["traffic_code"] == "NULL":
                invalid_count += 1
                continue
            traffic_tuple = (int(traffic_map["traffic_number"]),traffic_map["traffic_code"])
            traffic_id = -1
            
            for k in Messages.keys():
                if Messages[k] == traffic_tuple:
                    traffic_id = k
                    break
            
            if traffic_id != -1:
                #print "messages found in lbe db, id=%d" % traffic_id
                pass
            else:
                traffic_id = max(Messages.keys()) + 1
                newmsg_count += 1
                print "new message format: id=%d, num=%s, content=%s" % (traffic_id, traffic_tuple[0], traffic_tuple[1].encode("GBK"))
                Messages[max(Messages.keys()) + 1] = traffic_tuple
            
            if (areacode, operator) in area_and_ops_mapping.keys():
                dup_count += 1
                print "Duplicate found in 360: %d, %s, %s" % (areacode, Operators[operator][1], Operators[operator][2])
            area_and_ops_mapping[(areacode, operator)] = traffic_id
                
        except Exception as e:
            print "----------------invalid 360 input line--------------------" + line
            invalid_count += 1
            print traceback.format_exc()
        
    print "360 invalid lines: %d, dup lines: %d / total lines: %d" % (invalid_count, dup_count, line_count)
    print "new message format count: %d" % newmsg_count
    print "valid 360 result: %d" % len(area_and_ops_mapping)
    if invalid_count + dup_count + len(area_and_ops_mapping) != line_count:
        print "!!!!!!!!!!RESULT IS NOT RIGHT"    
    return area_and_ops_mapping
        

def print_collection(area_and_ops_mapping):
    for key in area_and_ops_mapping:
        try:
            print AreaNames[key[0]][0] + AreaNames[key[0]][1] + " " + Operators[key[1]][1] + " " + Operators[key[1]][2] + ":     "  +  str(Messages[area_and_ops_mapping[key]][0]) + ",      \"" + Messages[area_and_ops_mapping[key]][1] + "\""
        except Exception as e:
            if e.args[0] == 0:
                pass
            else:
                print traceback.format_exc()                   

def merge_collections(lbe, qihoo):
    
    global AreaNames, Operators, Messages
    
    matched_count = 0
    added_count = 0
    updated_count = 0    
    areas = set()
    updated_msg_id = set()
    updated_new_msg_count = 0
    total_areas = 0
    
    for key in lbe:
        areas.add(key[0])
    total_areas = len(areas)
    
    for key in qihoo:
        if key in lbe.keys():
            if qihoo[key] == lbe[key]:
                matched_count += 1
            else:
                updated_count += 1
                if key[0] in areas:
                    areas.remove(key[0])
                updated_msg_id.add(qihoo[key])
                if qihoo[key] >= 50:    # old db has only 49
                    updated_new_msg_count += 1
                
                if lbe[key] != 0:
                    print str(key[0]).rjust(6) + ("(" + AreaNames[key[0]][0].encode("GBK") + AreaNames[key[0]][1].encode("GBK") + ")").ljust(16) + \
                          (Operators[key[1]][1].encode("GBK") + Operators[key[1]][2].encode("GBK")).ljust(20) + \
                          "   FROM: id[" + str(lbe[key])   + "]: " + str(Messages[lbe[key]][0])   + "," + Messages[lbe[key]][1] + \
                          "   TO:   id[" + str(qihoo[key]) + "]: " + str(Messages[qihoo[key]][0]) + "," + Messages[qihoo[key]][1]
                else:
                    print str(key[0]).rjust(6) + ("(" + AreaNames[key[0]][0].encode("GBK") + AreaNames[key[0]][1].encode("GBK") + ")").ljust(16) + \
                          (Operators[key[1]][1].encode("GBK") + Operators[key[1]][2].encode("GBK")).ljust(20) + \
                          "   FROM: id[" + str(lbe[key])   + "]: " + "None"   + "," + "None" + \
                          "   TO:   id[" + str(qihoo[key]) + "]: " + str(Messages[qihoo[key]][0]) + "," + Messages[qihoo[key]][1]
                    
                lbe[key] = qihoo[key]
        else:
            added_count += 1
            lbe[key] = qihoo[key]
    
    print "Matched %d. Updated %d. Added %d. Total from 360: %d. Total in LBE base(result): %d" % (matched_count , updated_count , added_count , len(qihoo), len(lbe))
    print "Updated new msg count: %d, updated ids:" %(updated_new_msg_count)
    print updated_msg_id
    print "Unchanged areas: %d (total %d):" % (len(areas),total_areas)
    print areas
    
    if matched_count + added_count + updated_count != len(qihoo):
        print "!!!!!!!!!!RESULT IS NOT RIGHT"

def save_result(lbe):
    global Messages
    
    con = sqlite3.connect("D:/workspace/lbesecv3/trunk/assets/operator_new.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    cur.execute("drop table if exists `android_metadata`")
    cur.execute("drop table if exists `lbe_operator`")
    cur.execute("drop table if exists `content`")
    
    cur.execute("CREATE TABLE android_metadata (locale TEXT)")
    cur.execute("CREATE TABLE [content] ([areacode] integer NOT NULL PRIMARY KEY, [operator] long)")
    cur.execute("CREATE TABLE lbe_operator(id integer primary key autoincrement, number integer, content varchar(20))")
    
    cur.execute("insert into `android_metadata` values('zh_CN');")
    
    for key in Messages:
        cur.execute("insert into `lbe_operator` values(%d,%d,'%s');" % (key, Messages[key][0], Messages[key][1].encode("UTF-8")))
    con.commit()
    
    #cur.execute("update `content` set `operator` = 0")
    con.commit()

    progress = 0
    for key in lbe:
        progress += 1
        print str(progress)
        
        cur.execute("select `operator` from `content` where `areacode` = %d" % key[0])
        longi = 0
        row = cur.fetchone()
        if row != None:
            longi = row['operator']
            #print "fetched operator: %d" % longi
        longi += (lbe[key] << (key[1] * 8))
        
        #print str(key[0]) + ":" + str(key[1]) + "-" + str(longi)
        if row != None:
            cur.execute("update `content` set `operator`=%d where `areacode`=%d" % (longi, key[0]))
        else:
            cur.execute("insert into `content` values(%d,%d)" % (key[0], longi))
            
        con.commit()
    
    cur.close()
    con.close()


if __name__ == "__main__":
    """ collection map: { ( area code, operator id) : message id }
        message map: { message id : ( number, content ) }
        area map: { area code : ( province, city ) }
    """
        
    print "=====================start"
    init_area_names()

    init_msg_map()
    #print_msg_map()
    
    lbe = get_lbe_collection()
    #print_collection(lbe)
    
    qihoo = get_360_collection()
    #print_collection(qihoo)
    
    merge_collections(lbe, qihoo)
    
    save_result(lbe)
    
    print "=====================end"
    