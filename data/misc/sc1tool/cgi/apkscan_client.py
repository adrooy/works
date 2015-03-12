#!/usr/bin/python
import sys
import httplib, urllib

params = urllib.urlencode({'code' : "YOUR_CLIENT_CODE" , \
			   'apkMd5' : "68cb5c68e4681d863cf974d286d4ef80", \
			   'apk' : "sample.apk", \
			   'url' : "http://apk.server.ip.or.FQDN/sample.apk", \
			   'callback' : "http://callback.server.ip.or.FQDN/cgi-bin/apkscan_callback.py"})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
httpconn = httplib.HTTPConnection("sc1.lbesec.com")
httpconn.request("POST", "/scan/apkscan2", params, headers)
response = httpconn.getresponse()
print response.status, response.reason
