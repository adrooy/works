#! -*- coding:utf-8 -*-


import urllib2
import urllib
import time
import hashlib
import json
#from httplib2 import iri2uri

def checkVersion(package_name):
    reqUrl = "http://api.wandoujia.com/v1/apps/"
    authId = "lbe"
    key = "03ff2ad5a1ea48968bfda5c3c18bf2cf"
    timestamp = int(time.time() * 100)
    timestamp = bytes(timestamp)

    md5 = hashlib.md5()
    md5.update(authId + key + timestamp)
    token = md5.hexdigest()
#    'key': key,

    reqUrl = reqUrl + package_name

    postDict = {
        'id': authId,
        'timestamp': timestamp,
        'token': token
    }


    encodeurl = urllib.urlencode(postDict)
    reqUrl = reqUrl + "?" + encodeurl

    ret = urllib.urlopen(reqUrl)
    code = ret.getcode()


    results = json.loads(ret.read())

    versionCode = str(results['apks'][0]['versionCode'])
#downloadUrl = iri2uri(results['apks'][0]['downloadUrl']['url'])
    downloadUrl = urllib.unquote(results['apks'][0]['downloadUrl']['url'])

    return versionCode, downloadUrl

if __name__ == '__main__':
    package_name = 'MyWork.Baby'

    subprocess.Popen(['python', 'test1.py'])

    version_code, download_url = checkVersion(package_name)

    print [version_code], [download_url]
