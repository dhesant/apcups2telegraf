# apcups2telegraf
Read apcupsd status messages into telegraf using InfluxDB line protocol

# Quick start
```
# Install package with pip
python3 -m pip install git+git@github.com:dhesant/apcups2telegraf.git

# Copy and modify telegraf config file
cp telegraf.d/apcups.conf.sample /etc/telegraf/telegraf.d/apcups.conf
```
