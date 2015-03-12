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


def getAppList(authId, key, page=1, isIncrement=False):
    reqUrl = "http://api.wandoujia.com/v1/allApps.json"
    timestamp = int(time.time() * 100)
    timestamp = bytes(timestamp)
    md5 = hashlib.md5()
    md5.update(authId + key + timestamp)
    token = md5.hexdigest()

    post_dict = {
        'id': authId,
        'timestamp': timestamp,
        'token': token,
        'page': page
    }
    if isIncrement:
        post_dict.setdefault('lastFetch', timestamp)

    reqUrl = reqUrl + "?" + urllib.urlencode(post_dict)
    ret = urllib.urlopen(reqUrl)
    result = ret.read()
    return json.loads(result)


if __name__ == '__main__':

    db_host = "192.168.1.15"
    db_user = "root"
    db_passwd = "!LBE_Privacy#"
    db_name = "permission"

    #table = "permission_suggest"
    my = MySQL(db_host, db_user, db_passwd, db_name)
    if my.con is None:
        print("Cannot connect to DB, please check.")
        sys.exit()
    else:
        my.close()

    auth_id = "lbe"
    auth_key = "03ff2ad5a1ea48968bfda5c3c18bf2cf"
    tmp = getAppList(auth_id, auth_key, 94)
    total_page =  tmp['totalPage']
    for i in range(1, total_page+1):
        print 'start get page '+ str(i)
        apps = {}
        isSuccess = False
        while (not isSuccess):
            try:
                apps = getAppList(auth_id, auth_key, i)
                isSuccess = True
            except:
                print "Connection error, sleep and retry..."
                time.sleep(10)
                continue
        for app in apps['apps']:
            title = app['title']
            package_name = app['packageName']
            version_code = app['apks'][0]['versionCode']
            md5 = app['apks'][0]['signature']
            category = []
            for ctg in app['categories']:
                category.append(ctg['name'])
            category = ",".join(category)
            download_count = app['downloadCount']
            install_count = app['installedCount']
            download_url = app['apks'][0]['downloadUrl']['url']
            #if game, ignore
            if download_url[-4:] == 'GAME':
                continue
            print title, package_name, version_code, md5, category, download_count, install_count, download_url
            if title is None:
                title = ''
            sql_str = "insert into all_app_info (title, package_name, version_code, md5, category, download_url, download_count, install_count) values ('"
            sql_tmp = "', '".join([title, package_name, str(version_code), md5, category, download_url])
            sql_str += sql_tmp + "', " + str(download_count) +", " + str(install_count) + ")"
            print sql_str
            try:
                my = MySQL(db_host, db_user, db_passwd, db_name)
                my.cur.execute(sql_str)
                my.con.commit()
            except Exception as e:
                print("Cannot insert this record into DB: " + str(e))
                continue
            finally:
                my.close()
        # sleep 5 seconds, because WanDouJia limits 500 requests per hour'
        time.sleep(5)