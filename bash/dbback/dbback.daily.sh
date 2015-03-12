#!/bin/bash

#
LOG_FILE_NAME='./log/daily.log'

#
FUNCTION_FILE_NAME='./function.sh'

#
if [ -r $FUNCTION_FILE_NAME ];
then
	. $FUNCTION_FILE_NAME;
else
	exit;
fi

###########################################################################################################
# database forum
###########################################################################################################
echo `date`'#################dump database forum' 2>&1 | tee -a $LOG_FILE_NAME;

#
db='forum';
path=$DEFAULT_SQL_BASE_PATH'/'$db;
sql=$path'/'$db'.'$YMD_TODAY'.sql';

#
if [ ! -d  $path ];
then
	mkdir $path;
	if [ $? -ne 0 ];
	then
		exit;
	fi
fi

#
echo '--------------------------start----------------------------' 2>&1 | tee -a $LOG_FILE_NAME;
dumpdatabase $db $sql
echo '--------------------------end------------------------------' 2>&1 | tee -a $LOG_FILE_NAME;

echo '--------------------------start----------------------------' 2>&1 | tee -a $LOG_FILE_NAME;
_PWD=`pwd`;
cd $path;

cp -a /opt/www/forum .;
tar -czvf 'forum''.'$YMD_TODAY'.tar.gz' forum
rm -rf forum;

cp -a /opt/www/iplay_mgmt .;
tar -czvf 'iplay_mgmt''.'$YMD_TODAY'.tar.gz' iplay_mgmt
rm -rf iplay_mgmt;

cp -a /opt/www/python .;
tar -czvf 'python''.'$YMD_TODAY'.tar.gz' python
rm -rf python;

cp -a /opt/lucence .;
tar -czvf 'lucence''.'$YMD_TODAY'.tar.gz' lucence
rm -rf lucence;

cd $_PWD;
echo '--------------------------end------------------------------' 2>&1 | tee -a $LOG_FILE_NAME;
