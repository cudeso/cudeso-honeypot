#!/usr/bin/env python
#
# Get conpot events from mysql database and print to logfile
#  Uses a temp file to keep track of last printed id
#
# Configuration:
#       Change LAST_CONNECTION_FILE, SQLITE_DB and database connection settings
#       Leave SQLITE_DB empty for mysql-db 
#       Change LOGFILE or leave empty for output to screen
#       Change honeypot-network definitions 
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

LAST_CONNECTION_FILE = "/tmp/conpot-singlelogline.id"
LOGFILE="/var/log/elk-import/conpot-single.log"

SQLITE_DB="/opt/myhoneypot/logs/conpot.db"

DB_USER="conpot"
DB_PASS="conpot"
DB_DB="conpot"
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
        if len(row) == 8:
            skip = 0
        else:
            skip = -1
        connection_id = row[0]
        sensor_id = row[1]
        session_id = row[2 + skip]
        timestamp = row[3 + skip]
        source = row[4 + skip].split(',')
        srcip = source[0][2:-1]
        srcport = source[1][:-1]
        protocol = row[5 + skip]
        request_raw = row[6 + skip].replace('\n', '|').replace('\r', '')
        response = row[7 + skip]
        if LOGFILE:
            f_log.write("%s : %s \t %s \t %s \t %s \t %s \t %s \t '%s' \n" % (timestamp, srcip, srcport, DSTIP, protocol, response, sensor_id, request_raw))
        else:
            print "%s : %s \t %s \t %s \t %s \t %s \t %s  \t '%s' \n" % (timestamp, srcip, srcport, DSTIP, protocol, response, sensor_id, request_raw)
    db.close()
    if LOGFILE:
        f_log.close()

    if not(connection_id and connection_id > 0):
        connection_id = connection_start
    f = open(LAST_CONNECTION_FILE, 'w')
    f.write(str(connection_id))
    f.close()
