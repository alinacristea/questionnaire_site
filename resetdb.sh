#!/bin/sh
cd /home/alina/Dropbox/questionnaire_site_7thJuly
python manage.py sqlclear questionnaire_site | python manage.py dbshell
echo "cleared db"
python manage.py syncdb
echo "syncing db"
python populate.py
echo "populating"