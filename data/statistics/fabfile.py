#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: db_remote_by18.py
Author: limingdong
Date: 2/11/15
Description:
18上运行脚本，同步
lbe_backend_sta_anti_cheat_product_channel
lbe_backend_sta_product_channel
到sc3
"""

import os
import logging
import fabric
from fabric.api import local
from fabric.api import get
from fabric.api import put
from fabric.api import reboot
from fabric.api import run
from fabric.api import task
from fabric.api import roles
from fabric.api import env
from fabric.context_managers import cd, lcd

path = os.path.dirname(__file__)


############################
# log
############################
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

LOGS_DIR = path + '/statistics_sync_db.log'

file_handler = logging.FileHandler(LOGS_DIR)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)-15s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

############################
# db sync
############################

table_anti = "lbe_backend_sta_anti_cheat_product_channel"
table_product = "lbe_backend_sta_product_channel"

dump_sql = """
    mysqldump -h192.168.1.18 --add-locks -ustatistics -pooCjkwP8MXgZ6pZq statistics %(table)s > /tmp/%(table)s.sql
"""
lbe_backend_sta_anti_cheat_product_channel = dump_sql % {"table": table_anti}
lbe_backend_sta_product_channel = dump_sql % {"table": table_product}

# env.user = 'mgmt'
# env.password = ''
# env.hosts = ['122.97.248.19']

env.roledefs = {
    '45': ['root@192.168.1.45'],
    'test': ['localhost'],
    'mgmt': ['mgmt@122.97.248.19'],
}


def dump_db_to_tmp():
    """
    dump数据库文件到/tmp目录下
    """
    try:
        tar_str = "tar -cvzf /tmp/%(name)s.tar.gz -P /tmp/%(name)s.sql"
        local(lbe_backend_sta_anti_cheat_product_channel)
        local(lbe_backend_sta_product_channel)
        local(tar_str % {"name": table_anti})
        local(tar_str % {"name": table_product})
    except Exception as e:
        logger.debug("dump_db_to_tmp : %s ", str(e.args))


@roles('mgmt')
@task
def sync_db_to_sc3():
    # dump db
    dump_db_to_tmp()

    try:

        # pub db file
        put('/tmp/%s.tar.gz' % table_anti, '/tmp/%s.tar.gz' % table_anti)
        put('/tmp/%s.tar.gz' % table_product, '/tmp/%s.tar.gz' % table_product)

        # tar -xvzf db file
        run('chmod 755 /tmp/%s.tar.gz' % table_anti)
        run('chmod 755 /tmp/%s.tar.gz' % table_product)
        run('tar -xvzf /tmp/%s.tar.gz -P /tmp/' % table_anti)
        run('tar -xvzf /tmp/%s.tar.gz -P /tmp/' % table_product)

        # import db file
        import_str = "mysql -h127.0.0.1 -ustatistics -pooCjkwP8MXgZ6pZq statistics < /tmp/%(name)s.sql"
        run(import_str % {"name": table_anti})
        run(import_str % {"name": table_product})

    except Exception as e:
        logger.debug("sync_db_to_sc3 : %s ", str(e.args))

if __name__ == '__main__':
    sync_db_to_sc3()