# Honeypot
Fairly simple low-interaction honeypot setups
 Koen Van Impe

# Kippo

Kippo is a medium interaction SSH honeypot designed to log brute force attack.

------------------------------------------------------------------------------------------

# Install kippo

Kippo uses a couple of Python libraries. 

```
sudo apt-get install python-openssl python-pyasn1 python-twisted python-mysqldb
```

You can download the latest source from Github.

```
git clone https://github.com/desaster/kippo.git
```

## mysql

Kippo can store the connection attempts in a mysql database. 

Create a mysql database and user for kippo. Generate the tables from **doc/sql/mysql.sql**

# Configuration

The kippo configuration is stored in kippo.cfg. You can copy the config file from **kippo/kippo.cfg**

## Mysql

Enable the mysql configuration by changing the section [database_mysql]. Set the database, hostname, username and password. I don't use mysql in this setup.

## Kippo hostname

The default hostname returned by kippo is svr03. Make sure you change the setting **hostname**.

## SSH Banner
You can define the SSH-banner returned by kippo. It's advisable you change this to make it more difficult for intruders to guess that they are in a honeypot. Do this with the **ssh_version_string** setting.

## Listen on tcp/22

kippo listens on tcp/2222 and should not be run as root. Non-root users can not bind to tcp/22. In order to get incoming SSH connections into kippo you have to add an iptables rule. 192.168.218.141 below is the IP of the interface to which kippo is binded.
```
iptables  -t nat -A PREROUTING -p tcp --dport 22 -d 192.168.218.141 -j REDIRECT --to-port 2222
```

# Start kippo

The kippo startup script is **start.sh** . Check the logs in log/kippo.log 

## Logging

The startup script sets logging to log/kippo.log ; it's better to change this to /var/log/kippo/kippo.log ; make sure that your kippo user has write access.

## Log rotate

Rotate the kippo logs (with **kippo.logrotate**) ; make sure you substitute the username 'kippo' in the logrotate script with your username

# Stop kippo

```
kill `cat kippo.pid`
```

or use the stop.sh script.

# Kippo graphs

Graphs make sense of the data that is stored in the database. You can use kippo-graph for this.

```
sudo apt-get install php5-gd php5-curl
```

```
git clone https://github.com/cudeso/kippo-graph.git
```


## Configuration

The configuration of kippo-graph is in **config.php**. Change the mysql settings to make sure kippo-graph can read its data. 

Do not forget to make sure that the webserver can write to the directory **generated-graphs**.


# Finishing up

