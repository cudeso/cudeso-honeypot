#!/usr/bin/env python 
#
# Process the 'Inspect' command from Kibana and convert to CSV
#
# Save the 'inspect' window output in the variable 'request_file'
# It will extract the URL and request and return CSV output
# Does not work on histogram ...
#
#  Koen Van Impe on 2014-12-31
#   koen dot vanimpe at cudeso dot be
#   license New BSD : http://www.vanimpe.eu/license
#
#

import requests
import json

request_file = "request.inspect"

# Read the request
f = open( request_file, "r")
request = f.read()
f.close()

# Split URL and request
curl_request = request.split("' -d '")
p = curl_request[0].find("-XGET ")
url = curl_request[0][p+7:]
request = curl_request[1][0:-1]

# Get the response from the Elasticsearch server
response = requests.post(url, data=request)
response_json = json.loads( response.text )

# Print out all the master elements
#for el in response_json:
#   print el

if "facets" in response_json:
    if "terms" in response_json["facets"]:
        terms = response_json["facets"]["terms"]["terms"]
        for t in terms:
            print "%s,%s" % (t["count"], t["term"])

if "hits" in response_json:
    print "Hits"
    if "hits" in response_json["hits"]:
        for h in response_json["hits"]["hits"]:
            print h

# Print the full response
#print response.text