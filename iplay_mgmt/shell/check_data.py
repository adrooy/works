#!/usr/bin/python
# -*- coding:utf-8 -*-


import os
import sys
import datetime
from mailsender import Mailsender
from mysql_connection import forum_data_conn


reload(sys)
sys.setdefaultencoding('utf-8')

@forum_data_conn
def get_label_game(db):
    games = {}
    sql = 'SELECT game_id, game_name FROM iplay_game_label_info'
    db.execute(sql)
    for row in db.fetchall():
        game_id = row[0]
        game_name = row[1]
        games[game_id] = game_name
    return games

@forum_data_conn
def get_topics(db):
    topics = {}
    sql = 'SELECT id, name FROM iplay_topic_info'
    db.execute(sql)
    for row in db.fetchall():
        topic_id = int(row[0])
        topic_name = row[1]
        topics[topic_id] = topic_name
    return topics

@forum_data_conn
def get_category(db):
    cats = {}
    sql = 'SELECT id, name FROM iplay_game_category_info WHERE parent_id=0'
    db.execute(sql)
    for row in db.fetchall():
        category_id = row[0]
        category_name = row[1] 
        cats[category_id] = category_name
    categorys = {}
    sql = 'SELECT id, display_name, parent_id FROM iplay_game_category_info'
    db.execute(sql)
    for row in db.fetchall():
        category_id = row[0]
        category_name = row[1]
        parent_id = row[2]
        categorys[category_id] = category_name
        if parent_id:
            categorys[category_id] = cats[parent_id] + '_' + category_name
    return categorys

@forum_data_conn
def get_topic_game(db): 
    sql = 'SELECT iplay_topic_game.game_id, iplay_topic_game.game_name, iplay_topic_game.order_num, iplay_topic_info.name FROM iplay_topic_game JOIN iplay_topic_info ON iplay_topic_game.topic_id = iplay_topic_info.id'
    db.execute(sql)
    topic_games = {}
    for row in db.fetchall():
        game_id = row[0]
        game_name = row[1]
        order_num = row[2]
        topic_name = row[3]
        game = {'game_name': game_name, 'num': order_num, 'topic_name': topic_name}
        topic_games[game_id] = game
    return topic_games

@forum_data_conn
def get_recommend_game(db): 
    sql = 'SELECT game_id, game_name, manual_num FROM iplay_recomend_game'
    db.execute(sql)
    recommend_games = {}
    for row in db.fetchall():
        game_id = row[0]
        game_name = row[1]
        order_num = row[2]
        game = {'game_name': game_name, 'num': order_num, 'game_name': game_name}
        recommend_games[game_id] = game
    return recommend_games

@forum_data_conn
def get_recommend_banner(db):
    banner_topics = {}
    banner_games = {}
    sql = 'SELECT id, game_id, topic_id, order_num, name FROM iplay_recomend_banner_info'
    db.execute(sql)
    for row in db.fetchall():
        banner_id = row[0]
        game_id = row[1]
        topic_id = row[2]
        order_num = row[3]
        name = row[4]
        if game_id:
            game = {'num': order_num, 'banner_name': name}
            banner_games[game_id] = game
        if topic_id:
            topic = {'num': order_num, 'banner_name': name}
            banner_topics[int(topic_id)] = topic
    return banner_games, banner_topics

@forum_data_conn
def get_category_game(db): 
    sql = 'SELECT game_id, game_name, manual_num, category_id FROM iplay_category_game_order_adjust'
    db.execute(sql)
    category_games = {}
    for row in db.fetchall():
        game_id = row[0]
        game_name = row[1]
        order_num = row[2]
        category_id = row[3]
        game = {'game_name': game_name, 'num': order_num, 'game_name': game_name, 'category_id': category_id}
        category_games[game_id] = game
    return category_games

def sendMail(line):
    smtp = 'smtp.163.com'
    sender = 'adrlbe@163.com'
    password = '215481379'
#    receiver = ['xiangxiaowei@mayi.com','zhaiguanglong@mayi.com','zhulantian@mayi.com','yushuyang@ganji.com','fuliang@mayi.com','zhujianxiong@mayi.com','hehaifeng@mayi.com','qulei@mayi.com','zhangwei5@mayi.com', 'niliuyang@mayi.com', 'gongmengyuan@mayi.com','lijinzhi@mayi.com','chenzhihua@mayi.com']
    receiver = ['2495430900@qq.com', 'wangxin@lbesec.com']
    #receiver = ['2495430900@qq.com']
    mail = Mailsender()
    mail.setSmtpServer(smtp)
    mail.setSender(sender,password)
    mail.setReceiver(receiver)
    mail.sendMail(line)  

