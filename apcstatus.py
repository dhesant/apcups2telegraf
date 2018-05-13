#!/usr/bin/python3
import subprocess
import dateutil.parser as dparser
import pytz

# Holding Variable
status = {}

# Key defintions
ignore = ['apc', 'cable', 'driver', 'upsmode', 'starttime', 'end apc']
tags = ['hostname', 'upsname', 'serialno']
date_parse = ['date', 'battdate', 'xonbatt', 'xoffbatt']
force_text = ['version', 'serialno', 'firmware', 'statflag']

# Parse output into holding variable
res = subprocess.getoutput(["/sbin/apcaccess -u"])
for line in res.split("\n"):
    (key,spl,val) = line.partition(': ')
    key = key.strip().lower()
    val = val.strip()
    if key not in ignore:
        if key in date_parse:
            if not val[0].isdigit():
                continue
            status[key] = dparser.parse(val)
        elif val[0].isdigit() and key not in force_text:
            status[key] = float(val)
        else:
            if key == 'alarmdel':
                continue
            status[key] = val

# Generate InfluxDB Line Protocol String        
influx_string = 'apcups'

# Add Influx Tags
for tag in tags:
    influx_string = influx_string + ',' + tag + '=' + status[tag]

influx_string = influx_string + ' '

# Add Inflix Measurements
for key in status:
    if key not in tags and key != 'date':
        influx_string = influx_string + key + '='
        if type(status[key]) is str:
            influx_string = influx_string + '"' + status[key] + '"'
        elif key in date_parse:
            influx_string = influx_string + str(int(status[key].timestamp()))
        else:
            influx_string = influx_string + str(status[key])
        influx_string = influx_string + ','

influx_string = influx_string[:-1] + ' ' + str(int(status['date'].timestamp() * 1000000000))

#print(status)
print(influx_string)
