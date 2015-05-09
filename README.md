cudeso-honeypot
===============

## Low interaction honeypot

Setup documentation for a number of low interaction honeypots

* dionaea
* kippo
* glastopf
* conpot

## SSHD Configuration

The kippo honeypot takes connections on tcp/22 (and tcp/2222). Change the listening port of the SSH daemon.
In
```
/etc/ssh/sshd_config 
```
Change the Port setting to
```
Port 8822
```
Restart the SSD daemon.