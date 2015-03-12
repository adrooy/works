#!/usr/bin/python
#coding=utf-8
import sys
import cgi
import json
import urllib

RETURN_JSON_STR = "{\"code\":\"%s\", \"ucode\":\"YOUR_UCODE_ID\", \"message\":\"%s\"}"

print "Content-Type: text/html"
print 

form = cgi.FieldStorage()
logf = open("/tmp/apkscan_callback.log", "a")

if "c" not in form or "r" not in form:
	print RETURN_JSON_STR % (-1, "Invalid callback arguments.")
	sys.exit(0)

if form["c"].value != "LBE":
	print RETURN_JSON_STR % (-1, "Invalid caller ID: %s." % form["c"].value)
	sys.exit(0)

try:
	jdata = json.loads(form["r"].value.decode('utf-8'))
	logf.write("Package Name: %s\n" % jdata["packageName"].encode('utf-8'))
	logf.write("Package MD5: %s\n" % jdata["apkMd5"].encode('utf-8'))
	logf.write("Package level: %s\n" % jdata["level"].encode('utf-8'))
	if "description" in jdata:
		jdesc = jdata["description"]
		if "viruses" in jdesc:
			for virus in jdesc["viruses"]:
				logf.write("Virus: name: %s, description: %s\n" % (virus["name"].encode('utf-8'), virus["description"].encode('utf-8')))
		if "adwares" in jdesc:
			for adware in jdesc["adwares"]:
				logf.write("Adware: name: %s, level: %s\n" % (adware["name"].encode('utf-8'), adware["level"].encode('utf-8')))
except:
	print RETURN_JSON_STR % (-1, "Invalid JSON string.")
	logf.write ("JSON Exception!\n")
	logf.write (form["r"].value)
	sys.exit(0)

print RETURN_JSON_STR % (0, "Success.")


