#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import datetime
from utils import forum_data_conn, getTimeStamp, getDate


DATE = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
time_stamp = getTimeStamp(DATE)          


@forum_data_conn
def update_topicInfo(db):
#    unreleased = []
#    released = []
    #print DATE
    time_stamp = getTimeStamp(DATE)          
    #print [time_stamp]
    #上线发布
    sql = "UPDATE iplay_topic_info SET enabled=1 WHERE enabled=0 AND topic_date<>0 AND topic_date<=%s" % time_stamp
    db.execute(sql)
    #下线
    sql = "UPDATE iplay_topic_info SET enabled=0 WHERE enabled=1 AND unrelease_date<>0 AND unrelease_date<=%s" % time_stamp
    db.execute(sql)

@forum_data_conn
def update_recommendBanner(db):
    time_stamp = getTimeStamp(DATE)          
    #print [time_stamp]
    sql = "UPDATE iplay_recomend_banner_info SET enabled=1 WHERE enabled=0 AND release_date<>0 AND release_date<=%s" % time_stamp
    db.execute(sql)
    #下线
    sql = "UPDATE iplay_recomend_banner_info SET enabled=0 WHERE enabled=1 AND unrelease_date<>0 AND unrelease_date<=%s" % time_stamp
    db.execute(sql)

@forum_data_conn
def update_recommendGame(db):
    time_stamp = getTimeStamp(DATE)          
    #print [time_stamp]
    sql = "UPDATE iplay_recomend_game SET enabled=1 WHERE enabled=0 AND release_date<>0 AND release_date<=%s" % time_stamp
    db.execute(sql)
    #下线
    sql = "UPDATE iplay_recomend_game SET enabled=0 WHERE enabled=1 AND unrelease_date<>0 AND unrelease_date<=%s" % time_stamp
    db.execute(sql)

@forum_data_conn
def update_categoryGame(db):
    time_stamp = getTimeStamp(DATE)          
    #print [time_stamp]
    sql = "UPDATE iplay_category_game_order_adjust SET enabled=1 WHERE enabled=0 AND release_date<>0 AND release_date<=%s" % time_stamp
    db.execute(sql)
    #下线
    sql = "UPDATE iplay_category_game_order_adjust SET enabled=0 WHERE enabled=1 AND unrelease_date<>0 AND unrelease_date<=%s" % time_stamp
    db.execute(sql)

def release():
    os.system('python /root/operation/step_09_gen_mapping_tables_for_service/09_8_gen_category_to_game_result.py')
    os.system("wget -O - 'http://127.0.0.1:8080/gamecommunity/instruction!clear.action?name=table'")

def main():
    update_topicInfo()
    update_recommendBanner()
    update_recommendGame()
    update_categoryGame()
    release()

if __name__ == '__main__':
    main()
