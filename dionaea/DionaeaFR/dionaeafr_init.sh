#!/bin/bash

# DionaeaFR Startup script

cd /opt/DionaeaFR
#python manage.py collectstatic
python manage.py runserver 0.0.0.0:8000
