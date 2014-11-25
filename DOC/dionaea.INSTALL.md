# Honeypot
Fairly simple low-interaction honeypot setups
 Koen Van Impe

# Dionaea

------------------------------------------------------------------------------------------


# Layout

The dionaea and p0f packages are installed from .deb
The front-end DionaeaFR is installed from source (git) in /opt/DionaeaFR/

# Install dionaea

Install info partly from http://www.cyberbrian.net/2014/09/install-dionaea-ubuntu-14-04/

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
```
sudo p0f -i any -u root -Q /tmp/p0f.sock -q -l
```
Afterwards, use the init-script provided p0f/

## Start dionaea
```
sudo service dionaea-phibo start
```

## Statistics, optionally use gnuplotsql
The gnuplotsql utility is not included in the .deb. We can get it from the source of dionaea. The useful modules are in dionaea/modules_python_util

```
sudo apt-get install gnuplot
./gnuplotsql.py -d /var/lib/dionaea/logsql.sqlite  -p smbd -p epmapper -p mssqld -p httpd -p ftpd -D /var/www/html/dionaea-gnuplot/
```

# Configuration

The configuration files are in /etc/dionaea/
Data files are in /var/lib/dionaea/

# Install dionaeaFR

See http://www.vanimpe.eu/2014/07/04/install-dionaeafr-web-frontend-dionaea-ubuntu/



# Finishing up

* Rotate the dionaea logs (with **dionaea.logrotate**)
* Create a cronjob for gnuplotsql
* Set dionaea-phibo to start at boot
* Set dionaeaFR to start at boot


