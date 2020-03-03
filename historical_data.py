#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

endpoint = "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&start=2018-01-01T&end=2020-01-01T&candleFormat=midpoint&granularity=D&alignmentTimezone=America%2FChicago"
headers = {"Authorization": "Bearer 86079c3bb756b69e3b9fbf173f91540b-74fb20143539fbc9ae0999e033c7658c"}

data = (requests.get(endpoint, headers=headers).json())
print(data)
data['instrument'] = data['instrument'].lower()
sql = f"drop table if exists {data['instrument']};\n"
sql += f"create table {data['instrument']}(\n"
sql += "time date,\n"
sql += "openMid double precision,\n"
sql += "highMid double precision,\n"
sql += "lowMid double precision,\n"
sql += "closeMid double precision, \n"
sql += "volume int\n"
sql += ");\n"
sql += f"insert into {data['instrument']}(time, openMid, highMid, lowMid, closeMid, volume)\n"
sql += "values"

counter = 1 
for c in data['candles']:
    #  print(c)
    if (counter < len(data['candles'])):
        time = c['time'].split('T')[0]
        sql += f"('{time}', {c['openMid']}, {c['highMid']}, {c['lowMid']}, {c['closeMid']}, {c['volume']}),\n"
        counter += 1
    else:
        sql += f"('{time}', {c['openMid']}, {c['highMid']}, {c['lowMid']}, {c['closeMid']}, {c['volume']});\n"


#  sql += ");"

with open("test.sql", "w") as outfile:
    outfile.write(sql)

