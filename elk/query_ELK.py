#!/usr/bin/python

import urllib2
import json

url="http://192.168.218.140:9200/_search?q=geoip.country_code2:be"

req = urllib2.Request(url)
out = urllib2.urlopen(req)
data = out.read()
print data



{"filtered":{"query":{"bool":{"should":[{"query_string":{"query":"*"}}]}},"filter":{"bool":{"must":[{"range":{"@timestamp":{"from":1418607243883,"to":1419212043883}}}]}}}}