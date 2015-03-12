#-*- coding: utf-8 -*-

import apk, lbedb
import os, traceback, time, sys

g_count = 0
g_processed_count = 0
g_malform_count = 0

PROGRESS_DISPLAY_STEP = 1000

def is_parsed(filename, db, table):
    """ this can not be used for future incremental update, since the filename might be the same
        this should only be used in the init data import
    """
    db.cur.execute("select `file_md5` from %s where `file_name` = '%s';" % (table, os.path.basename(filename)))
    row = db.cur.fetchone()
    return (row is not None)

def add_db(apkf, db, table):
    file_md5 = apkf.file_md5
    file_name = os.path.basename(apkf.filename)
    file_size = apkf.file_size
    package_name = apkf.package or ""
    cert_md5 = apkf.cert_md5 or ""
    cert_text = apkf.cert_text or ""
    sf_md5 = apkf.sf_md5 or ""
    mf_md5 = apkf.mf_md5 or ""
    dex_digest_method = apkf.dex_digest_method or ""
    dex_digest = apkf.dex_digest or ""
    axml_digest_method = apkf.axml_digest_method or ""
    axml_digest = apkf.axml_digest or ""
    arsc_digest_method = apkf.arsc_digest_method or ""
    arsc_digest = apkf.arsc_digest or ""
    version_name = apkf.get_androidversion_name() or ""
    version_code = apkf.get_androidversion_code() and int(apkf.get_androidversion_code()) or 0
    min_sdk_ver = apkf.get_min_sdk_version() and int(apkf.get_min_sdk_version()) or 0
    target_sdk_ver = apkf.get_target_sdk_version() and int(apkf.get_target_sdk_version()) or 0
    permissions = apkf.get_permissions() and "|".join(apkf.get_permissions()) or ""
    activities = apkf.get_activities() and "|".join(apkf.get_activities()) or ""
    services = apkf.get_services() and "|".join(apkf.get_services()) or ""
    receivers = apkf.get_receivers() and "|".join(apkf.get_receivers()) or ""
    providers = apkf.get_providers() and "|".join(apkf.get_providers()) or ""
    libraries = apkf.get_libraries() and "|".join(apkf.get_libraries()) or ""
    intentfilters = apkf.get_intentfilters() and "|".join(apkf.get_intentfilters()) or ""

    sqlstr = u"insert into %s values('%s','%s',%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d,%d,%d,'%s','%s','%s','%s','%s','%s','%s')" % \
                   (\
                    table,\
                    file_md5 ,\
                    file_name ,\
                    file_size ,\
                    package_name ,\
                    cert_md5 ,\
                    cert_text.replace("'", "''") ,\
                    sf_md5 ,\
                    mf_md5 ,\
                    dex_digest_method ,\
                    dex_digest ,\
                    axml_digest_method ,\
                    axml_digest ,\
                    arsc_digest_method ,\
                    arsc_digest ,\
                    version_name ,\
                    version_code ,\
                    min_sdk_ver ,\
                    target_sdk_ver ,\
                    permissions ,\
                    activities ,\
                    services ,\
                    receivers ,\
                    providers ,\
                    libraries ,\
                    intentfilters \
                   )
    if db:
        db.cur.execute(sqlstr)
    else:
        print intentfilters


def parse_folder(folder, db, table, parsed_files):
    global g_malform_count, g_count, g_processed_count

    #print "Start parse folder [%s] @ %s" % (folder, time.asctime())
    sys.stdout.flush()
    flist = os.listdir(folder)
    #print "Done parse folder [%s] @ %s" % (folder, time.asctime())
    sys.stdout.flush()

    for filename in flist:
        full_filename = os.path.join(folder, filename)
        if os.path.isdir(full_filename):
            parse_folder(full_filename, db, table, parsed_files)
            continue
        g_count += 1
        if (g_count % PROGRESS_DISPLAY_STEP) == 0:
            print "%d file parsed @ %s" % (g_count, time.asctime())
            sys.stdout.flush()
        try:
            if not (filename in parsed_files):
                apkf = apk.APK(full_filename)
                add_db(apkf, db, table)
                g_processed_count += 1
                if (g_processed_count % PROGRESS_DISPLAY_STEP) == 0:
                    print "+++ %d file processed @ %s" % (g_processed_count, time.asctime())
                    sys.stdout.flush()

        except Exception as e:
            err_msg = traceback.format_exc().split('\n')[-2]
            errf = open("apkrepo.error.log", "ab")
            errf.write("%s,%s\n" % (full_filename.encode("utf-8"),err_msg))
            g_malform_count += 1
            if (g_malform_count % PROGRESS_DISPLAY_STEP) == 0:
                print "--- %d malformed @ %s" % (g_malform_count, time.asctime())
                sys.stdout.flush()
            continue


def do(folder, db, table, parsed_files):
    parse_folder(folder, db, table, parsed_files)
    print "malform filename count: %d" % g_malform_count
    print "total file count: %d" % g_count
    sys.stdout.flush()

if __name__ == "__main__":
    #open(u"Y:\\yunos_virus\\168彩票官方版-1.apk")
    apkf = apk.APK(u"Y:\\yunos_virus\\500彩票(1).apk")
    add_db(apkf, None, None)