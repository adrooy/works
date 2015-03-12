import httplib, time, os

f200 = open("200.txt", "w")
f404 = open("404.txt", "w")
fexceptions = open("exceptions.txt", "w")
count = 0

def download(pkgname):
        global f200, f404, count
        count += 1
        if os.path.exists(os.path.join("pages", pkgname)):
                print "%d @ %s: %s: downloaded" % (count, time.asctime(), pkgname)
                f200.write (pkgname + "\n")
                f200.flush()
                return

        if os.path.exists(os.path.join("failedpages", pkgname)):
                print "%d @ %s: %s: not found" % (count, time.asctime(), pkgname)
                f404.write (pkgname + "\n")
                f404.flush()
                return

        httpconn = httplib.HTTPSConnection("play.google.com")
        httpconn.request("GET", "/store/apps/details?id=%s" % pkgname)
        #httpconn = httplib.HTTPConnection("127.0.0.1", 8087)
        #httpconn.request("GET", "https://play.google.com/store/apps/details?id=%s" % pkgname)
        httpresult = httpconn.getresponse()
        if httpresult.status == 200:
                httpdata = httpresult.read()
                f = open ("pages/%s" % pkgname, 'w')
                f.write(httpdata)
                f.close()
                f200.write(pkgname + "\n")
                f200.flush()
        else:
                f = open ("failedpages/%s" % pkgname, 'w')
                f.write(str(httpresult.status))
                f.close()
                f404.write(pkgname + "\n")
                f404.flush()
        httpconn.close()
        print "%d @ %s: %s: %s" % (count, time.asctime(), pkgname, httpresult.status)

        time.sleep(0.1)


pkglist = open("popular_multi_sig_pkg.txt", "r")
print "Start @ %s" % time.asctime()
for pkgname in pkglist:
        pkgname = pkgname.strip().rstrip()
        try:
                download(pkgname)
        except Exception as e:
                fexceptions.write(pkgname + "\n")
                fexceptions.flush()
                print "%d @ %s: %s: exception" % (count, time.asctime(), pkgname)
