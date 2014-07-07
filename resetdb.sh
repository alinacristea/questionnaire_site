#!/bin/sh
cd /home/alina/PycharmProjects/questionnaire_site
python manage.py sqlclear questionnaire_site | python manage.py dbshell
echo "cleared db"
python manage.py syncdb
echo "syncing db"