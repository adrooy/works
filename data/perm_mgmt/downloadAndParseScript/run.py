__author__ = 'zz'
# coding=utf-8
import os
import time
# import datetime
import urllib
import urllib2
import hashlib
import json
import sys
from httplib2 import iri2uri
import MySQLdb

from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis, ganalysis
from androguard.core import androconf


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


def parseApk(filename, permissions):
    if filename is not None:
        ret_type = androconf.is_android(filename)
        vm = None
        a = None
        if ret_type == 'APK':
            a = apk.APK(filename)
            md5 = a.md5

            if a.is_valid_APK():
                vm = dvm.DalvikVMFormat(a.get_dex())
            else:
                print 'INVALID APK'
                return "Error"
        else:
            print 'INPUT ERROR'
            return "Error"

        vmx = analysis.VMAnalysis(vm)
        gvmx = ganalysis.GVMAnalysis(vmx, a)

        outs = {}

        for and_permission in gvmx.get_and_permissions():
            if and_permission in permissions:
                outs.setdefault(permissions[and_permission])

        result = [md5]
        for lbe_permission in outs:
            result.append(lbe_permission)

        strings = '%s' % ','.join(result)
        return strings


def getCategories(authId, key):
    reqUrl = "http://api.wandoujia.com/v1/categories"
    timestamp = int(time.time() * 100)
    timestamp = bytes(timestamp)
    md5 = hashlib.md5()
    md5.update(authId + key + timestamp)
    token = md5.hexdigest()

    post_dict = {
        'id': authId,
        'timestamp': timestamp,
        'token': token,
        'type': 'APP'
    }

    reqUrl = reqUrl + "?" + urllib.urlencode(post_dict)
    ret = urllib.urlopen(reqUrl)
    result = ret.read()
    return json.loads(result)


def getAppList(tag, authId, key, count_per_category=20):
    reqUrl = "http://api.wandoujia.com/v1/apps"
    timestamp = int(time.time() * 100)
    timestamp = bytes(timestamp)
    md5 = hashlib.md5()
    md5.update(authId + key + timestamp)
    token = md5.hexdigest()
    type='total'

    post_dict = {
        'id': authId,
        'timestamp': timestamp,
        'token': token,
        'tag': tag.encode('utf-8'),
        'type': type,
        'start': 0,
        'max': count_per_category
    }

    reqUrl = reqUrl + "?" + urllib.urlencode(post_dict)
    ret = urllib.urlopen(reqUrl)
    result = ret.read()
    return json.loads(result)


if __name__ == '__main__':
    permissions = {}
    with open("PERMISSIONS") as perm_file:
        for line in perm_file:
            line_info = line.strip('\r\n').split(',')
            lbe_permission = line_info[0]
            and_permission = line_info[1]
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
                   "PERM_ID_AUTOSTART":"perm_autostart_suggest",
                   "PERM_ID_NOTIFICATION":"perm_notification_suggest",
                   "PERM_ID_INSTALL_PACKAGE":"perm_installpackage_suggest",
                   "PERM_ID_AUDIO_RECORDER":"perm_audiorecorder_suggest",
                   "PERM_ID_MMSDB":"perm_mmsdb_suggest",
                   "PERM_ID_SENDMMS":"perm_sendmms_suggest",
                   "PERM_ID_MOBILE_CONNECTIVITY":"perm_mobileconnectivity_suggest",
                   "PERM_ID_WIFI_CONNECTIVITY":"perm_wificonnectivity_suggest",
                   "PERM_ID_BT_CONNECTIVITY":"perm_btconnectivity_suggest"}

    """
    if (len(sys.argv)<5):
        print("Usage: python run.py db_host db_user db_password db_name")
        sys.exit(2)
    db_host = sys.argv[1]
    db_user = sys.argv[2]
    db_passwd = sys.argv[3]
    db_name = sys.argv[4]
    """
    db_host = "localhost"
    db_user = "zz"
    db_passwd = "123qwe"
    db_name = "zzdev"

    #table = "permission_suggest"
    my = MySQL(db_host, db_user, db_passwd, db_name)
    if my.con is None:
        print("Cannot connect to DB, please check.")
        sys.exit()
    else:
        my.close()
    # dirName = os.getcwd()
    # processDate = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    # log_file = os.path.join(dirName, 'log', '%s.log' % processDate)
    # logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.DEBUG)

    #download apk from wandoujia
    auth_id = "lbe"
    auth_key = "03ff2ad5a1ea48968bfda5c3c18bf2cf"
    app_categories = getCategories(auth_id, auth_key)
    for category in app_categories:
        for subCa in category["subCategories"]:
            tag = subCa["name"]
            if not os.path.exists("download/"+tag):
                os.makedirs("download/"+tag)
            apps = getAppList(tag, auth_id, auth_key)
            for app in apps[0]["apps"]:
                package_name = app["packageName"]
                title = app["title"]
                version_code = app["apks"][0]["versionCode"]
                downloadUrl = iri2uri(app["apks"][0]["downloadUrl"]["url"])
                save_path = "download/"+tag+"/"+title+"_"+package_name+"_"+str(version_code)+".apk"
                save_path = os.path.join(os.getcwd(), save_path)
                # save_path = "/home/zz/PycharmProjects/androguard/download/票务/美历_cn.etouch.ecalendar.ladies_11.apk"
                print("Downloading "+title+" "+package_name+"...")

                #urllib.urlretrieve(downloadUrl1, save_path)
                try:
                    f = urllib2.urlopen(downloadUrl, None, 180)
                    data = f.read()
                    with open(save_path, "wb") as code:
                        code.write(data)
                except Exception as e:
                    print(e)
                    print("Cannot download  apk, process next one")
                    continue

                #after download apk, analyze and write into db
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
                print parse_result
                if parse_result == "Error":
                    print("Analyze error, process next one")
                    continue
                parse_result = parse_result.split(",")
                for perm_lbe in parse_result[1:]:
                    for perm_id in perm_dict.keys():
                        if perm_lbe == perm_id:
                            sql_str += ", "+perm_dict[perm_id]+" "
                            perm_number += 1
                sql_tmp = "', '".join([title, package_name, str(version_code), parse_result[0], tag])
                sql_str += ") values ('"+sql_tmp+"'"
                for i in range(0, perm_number):
                    sql_str += ",'?'"
                sql_str += ")"
                print(sql_str)
                print("Insert DB records")
                try:
                    my = MySQL(db_host, db_user, db_passwd, db_name)
                    my.cur.execute(sql_str)
                    my.con.commit()
                except Exception as e:
                    print("Cannot insert this record into DB: " + str(e))
                    continue
                finally:
                    my.close()