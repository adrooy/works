__author__ = 'zz'
# coding=utf-8
import os
# import datetime
import urllib2
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


if __name__ == '__main__':

    db_host = "192.168.1.15"
    db_user = "root"
    db_passwd = "!LBE_Privacy#"
    db_name = "permission"

    #download apk from wandoujia
    print("Download top 200 first, 20140610")
    # sql_str = "select title, package_name, version_code, download_url from all_app_info order by download_count desc limit 200"
    sql_str = "select title, package_name, version_code, download_url from all_app_info where title = 'K歌达人'"
    my = MySQL(db_host, db_user, db_passwd, db_name)
    my.cur.execute(sql_str)
    while True:
        row = my.cur.fetchone()
        if row is None:
            break
        file_name = "_&_".join([row[0], row[1], row[2]]) + ".apk"
        print file_name
        # save_path = "app-apk/"+file_name
        save_path = os.path.join(os.getcwd(), "app-apk", file_name)
        # save_path = "app-apk/"+row[0]+"_&_"+row[1]+"_&_"+row[2]+".apk"
        print("Downloading " +file_name)

        #urllib.urlretrieve(downloadUrl1, save_path)
        download_finish = False
        while (not download_finish):
            try:
                f = urllib2.urlopen(row[3], None, 180)
                data = f.read()
                with open(save_path, "wb") as code:
                    code.write(data)
                download_finish = True
            except Exception as e:
                print(e)
                print("Cannot download  apk, try again: "+ file_name +"\n")
    my.close()