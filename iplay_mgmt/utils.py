#!/usr/bin/python

import time
import MySQLdb

def getTimeStamp(date):
    timeArray = time.strptime(date, '%Y-%m-%d %H:%M:%S')
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

def getDate(timeStamp):
    if timeStamp:
        timeArray = time.localtime(timeStamp)
        date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
    else:
        date = ''
    return date

def forum_data_conn(func):
    def conn(*args, **kwargs):
#        conn = MySQLdb.connect(host='192.168.1.45',port=3306,user='root',passwd='111111',db='forum',charset='utf8')
        conn = MySQLdb.connect(host='192.168.0.1',port=3306,user='forum',passwd='VQq*d@GY4F7J6]MP',db='forum',charset='utf8')
        conn.ping(True)
        db = conn.cursor()
        result = func(db, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return conn

if __name__ == '__main__':
    date =getDate(None)
    print date
