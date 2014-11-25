# Honeypot
Fairly simple low-interaction honeypot setups
 Koen Van Impe

# Kippo

------------------------------------------------------------------------------------------

# Install kippo

'''
sudo apt-get install python-openssl python-pyasn1 python-twisted python-mysqldb
'''

'''
git clone https://github.com/desaster/kippo.git
'''

## mysql

Create a mysql database and user for kippo. Generate the tables from **doc/sql/mysql.sql**

# Configuration

* Enable the mysql-setting in the config file
* Change the (hostname) setting
* Change the SSH-banner (ssh_version_string)

## Listen on tcp/22

kippo listens on tcp/2222 and should not be run as root. Non-root users can not bind to tcp/22. In order to get incoming SSH connections into kippo you have to add an iptables rule. 192.168.218.141 below is the IP of the interface to which kippo is binded.
'''
iptables  -t nat -A PREROUTING -p tcp --dport 22 -d 192.168.218.141 -j REDIRECT --to-port 2222
'''

# Start kippo

The kippo startup script is **start.sh** . Check the logs in log/kippo.log 

## Logging

The startup script sets logging to log/kippo.log ; it's better to change this to /var/log/kippo/kippo.log ; make sure that your kippo user has write access.

# Stop kippo

'''
kill `cat kippo.pid`
'''

or use the stop.sh script.

# Finishing up

* Rotate the kippo logs (with **kippo.logrotate**) ; make sure you substitute the username 'kippo' in the logrotate script with your username
