# -*- coding: gbk -*-
import httplib, string, re, json, os, traceback

model_replacing_table = {
                         "三星".encode("GBK") : "samsung",
                         "联想".encode("GBK") : "lenovo",
                         "联想".encode("GBK") : "lenovo",
                         "中兴".encode("GBK") : "zte",
                         "华为".encode("GBK") : "huawei",
                         "酷派".encode("GBK") : "coolpad",
                         "魅族".encode("GBK") : "meizu",
                         "索尼".encode("GBK") : "sony",
                         "索尼爱立信".encode("GBK") : "sonyericsson",
                         "小米".encode("GBK") : "xiaomi",
                         "天语".encode("GBK") : "k-touch",
                         "摩托罗拉".encode("GBK") : "motorola",
                         "康佳".encode("GBK") : "konka",
                         "金立".encode("GBK") : "gionee",
                         "海信".encode("GBK") : "hisense",
                         "夏普".encode("GBK") : "sharp",
                         "佳域".encode("GBK") : "alps",
                         "戴尔".encode("GBK") : "dell",
                         "谷歌".encode("GBK") : "google",
                         "富士通".encode("GBK") : "FUJITSU".lower(),
                         "爱国者".encode("GBK") : "aigo",
                         "宏碁".encode("GBK") : "acer",
                         "夏新".encode("GBK") : "amoi",
                         "HTC" : "htc",
                         "oppo" : "oppo",
                         "lg" : "lge",
                         "纽曼".encode("GBK") : "newsmy",
                         "步步高".encode("GBK") : "BBK",
                         "亿通".encode("GBK") : "eton"
                         }

model_replacing_table2 = {
                         "酷派".encode("GBK") : "yulong"
                        }
def crawl_list():
    
    #httpconn = httplib.HTTPConnection("product.cnmo.com")
    
    for i in range(1, 57):
        
#         httpconn.request("GET", "/all/product_s20_t1_p%s.html" % i)
#         response = httpconn.getresponse()
#         file = open("listfiles/%s.html" % i, "w")
#         content = response.read()
#         file.write(content)
#         file.close()
        
        content = open("listfiles/%d.html" % i, "r").read()
        list = open("list.txt", "a")
        for line in content.split("\n"):
            line = line.decode("gbk")
            pos = line.rfind("参数".decode("gbk"))
            if pos != -1:
                #print line
                #print line[ line.rfind("http",0,pos) : line.rfind("html",0,pos) + 4]
                url = line[ line.rfind("http",0,pos) : line.rfind("html",0,pos) + 4]
                if len(url) > 0:
                    list.write(line[ line.rfind("http",0,pos) : line.rfind("html",0,pos) + 4])
                    list.write("\n")
        list.close()
        
    #httpconn.close()

def crawl_phoneinfo():
    httpconn = httplib.HTTPConnection("product.cnmo.com")
    batterycsv = open ("battery.csv", "w")
    batteryjson = open ("battery.json", "w")
    batterydict = dict()
    i = 0
    
    for fullurl in open("list.txt"):
        
        fullurl = fullurl.rstrip()
        
        try:
            url = fullurl[fullurl.find("cnmo.com") + 8:]
            
            print "Get[%d]: %s" % (i,url)
            i += 1
            
            savefilename = "phonefiles/%s.html" % url.split("/")[2]
            content = ""
            if os.path.exists(savefilename):
                content = open(savefilename,"r").read()
            else:
                httpconn.request("GET", url)
                response = httpconn.getresponse()
                content = response.read()
            
                savefile = open(savefilename,"w")
                savefile.write(content)
                savefile.close()
            
            model = ""
            fullmodel = ""
            battery = 0
            
            for line in content.split("\n"):
                
                try:
                    line = line.decode("gbk")
                except Exception as e:
                    continue
                
                pos = line.find("详细参数".decode("gbk"))
                if pos != -1 and len(model) == 0:
                        model = line[line.find("<strong>") + 8 : pos]
                        fullmodel = model
                        model = filter(lambda x: x in string.printable, model)
                        if len(model) == 0:
                            model = line[line.find("<strong>") + 8 : pos]
                        model = model.replace("()", "")
                        model = re.sub(r"\(.*\)", "", model)
                        model = model.strip()
                        if len(model) == 1:
                            model = ""
                
                pos = line.find("mAh")
                if pos >=5 and battery == 0:
                    battery = int(filter(lambda x: x in string.digits, line[pos-5:pos]))
                    
            if len(model) == 0 or battery == 0:
                raise RuntimeError('Not found')
            
            for zh_name in model_replacing_table:
                if fullmodel.find(zh_name) != -1:
                    model = model_replacing_table[zh_name] + model
                    fullmodel = string.replace(fullmodel, zh_name, model_replacing_table[zh_name],1)
                    break
            
            model = filter(lambda x: not (x in string.whitespace), model)
            model = model.lower()
            batterycsv.write("%s, %d, %s\n" % (model, battery, fullmodel))
            batterydict[model] = battery
            
        except Exception as e:
            errfile = open("errors.txt", "a")
            errfile.write(fullurl+"\n")
            errfile.write(traceback.format_exc())
            errfile.close()
            
    batterycsv.close()
    batteryjson.write(json.dumps({"type":batterydict}))
    batteryjson.close()
    httpconn.close()

def convert_vendor():
    out = open("D:/workspace/data/batterycapacity/batterycapacity.ini", 'w')
    in_file = open("D:/workspace/data/batterycapacity/battery_newer.csv")
    for line in in_file:
        csv = line.decode("GBK").rstrip().strip().split(",")
        if len(csv) < 3:
            continue
        for key in model_replacing_table: 
            if key.lower() in csv[0].lower() and not model_replacing_table[key] in csv[1].lower():
                csv[1] = model_replacing_table[key] + csv[1]
        for key in model_replacing_table2: 
            if key.lower() in csv[0].lower() and not model_replacing_table2[key] in csv[1].lower():
                csv[1] = model_replacing_table2[key] + csv[1]
        out.write("%s,%s\n" % (csv[1], csv[2]))
                   
if __name__ == "__main__":
    #crawl_list()
    #crawl_phoneinfo()
    convert_vendor()
