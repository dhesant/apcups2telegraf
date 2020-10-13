#!/usr/bin/env python3
import subprocess
import dateutil.parser as dparser
import pytz

# Key defintions
IGNORE = ["apc", "cable", "driver", "upsmode", "starttime", "end apc"]
TAGS = ["hostname", "upsname", "serialno"]
DATE_PARSE = ["date", "battdate", "xonbatt", "xoffbatt", "laststest"]
FORCE_TEXT = ["version", "serialno", "firmware", "statflag"]


def main():
    status = {}  # Holding Variable

    # Parse output into holding variable
    res = subprocess.getoutput(["/sbin/apcaccess -u"])
    for line in res.split("\n"):
        (key, spl, val) = line.partition(": ")
        key = key.strip().lower()
        val = val.strip()
        if key not in IGNORE:
            if key in DATE_PARSE:
                if not val[0].isdigit():
                    continue
                status[key] = dparser.parse(val)
            elif val[0].isdigit() and key not in FORCE_TEXT:
                status[key] = float(val)
            else:
                if key == "alarmdel":
                    continue
                status[key] = val

    # Generate InfluxDB Line Protocol String
    influx_string = "apcups"

    # Add Influx tags
    for tag in TAGS:
        influx_string = influx_string + "," + tag + "=" + status[tag]

    influx_string = influx_string + " "

    # Add Inflix Measurements
    for key in status:
        if key not in TAGS and key != "date":
            influx_string = influx_string + key + "="
            if type(status[key]) is str:
                influx_string = influx_string + '"' + status[key] + '"'
            elif key in DATE_PARSE:
                influx_string = influx_string + str(int(status[key].timestamp()))
            else:
                influx_string = influx_string + str(status[key])
            influx_string = influx_string + ","

    influx_string = influx_string[:-1] + " " + str(int(status["date"].timestamp() * 1000000000))

    # print(status)
    print(influx_string)


if __name__ == "__main__":
    main()
