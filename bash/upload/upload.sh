#!/bin/bash
FTP_URL='118.192.170.2:2121';
FTP_USER='iplay';
FTP_PASSW='24iDjfp2velfq';
FTP_LPATH='/iplay';

/usr/bin/lftp $FTP_URL  <<-EOFLTP
	user $FTP_USER $FTP_PASSW
	cd  $FTP_LPATH
	mput -cE /opt/databackup/forum/*.gz
	bye
EOFLTP
