#!/usr/bin/env python
#
# Get glastopf events from mysql database and print to logfile
#  Uses a temp file to keep track of last printed id
#
# Configuration:
#       Change LAST_CONNECTION_FILE, SQLITE_DB and database connection settings
#       Leave SQLITE_DB empty for mysql-db 
#       Change LOGFILE or leave empty for output to screen
#       Change honeypot-network definitions (DSTP, DSTPORT, PROTOCOL)
#
# Koen Van Impe
#   koen.vanimpe@cudeso.be      @cudeso         http://www.vanimpe.eu
#   20141210
#

import os
import sys
import datetime
import sqlite3
import MySQLdb

DSTIP="192.168.218.140"
DSTPORT="80"
PROTOCOL="tcp"

LAST_CONNECTION_FILE = "/tmp/glastopf-singlelogline.id"
LOGFILE="/var/log/elk-import/glastopf-single.log"

SQLITE_DB="/opt/myhoneypot/db/glastopf.db"

DB_USER="glastopf"
DB_PASS="glastopf"
DB_DB="glastopf"
DB_HOST="localhost"

connection_start = 0
connection_id = 0

if __name__ == "__main__":

    if os.path.isfile(LAST_CONNECTION_FILE):
        f = open(LAST_CONNECTION_FILE, 'r')
        f_content = f.read()
        f.close()
        if f_content and int(f_content) > 0:
            connection_start = int(f_content)

    if SQLITE_DB:       
        db = sqlite3.connect(SQLITE_DB)
    else:
        db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_DB) 
    cur = db.cursor() 

    if LOGFILE:
        f_log = open(LOGFILE, 'a')
    cur.execute("SELECT * FROM events WHERE id > %s ORDER BY id ASC" % connection_start)
    for row in cur.fetchall() :
        connection_id = row[0]
        timestamp = row[1]
        source = row[2].split(':')
        srcip = source[0]
        srcport = source[1]
        request_url = row[3]
        request_raw = row[4].replace('\n', '|').replace('\r', '')
        request_type = request_raw[0:4].strip()
        if not(request_type == "POST" or request_type == "GET" or request_type == "HEAD"):
            request_type = "Unknown"
        pattern  = row[5]
        filename = row[6]
        if LOGFILE:
            f_log.write("%s : %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t '%s' \n" % (timestamp, srcip, srcport, DSTIP, DSTPORT, PROTOCOL, request_url, pattern, filename, request_type, request_raw))
        else:
            print "%s : %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t %s \t '%s' \n" % (timestamp, srcip, srcport, DSTIP, DSTPORT, PROTOCOL, request_url, pattern, filename, request_type, request_raw)
    db.close()
    if LOGFILE:
        f_log.close()

    if not(connection_id and connection_id > 0):
        connection_id = connection_start
    f = open(LAST_CONNECTION_FILE, 'w')
    f.write(str(connection_id))
    f.close()
