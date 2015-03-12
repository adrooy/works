import sqlite3, MySQLdb, traceback


def dict_factory_for_sqlite(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class LBEDB:
    def commit(self):
        if self.con is not None:
            self.con.commit()

    def close(self):
        if self.cur is not None:
            self.cur.close()
        if self.con is not None:
            self.con.close()

    def __init__(self):
        self.con = None
        self.cur = None


class SQLite(LBEDB):
    def open(self, db_filename):
        try:
            self.con = sqlite3.connect(db_filename)
            self.con.row_factory = dict_factory_for_sqlite
            self.cur = self.con.cursor()
        except Exception:
            print "e"
            self.close()

    def __init__(self, db_filename, ):
        LBEDB.__init__(self)
        self.open(db_filename)


class MySQL(LBEDB):
    def open(self, host, user, passwd):
        try:
            self.con = MySQLdb.connect(host, user, passwd)
            self.con.set_character_set('utf8')
            self.cur = self.con.cursor(MySQLdb.cursors.SSCursor)
        except Exception:
            print traceback.format_exc()
            self.close()


    def __init__(self, host, user, passwd):
        LBEDB.__init__(self)
        self.open(host, user, passwd)


if __name__ == "__main__":
    lite = SQLite(r"D:\workspace\appservice\sdclean\pycgi\db_original\lbecl.db")
    lite.cur.execute("select * from `sub`")
    print "sqlite3 row count test: %d" % len(lite.cur.fetchall())
    lite.close()

    my = MySQL('192.168.1.18', 'root', '!LBE_Privacy#')
    my.cur.execute("select * from `szn1`.`paper_test`")
    print "MySQL row count test: %d" % my.cur.rowcount
    my.close()

