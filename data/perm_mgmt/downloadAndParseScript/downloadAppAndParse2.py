__author__ = 'zz'
# coding=utf-8
import os
# import datetime
import urllib2, time, hashlib, urllib, json, httplib2
import MySQLdb
import logging, errno
from androguard.core.bytecodes import apk, dvm
from androguard.core import androconf
from androguard.core.analysis import analysis

class MySQL():
    # def open(self, host, user, passwd, db, cursorclass):
    def open(self, host, user, passwd, db):
        try:
            # self.con = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, cursorclass=cursorclass)
            self.con = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
            self.con.set_character_set('utf8')
            self.cur = self.con.cursor()
        except Exception:
            print("Cannot connect to db")
            self.close()

    # def __init__(self, host, user, passwd, db, cursorclass):
    def __init__(self, host, user, passwd, db):
        self.open(host, user, passwd, db)

    def close(self):
        if self.cur is not None:
            self.cur.close()
        if self.con is not None:
            self.con.close()

def getAppInfo(package_name, authId="lbe", key="03ff2ad5a1ea48968bfda5c3c18bf2cf"):
    reqUrl = "http://api.wandoujia.com/v1/apps/"
    timestamp = int(time.time() * 100)
    timestamp = bytes(timestamp)
    md5 = hashlib.md5()
    md5.update(authId + key + timestamp)
    token = md5.hexdigest()

    reqUrl = reqUrl + package_name
    postDict = {
        'id': authId,
        'timestamp': timestamp,
        'token': token
    }

    encodeurl = urllib.urlencode(postDict)
    reqUrl = reqUrl + "?" + encodeurl

    try:
        ret = urllib2.urlopen(reqUrl, None, 180)
    except Exception as e:
        print(str(e))
        if e.errno == errno.ECONNRESET:
            #reset by WDJ
            time.sleep(10)
            return getAppInfo(package_name)
        else:
            return "Error"
        #may not found here
    result = ret.read()
    return json.loads(result)

def parseApk(filename, permissions):
    if filename is not None:
        ret_type = androconf.is_android(filename)
        vm = None
        a = None
        if ret_type == 'APK':
            a = apk.APK(filename)

        outs = {}
        for and_permission in a.get_permissions():
            and_permission = and_permission.rsplit('.', 1)[-1]
            if and_permission in permissions:
                if isinstance(permissions[and_permission], basestring):
                    outs.setdefault(permissions[and_permission])
                elif isinstance(permissions[and_permission], list):
                    for and_perm in permissions[and_permission]:
                        outs.setdefault(and_perm)
        if a.is_valid_APK():
            vm = dvm.DalvikVMFormat(a.get_dex())
        vmx = analysis.VMAnalysis(vm)
        for str in vm.get_strings():
            if "IMAGE_CAPTURE" in str or "VIDEO_CAPTURE" in str:
                outs.setdefault("PERM_ID_RECORDER")
            if "ACTION_CALL" in str or "action.CALL" in str:
                outs.setdefault("PERM_ID_CALLPHONE")

        for and_permission in vmx.get_permissions([]):
            if and_permission in permissions:
                if isinstance(permissions[and_permission], basestring):
                    outs.setdefault(permissions[and_permission])
                elif isinstance(permissions[and_permission], list):
                    for and_perm in permissions[and_permission]:
                        outs.setdefault(and_perm)

        result = []
        for lbe_permission in outs:
            result.append(lbe_permission)

        return result


