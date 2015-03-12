# -*- coding: gbk -*-
import httplib, string, re, json, os, traceback

model_replacing_table = {
                         "����".encode("GBK") : "samsung",
                         "����".encode("GBK") : "lenovo",
                         "����".encode("GBK") : "lenovo",
                         "����".encode("GBK") : "zte",
                         "��Ϊ".encode("GBK") : "huawei",
                         "����".encode("GBK") : "coolpad",
                         "����".encode("GBK") : "meizu",
                         "����".encode("GBK") : "sony",
                         "���ᰮ����".encode("GBK") : "sonyericsson",
                         "С��".encode("GBK") : "xiaomi",
                         "����".encode("GBK") : "k-touch",
                         "Ħ������".encode("GBK") : "motorola",
                         "����".encode("GBK") : "konka",
                         "����".encode("GBK") : "gionee",
                         "����".encode("GBK") : "hisense",
                         "����".encode("GBK") : "sharp",
                         "����".encode("GBK") : "alps",
                         "����".encode("GBK") : "dell",
                         "�ȸ�".encode("GBK") : "google",
                         "��ʿͨ".encode("GBK") : "FUJITSU".lower(),
                         "������".encode("GBK") : "aigo",
                         "�곞".encode("GBK") : "acer",
                         "����".encode("GBK") : "amoi",
                         "HTC" : "htc",
                         "oppo" : "oppo",
                         "lg" : "lge",
                         "Ŧ��".encode("GBK") : "newsmy",
                         "������".encode("GBK") : "BBK",
                         "��ͨ".encode("GBK") : "eton"
                         }

model_replacing_table2 = {
                         "����".encode("GBK") : "yulong"
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
            pos = line.rfind("����".decode("gbk"))
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
                
                pos = line.find("��ϸ����".decode("gbk"))
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
