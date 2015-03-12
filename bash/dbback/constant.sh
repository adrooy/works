#!/bin/bash
# mysql
DEFAULT_MYSQL_HOST='localhost';
DEFAULT_MYSQL_USER='dumper';
DEFAULT_MYSQL_PASSWD='K%8Xaja6$%8dJ.z1%6';

# sql path
DEFAULT_SQL_BASE_PATH='/opt/databackup';

#
YMD_YESTERDAY=`date --date='-1 day' +%Y%m%d`;
YMD_TODAY=`date --date='now' +%Y%m%d`;
YMD_TOMORROW=`date --date='+1 day' +%Y%m%d`;
YMD_LAST_MONTH=`date --date='-1 month' +%Y%m`;
YMD_THIS_MONTH=`date --date='now' +%Y%m`;
YMD_NEXT_MONTH=`date --date='+1 month' +%Y%m`;
