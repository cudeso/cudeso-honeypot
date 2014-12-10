# Honeypot
Fairly simple low-interaction honeypot setups
 Koen Van Impe

# Conpot

Conpot is an ICS honeypot

------------------------------------------------------------------------------------------

# Install 

From http://glastopf.github.io/conpot/installation/ubuntu.html

```
sudo apt-get install libsmi2ldbl snmp-mibs-downloader python-dev libevent-dev libxslt1-dev libxml2-dev
```

If you get an error **E: Package 'snmp-mibs-downloader' has no installation candidate** then you will have to enable multiverse. Do this with **sudo vi /etc/apt/sources.list ; sudo apt-get update** 

```
cd /opt
git clone https://github.com/glastopf/conpot.git
cd conpot
python setup.py install
```

This will install all the necessary packages and install the conpot python package. The python package ends up in a location similar to **/usr/local/lib/python2.7/dist-packages/Conpot-0.3.1-py2.7.egg/**.

# Starting conpot

Conpot needs root privileges (because some services bind to ports below 1024). It drops privileges to nobody/nogroup once started.
You can start the honeypot with 

```
sudo conpot
```

You'll get a list of available templates if you start if with no options

* --template kamstrup_382
** Kamstrup 382 smart meter
** Services 
*** Kamstrup (tcp/1025)
*** Kamstrup (tcp/50100)
* --template proxy
** Demonstrating the proxy feature
** Services 
*** Kamstrup Channel A proxy server (tcp/1025)
*** Kamstrup Channel B proxy server (tcp/1026)
*** SSL proxy (tcp/1234)
*** Kamstrup telnet proxy server (tcp/50100)
* --template default
** Siemens S7-200 CPU with 2 slaves
** Services 
*** Modbus (tcp/502)
*** S7Comm (tcp/102)
*** HTTP (tcp/80)
*** SNMP (udp/161)

If you start conpot with the **-h** option then you get a list of configuration options. The three most useful are

* --template : what template to use
* --config : where is the config file
* --logfile : where to write the logs

The default logging is to a file **conpot.log** in the current directory.

I usually start it with

```
conpot --config /etc/conpot/conpot.cfg --logfile /var/log/conpot/conpot.log --template default
```

# Configuration

The configuration is in the file **conpot.cfg**.

## Services configured for proxy template

By default the proxy template has no http, snmp, etc. service configured.

```
No modbus template found. Service will remain unconfigured/stopped.
No s7comm template found. Service will remain unconfigured/stopped.
No kamstrup_meter template found. Service will remain unconfigured/stopped.
No kamstrup_management template found. Service will remain unconfigured/stopped.
No http template found. Service will remain unconfigured/stopped.
No snmp template found. Service will remain unconfigured/stopped.
```

## Adding a template 

The easiest way for adding a service template is by copying it from an existing one. For example to add the http service template to the proxy template you can merely copy it from the 'default' template.

If you're running conpot from the package then you'll have to reinstall it (sudo python setup.py install).

## Fetching public IP

Sometimes you'll notice outgoing tcp/80 connections when starting conpot. This is because it tries to obtain its public IP. By default the service at telize.com is used. You can change this by altering the configuration setting :

```
[fetch_public_ip]
enabled = True
urls = ["http://www.telize.com/ip", "http://queryip.net/ip/", "http://ifconfig.me/ip"]
```

## Database configuration

### mysql
Out of the box contop will log to a flat file. If you prefer mysql then first create a database, set proper permissions and change the setting in the config file.

```
create database conpot;
mysql> create user 'conpot'@'localhost' identified by 'conpot';
mysql> grant all privileges on conpot.* to 'conpot'@'localhost';
mysql> flush privileges;
```

Do not worry that the database is empty, without tables. conpot will create the necessary tables when it starts.
In conpot.cfg change this

```
[mysql]
enabled = True
device = /tmp/mysql.sock
host = localhost
port = 3306
db = conpot
username = conpot
passphrase = conpot
socket = tcp        ; tcp (sends to host:port), dev (sends to mysql device/socket file)
```

Do not leave out any of the settings. If you are not using sockets you might by tempted to leave out 'device'. This will prevent conpot from starting.

### sqlite

Similarily to mysql, you can also configure sqlite in the configuration file.
Conpot will use the path **logs/conpot.db** for storing the sqlite database (see conpot/core/loggers/sqlite_log.py)

## Other logging features

Conpot can also log / report to syslog and HPFeeds, these are disabled by default.

# Usage

http://glastopf.github.io/conpot/index.html

