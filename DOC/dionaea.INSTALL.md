# Honeypot
Fairly simple low-interaction honeypot setups
 Koen Van Impe

# Dionaea

Dionaea is a low-interaction honeypot that captures attack payloads and malware
p0f is a versatile passive OS fingerprinting tool.

------------------------------------------------------------------------------------------


# Layout

The dionaea and p0f packages are installed from pacakges but the front-end DionaeaFR is installed from source (git) in /opt/DionaeaFR/

# Install dionaea

The install info is partly from http://www.cyberbrian.net/2014/09/install-dionaea-ubuntu-14-04/

## Installation

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install software-properties-common python-software-properties
sudo add-apt-repository ppa:honeynet/nightly
sudo apt-get update
sudo apt-get install p0f
sudo apt-get install dionaea-phibo
```

## Start p0f

P0f can be started from the command line with 
```
sudo p0f -i any -u root -Q /var/run/p0f.sock -q -l
```

Make sure that the socket (-Q) is also accessible by dionaea. Alternatively you can use the init-script in p0f/p0f_init.sh

```
chgrp dionaea /var/run/p0f.sock 
```

## Start dionaea

```
sudo service dionaea-phibo start
```

## Statistics, optionally use gnuplotsql

The gnuplotsql utility is not included in the Ubuntu package but you can get it from the source of dionaea (you might first have to clone the source from dionaea.carnivore.it). The useful modules are in dionaea/modules_python_util

```
sudo apt-get install gnuplot
./gnuplotsql.py -d /var/lib/dionaea/logsql.sqlite  -p smbd -p epmapper -p mssqld -p httpd -p ftpd -D /var/www/html/dionaea-gnuplot/
```

# Configuration

The configuration files are in /etc/dionaea/ and the data files are in /var/lib/dionaea/
Use the config file in this repository **dionaea/dionaea.conf**

## Enable P0f

Enable P0f by uncommenting it in the list of **ihandlers** and set the proper path for the socket in        
```
p0f = {
            path = "un:///var/run/p0f.sock"
        }
```

## Logging

Enable proper logging in the logging = {} section.

## Logrotating

Make sure that you rotate your logs. You can use the **dionaea.logrotate** script for this (make sure you define the correct path).

## SQLITE database scheme

By default dionaea logs to a sqlite file /var/lib/dionaea/logsql.sqlite.

The sqlite logstash module needs an ID-column to keep track of the data.
The patch **logsql.py** adds an ID field and keeps its updated with every dionaea connection.

- Remove the SQLITE database /var/lib/dionaea/logsql.sqlite.
- Apply the patch
- Restart dionaea

## Set dionaea to start at boot

```
update-rc.d dionaea-phibo defaults
```

# Install dionaeaFR

See http://www.vanimpe.eu/2014/07/04/install-dionaeafr-web-frontend-dionaea-ubuntu/

# Start dionaeaFR



# Finishing up

* Create a cronjob for gnuplotsql
* Set dionaeaFR to start at boot


