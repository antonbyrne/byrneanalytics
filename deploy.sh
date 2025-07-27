#!/bin/bash

cd /var/www/byrneanalytics || exit
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
systemctl restart gunicorn

