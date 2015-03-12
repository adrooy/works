__author__ = 'zz'
# coding=utf-8
import urllib2, json, time, hashlib, errno, urllib

import MySQLdb


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
        print("Error " + str(e))
        '''
        if e.errno == errno.ECONNRESET:
            #reset by WDJ
            time.sleep(10)
            return getAppInfo(package_name)
        elif e.errno == 403:
            #exceeds limitation
            print("Error: exceed WDJ's limitation, retry after 1 hour...")
            time.sleep(3600)
            return getAppInfo(package_name)
        else:
            return "Error"
        #may not found here
        '''
        return "Error"
    result = ret.read()
    return json.loads(result)

if __name__ == '__main__':

    db_host = "192.168.1.15"
    db_user = "root"
    db_passwd = "!LBE_Privacy#"
    db_name = "permission"

    print("get app info from WanDouJia")
    sql_str = "select id, package_name from permission_suggest where id =1847"
    my = MySQL(db_host, db_user, db_passwd, db_name)
    my.cur.execute(sql_str)
    while True:
        row = my.cur.fetchone()
        if row is None:
            break

        try:
            app = getAppInfo(row[1])
            # time.sleep(10)
        except ValueError:
            print("No such package_name found in WDJ: "+row[1])
            continue
        if app == "Error":
            print("Get app info error: "+row[1])
            continue

        md5 = app['apks'][0]['signature']
        category = []
        for ctg in app['categories']:
            category.append(ctg['name'])
        category = ",".join(category)
        install_count = app['installedCount']

        sql_str_tmp = "update permission_suggest set md5='"+md5+"', category='"+category+"', install_count="+str(install_count)+" where id="+str(row[0])
        print("Update DB: "+sql_str_tmp)
        my1 = None
        try:
            my1 = MySQL(db_host, db_user, db_passwd, db_name)
            my1.cur.execute(sql_str_tmp)
            my1.con.commit()
        except Exception as e:
            print("Cannot insert this record into DB: " + str(e))
        finally:
            my1.close()
    my.close()