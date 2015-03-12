#!/bin/bash
#
CONSTANT_FILE_NAME='./constant.sh';

#
if [ -r $CONSTANT_FILE_NAME ];
then
    . $CONSTANT_FILE_NAME;
else
    exit;
fi

#
function dumpdatabase(){
    databasename=$1;
    sqlfilename=$2;
    if [ -z $databasename ];then
        echo 'databasename is empty';
        exit;
    fi
    if [ -z $sqlfilename ];then
        echo 'sqlfilename is empty';
        exit;
    fi

    mysql_host=$DEFAULT_MYSQL_HOST;
    if [ "$3" != "" ];then
       mysql_host=$3;
    fi
    mysql_user=$DEFAULT_MYSQL_USER;
    if [ "$4" != "" ];then
       mysql_user=$4;
    fi
    mysql_passwd=$DEFAULT_MYSQL_PASSWD;
    if [ "$5" != "" ];then
       mysql_passwd=$5;
    fi

	echo $databasename;
	echo $sqlfilename;
	#echo $mysql_host;
	#echo $mysql_user;
	#echo $mysql_passwd;

    mysqldump -h$mysql_host -u$mysql_user -p$mysql_passwd --add-drop-database --add-drop-table --add-locks $databasename > $sqlfilename;
    if [ $? -eq 0 ]; then
        gzip -f $sqlfilename;
        if [ $? -eq 0 ]; then
            return 0;
        else
            return -2;
        fi
    else
        return -1;
    fi
}

#
function dumptable(){
    databasename=$1;
    tablename=$2;
    sqlfilename=$3;
    if [ -z $databasename ];then
        echo 'databasename is empty';
        exit;
    fi
    if [ -z $tablename ];then
        echo 'tablename is empty';
        exit;
    fi
    if [ -z $sqlfilename ];then
        echo 'sqlfilename is empty';
        exit;
    fi

    mysql_host=$DEFAULT_MYSQL_HOST;
    if [ "$4" != "" ];then
       mysql_host=$4;
    fi
    mysql_user=$DEFAULT_MYSQL_USER;
    if [ "$5" != "" ];then
       mysql_user=$5;
    fi
    mysql_passwd=$DEFAULT_MYSQL_PASSWD;
    if [ "$6" != "" ];then
       mysql_passwd=$6;
    fi

	echo $databasename;
	echo $tablename;
	echo $sqlfilename;
	#echo $mysql_host;
	#echo $mysql_user;
	#echo $mysql_passwd;

    mysqldump -h$mysql_host -u$mysql_user -p$mysql_passwd --add-drop-database --add-drop-table --add-locks $databasename $tablename > $sqlfilename;
    if [ $? -eq 0 ]; then
        gzip -f $sqlfilename;
        if [ $? -eq 0 ]; then
            return 0;
        else
            return -2;
        fi
    else
        return -1;
    fi
}
