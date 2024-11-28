# Module with all the functions to connect to ThingSpeak in the Cloud

import requests
import logging
from datetime import datetime

def update_thingspeak(first_update, pi_temp, room_temp, room_humidity, cpu_usage, ram_usage, disk_usage):
    # ThingSpeak API key
    writeKey = 'YOURWRITEKEY'     # Enter your own writeKey

    # Thingspeak API connection
    params = {'field1': pi_temp,
              'field2': room_temp,
              'field3': room_humidity,
              'field4': cpu_usage,
              'field5': ram_usage,
              'field6': disk_usage,
              'key': writeKey,
              'format': 'json'}
    try:
        r = requests.get('https://api.thingspeak.com/update', params=params)
        try:
            r.raise_for_status()
            # Update global variable if it's the 1st update
            if first_update is True:
                first_update = False
            last_api_update = datetime.now()
        except requests.exceptions.HTTPError as err:
            logging.error(err)
    except requests.exceptions.ConnectionError as msg:
        logging.error(msg)

    return first_update, last_api_update
