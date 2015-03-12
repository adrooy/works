#coding: utf-8
# __author__ = 'sunzhennan'

g_pkgname = ""

def set_pkgname(pkgname):
    global g_pkgname
    g_pkgname = pkgname

def write(content):
    f = open(g_pkgname + "/console.log", "a")
    f.write("\n" + content)
    f.close()