if __name__ == '__main__':
    categorys = get_category()
    games = get_label_game()
    line = ""
    line2 = ""
    line4 = ""
    print 'category: %d' % len(categorys)
    print  
    print 'games: %d' % len(games)
    print 
    topic_games = get_topic_game()
    print 'topic_game: %d' % len(topic_games)
    for game_id in topic_games:
        if game_id not in games:
            line2 += "                <tr>\n"
            line2 += "                    <td>%s</td>\n" % str(game_id)
            line2 += "                    <td>%s</td>\n" % str(topic_games[game_id]['game_name'])
            line2 += "                    <td>%s</td>\n" % str(topic_games[game_id]['num'])
            line2 += "                    <td>市场专题页: %s专题下的游戏</td>\n" % str(topic_games[game_id]['topic_name']) 
            line2 += "                </tr>\n"
            print game_id, topic_games[game_id]['topic_name'],topic_games[game_id]['game_name'],topic_games[game_id]['num']
    print 
    recommend_games = get_recommend_game()
    print 'recommend_game: %d'  % len(recommend_games)
    for game_id in recommend_games:
        if game_id not in games:
            line2 += "                <tr>\n"
            line2 += "                    <td>%s</td>\n" % str(game_id)
            line2 += "                    <td>%s</td>\n" % str(recommend_games[game_id]['game_name'])
            line2 += "                    <td>%s</td>\n" % str(recommend_games[game_id]['num'])
            line2 += "                    <td>市场推荐页: 游戏列表</td>\n"
            line2 += "                </tr>\n"
            print game_id,recommend_games[game_id]['game_name'],recommend_games[game_id]['num']    
    print 
    category_games = get_category_game()
    print 'category_game: %d' % len(category_games)
    for game_id in category_games:
 #       if game_id not in games: 
            line2 += "                <tr>\n"
            line2 += "                    <td>%s</td>\n" % str(game_id)
            line2 += "                    <td>%s</td>\n" % str(category_games[game_id]['game_name'])
            line2 += "                    <td>%s</td>\n" % str(category_games[game_id]['num'])
            line2 += "                    <td>市场分类页: %s列表</td>\n" % str(categorys[category_games[game_id]['category_id']]) 
            line2 += "                </tr>\n"
            print game_id, category_games[game_id]['game_name'], category_games[game_id]['num'], categorys[category_games[game_id]['category_id']]
    print 
    topics = get_topics()
    print 'topic: %d' % len(topics)
    print 
    banner_games, banner_topics = get_recommend_banner()
    print 'banner_game:%d' % len(banner_games)
    print 'banner_topic:%d' % len(banner_topics)
    for game_id in banner_games:
        if game_id not in games:
            line2 += "                <tr>\n"
            line2 += "                    <td>%s</td>\n" % str(game_id)
            line2 += "                    <td>%s</td>\n" % str(banner_games[game_id]['banner_name'])
            line2 += "                    <td>%s</td>\n" % str(banner_games[game_id]['num'])
            line2 += "                    <td>市场推荐页: banner列表中的游戏</td>\n"
            line2 += "                </tr>\n"
            print game_id, banner_games[game_id]['num'], banner_games[game_id]['banner_name']
    print 
    for topic_id in banner_topics:
        if topic_id not in topics:
            line4 += "                <tr>\n"
            line4 += "                    <td>%s</td>\n" % str(topic_id)
            line4 += "                    <td>%s</td>\n" % str(banner_topics[topic_id]['banner_name'])
            line4 += "                    <td>%s</td>\n" % str(banner_topics[topic_id]['num'])
            line4 += "                    <td>市场推荐页: banner列表中的专题</td>\n"
            line4 += "                </tr>\n"
            print topic_id, banner_topics[topic_id]['num'], banner_topics[topic_id]['banner_name']
    line1 = """
    <div style='margin-left:10%'>
        <table border='1' cellspacing='0' width='80%'> 
            <thead>  
                <tr>
                    <th width='20%'>游戏ID</th>
                    <th width='20%'>游戏名</th>
                    <th width='20%'>排列序号</th>
                    <th width='20%'>类别</th>
                </tr>
            </thead>
            <tbody>
    """
    line3 = """
 
            </tbody>
        </table>
        <table border='1' cellspacing='0' width='80%'> 
            <thead>  
                <tr>
                    <th width='20%'>专题ID</th>
                    <th width='20%'>专题名</th>
                    <th width='20%'>排列序号</th>
                    <th width='20%'>类别</th>
                </tr>
            </thead>
            <tbody>
    """
    line5 = """
            </tbody>
        </table>
    </div>
    """
    line = line1 + line2 + line3 + line4 + line5
    DIR = os.getcwd()
    try:
        with open(os.path.join(DIR, 'templates/market/check.html'), 'w') as files:
            files.write("""
    {% extends 'market/header.html' %}    
    {% block title %}{% endblock %}
    {% block user %}{{ user.last_name }}{{ user.first_name }}{% endblock %}
    {% block content %}

    <div style='height:2%;font-size:25px;margin-top:5%;'>
    <p>失效的游戏和专题</p>
    </div>
    <hr>
            """)
            files.write(line)
            files.write("""
    {% endblock %}
            """)
    except:
        if line2 or line4:
            sendMail(line)