if __name__ == '__main__':
    # log_file = os.path.join(os.getcwd(), 'another3000.log')
    # logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.DEBUG)
    permissions = {}
    with open("PERMISSIONS") as perm_file:
        for line in perm_file:
            line_info = line.strip('\r\n').split(',')
            lbe_permission = line_info[0]
            and_permission = line_info[1]
            if and_permission in permissions:
                perm_tmp = []
                perm_tmp.append(permissions[and_permission])
                perm_tmp.append(lbe_permission)
                permissions[and_permission] = perm_tmp
            else:
                permissions[and_permission] = lbe_permission
    perm_dict = {"PERM_ID_SENDSMS":"perm_sendsms_suggest",
                   "PERM_ID_CALLPHONE":"perm_callphone_suggest",
                   "PERM_ID_SMSDB":"perm_smsdb_suggest",
                   "PERM_ID_CONTACT":"perm_contact_suggest",
                   "PERM_ID_CALLLOG":"perm_calllog_suggest",
                   "PERM_ID_LOCATION":"perm_location_suggest",
                   "PERM_ID_PHONEINFO":"perm_phoneinfo_suggest",
                   "PERM_ID_NETDEFAULT":"perm_netdefault_suggest",
                   "PERM_ID_NETWIFI":"perm_netwifi_suggest",
                   "PERM_ID_ROOT":"perm_root_suggest",
                   "PERM_ID_CALLSTATE":"perm_callstate_suggest",
                   "PERM_ID_CALLMONITOR":"perm_callmonitor_suggest",
                   "PERM_ID_RECORDER":"perm_recorder_suggest",
                   "PERM_ID_SETTINGS":"perm_settings_suggest",
                   "PERM_ID_AUDIO_RECORDER":"perm_audiorecorder_suggest",
                   "PERM_ID_MMSDB":"perm_mmsdb_suggest",
                   "PERM_ID_SENDMMS":"perm_sendmms_suggest",
                   "PERM_ID_MOBILE_CONNECTIVITY":"perm_mobileconnectivity_suggest",
                   "PERM_ID_WIFI_CONNECTIVITY":"perm_wificonnectivity_suggest",
                   "PERM_ID_BT_CONNECTIVITY":"perm_btconnectivity_suggest",
                   "PERM_ID_NOTIFICATION":"perm_notification_suggest"}

    db_host = "192.168.1.15"
    db_user = "root"
    db_passwd = "!LBE_Privacy#"
    db_name = "permission"

    #download apk from wandoujia
    # sql_str = "select title, package_name, version_code, download_url, category from all_app_info order by download_count desc limit 800 offset 200"
    # when downloading "com.tencen.shoudiantong" 404 error, hanging this program, so kill and restart.
    my = MySQL(db_host, db_user, db_passwd, db_name)
    total_count = 0
    f = open("install_numbers_app.txt")
    #with open("install_numbers_app.txt") as perm_file:
    for line in f:
        if total_count > 3000:
            break
        package_name = line.strip('\r\n')
        sql_str = "select * from permission_suggest where package_name='"+package_name+"'"
        count = my.cur.execute(sql_str)
        if count == 1:
            print("Exist package: "+package_name)
            continue
        try:
            app = getAppInfo(package_name)
        except ValueError:
            print("No such package_name found in WDJ: "+package_name)
            continue
        if app == "Error":
            print("Get app info error: "+package_name)
            continue
        title = app["title"]
        version_code = str(app["apks"][0]["versionCode"])
        download_url = app["apks"][0]["downloadUrl"]["url"]
        if download_url[-4:] == 'GAME':
            print("Ignore game: "+package_name)
            continue
        downloadUrl = httplib2.iri2uri(download_url)
        md5 = app['apks'][0]['signature']
        category = []
        for ctg in app['categories']:
            category.append(ctg['name'])
        category = ",".join(category)
        file_name = "_&_".join([title, package_name, version_code]) + ".apk"
        save_path = os.path.join(os.getcwd(), "app-apk", file_name)
        print("Downloading " + file_name)

        #urllib.urlretrieve(downloadUrl1, save_path)
        download_finish = False
        download_times = 0
        while (not download_finish):
            if download_times > 2:
                print("Cannot download for 3 times, next one.")
                break
            try:
                f = urllib2.urlopen(downloadUrl, None, 180)
                data = f.read()
                with open(save_path, "wb") as code:
                    code.write(data)
                download_finish = True
            except Exception as e:
                print(e)
                print("Cannot download  apk, try again: "+ file_name +"\n")
                download_times += 1
        if not download_finish:
            continue
        print("Analyze apk...")
        sql_str = "insert into permission_suggest (title, package_name, version_code, md5, category"
        perm_number = 0
        parse_result = ""
        try:
            parse_result = parseApk(save_path, permissions)
        except Exception as e:
            print(str(e))
            print("Analyze error, process next one")
            continue
        for perm_lbe in parse_result:
            sql_str += ", "+perm_dict[perm_lbe]+" "
            perm_number += 1
        sql_tmp = "', '".join([title, package_name, version_code, md5, category])
        sql_str += ") values ('"+sql_tmp+"'"
        for i in range(0, perm_number):
            sql_str += ",'?'"
        sql_str += ")"
        print("Insert DB records")
        print(sql_str)
        my1 = None
        try:
            my1 = MySQL(db_host, db_user, db_passwd, db_name)
            my1.cur.execute(sql_str)
            my1.con.commit()
        except Exception as e:
            print("Cannot insert this record into DB: " + str(e))
        finally:
            my1.close()
        total_count += 1
        print(str(total_count))
    my.close()