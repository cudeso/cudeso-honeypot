#!/usr/bin/env python
#
# Get dionaea events from sqlite database and print to logfile
#  Uses a temp file to keep track of last printed id
#
# Configuration:
#       Change SQLITE_DB and LAST_CONNECTION_FILE
#       Change LOGFILE or leave empty for output to screen
#
# Koen Van Impe
#   koen.vanimpe@cudeso.be      @cudeso         http://www.vanimpe.eu
#   20141206
#

import os
import sys
import datetime
import sqlite3

SQLITE_DB = "/var/lib/dionaea/logsql.sqlite"
LAST_CONNECTION_FILE = "/tmp/dionaea-singlelogline.id"
LOGFILE="/var/log/elk-import/dionaea-single.log"
IGNORE_SRC=[ "127.0.0.1" ]

connection_start = 0
connection_id = 0

if __name__ == "__main__":

    if os.path.isfile(SQLITE_DB):

        if os.path.isfile(LAST_CONNECTION_FILE):
            f = open(LAST_CONNECTION_FILE, 'r')
            f_content = f.read()
            f.close()
            if f_content and int(f_content) > 0:
                connection_start = int(f_content)

        conn = sqlite3.connect(SQLITE_DB)
        c = conn.cursor()

        if LOGFILE:
            f_log = open(LOGFILE, 'a')
        for row in c.execute("SELECT * FROM connections WHERE connection > %s ORDER BY connection ASC" % connection_start):
            timestamp = datetime.datetime.fromtimestamp(row[4]).strftime('%Y-%m-%d %H:%M:%S')
            connection_type = row[1]
            protocol = row[2]
            connection_protocol = row[3]
            dst_ip = row[7]
            dst_port = row[8]
            src_ip = row[9]
            src_port = row[11]
            hostname = row[10]
            connection_id = row[0]
            if src_ip in IGNORE_SRC:
                continue
            if connection_protocol == "p0fconnection":
                continue                
            if LOGFILE:
                f_log.write("%s : %-10s \t %-10s \t %s \t %s \t %s \t %s \t %s \t %s\n" % (timestamp, connection_type, connection_protocol, protocol, src_ip, src_port, dst_ip, dst_port, hostname))
            else:
                print "%s : %-10s \t %-10s \t %s \t %s \t %s \t %s \t %s \t %s " % (timestamp, connection_type, connection_protocol, protocol, src_ip, src_port, dst_ip, dst_port, hostname)
        conn.close()
        if LOGFILE:
            f_log.close()

        if not(connection_id and connection_id > 0):
            connection_id = connection_start
        f = open(LAST_CONNECTION_FILE, 'w')
        f.write(str(connection_id))
        f.close()
    else:
        print "Sqlite DB not found : %s " % SQLITE_DB
