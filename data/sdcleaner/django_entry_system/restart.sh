#!/bin/bash
echo '---------------------------------------kill---------------------------------------';
ps -ef | grep uwsgi | grep -v 'grep';
echo '----------------------';
ps -ef | grep uwsgi | grep -v 'grep' | awk '{print $2}' | xargs -i kill -9 {};
echo '----------------------';
ps -ef | grep uwsgi | grep -v 'grep';
echo '---------------------------------------kill---------------------------------------';
echo '---------------------------------------start---------------------------------------';
nohup /usr/bin/uwsgi /opt/www/zzdev/django_uwsgi.ini --uid 27 --gid 27 &
ps -ef | grep uwsgi | grep -v 'grep';
echo '---------------------------------------start---------------------------------------';
