# Honeypot
Fairly simple low-interaction honeypot setups
 Koen Van Impe

# Glastopf

Glastopf is a Python web application honeypot

------------------------------------------------------------------------------------------

# Install

Install instructions are in the git repository.
 https://github.com/glastopf/glastopf/blob/master/docs/source/installation/installation_ubuntu.rst

```
sudo apt-get install python2.7 python-openssl python-gevent libevent-dev python2.7-dev build-essential make
sudo apt-get install python-chardet python-requests python-sqlalchemy python-lxml
sudo apt-get install python-beautifulsoup mongodb python-pip python-dev python-setuptools
sudo apt-get install g++ git php5 php5-dev liblapack-dev gfortran libmysqlclient-dev
sudo apt-get install libxml2-dev libxslt-dev
sudo pip install --upgrade distribute
```

## Install PHP sandbox

```
cd /opt
sudo git clone git://github.com/glastopf/BFR.git
cd BFR
sudo phpize
sudo ./configure --enable-bfr
sudo make && sudo make install
```

Open the file php.ini (**/etc/php5/apache2/php.ini**) and add
```
zend_extension = /usr/lib/php5/20090626+lfs/bfr.so
```

## Install glastopf

```
cd /opt
sudo git clone https://github.com/glastopf/glastopf.git
cd glastopf
sudo python setup.py install
```

## Error while installing glastopf

If you are doing the install on **Ubuntu 14** and you get an error similar to

```
NameError: name 'sys_platform' is not defined

File "/opt/glastopf/distribute_setup.py", line 123, in _build_egg
    raise IOError('Could not build the egg.')
IOError: Could not build the egg.
```

(see https://github.com/glastopf/glastopf/issues/200#issuecomment-59065414 for the full error message) then you have to remove distribute and reinstall it manually.

```
rm -rf /usr/local/lib/python2.7/dist-packages/distribute-0.7.3-py2.7.egg-info/
rm -rf /usr/local/lib/python2.7/dist-packages/setuptools*
cd /opt
wget https://pypi.python.org/packages/source/d/distribute/distribute-0.6.35.tar.gz
tar -xzvf distribute-0.6.35.tar.gz
cd distribute-0.6.35
sudo python setup.py install
```

# Basic configuration

```
cd /opt
sudo mkdir myhoneypot
cd myhoneypot
sudo glastopf-runner
```

This will create a config file **glastopf.cfg**

## HP-Feeds

By default glastopf has hpfeeds enabled. You can disable it in the [hpfeed] section of glastopf.cfg

## Socket error

If glastopf fails to start 

```
socket.error: [Errno 98] Address already in use: ('0.0.0.0', 80)
```

then maybe Apache is also running? Stop Apache and bind it to a different port.

## Database configuration

Out of the box glastopf will log to a sqlite database. If you prefer mysql then first create a database, set proper permissions and change the setting in the config file.

```
create database glastopf;
mysql> create user 'glastopf'@'localhost' identified by 'glastopf';
mysql> grant all privileges on glastopf.* to 'glastopf'@'localhost';
mysql> flush privileges;
```

Do not worry that the database is empty, without tables. Glastophf will create the necessary tables when it starts.
In glastopf.cfg change this

```
[main-database]
enabled = True
connection_string = mysql://glastopf:glastopf@localhost/glastopf
```