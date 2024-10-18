# This code will run a weather station that sends the data to ThingSpeak

# External module imports
import RPi.GPIO as GPIO
from time import sleep
import logging
import signal
from datetime import datetime
import os
import sensor
import display
import thingspeak

# ----------------------------------
# ------- Preliminary setup --------
# ----------------------------------

# Raspberry Pi pin definitons
greenLED_pin = 20               # Green LED: ON when script is running
blueLED_pin = 8                 # Blue LED: ON when weather conditions measured and sent to Thing Speak
button_scriptOFF_pin = 21       # Push button to stop the script manually
button_LCD = 27                 # Push button to write data on LCD screen
button_poweroff = 1             # Push button to turn off Raspberry Pi
button_scriptOFF_pressed = False

# Raspberry Pi pin Setup:
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(greenLED_pin, GPIO.OUT, initial=1)
GPIO.setup(blueLED_pin, GPIO.OUT, initial=0)
GPIO.setup(button_scriptOFF_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Button set as input
GPIO.setup(button_LCD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Button set as input
GPIO.setup(button_poweroff, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Button set as input

# ThingSpeak API
API = True                      # Enable / disable API connection with ThingSpeak
last_api_update = datetime.now()
api_update_time_laps = 20       # in min, will update only every X min provided
first_update = True

# Logger configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s :: %(levelname)s :: Module %(module)s :: Line No %(lineno)d :: %(message)s',
                    filename='weather_station.log')       # Documents/RaspPiProjects/

# Run variable for kill signal detection
run = True

# ---------------------------------
# ----------- Functions -----------
# ---------------------------------

def stop_script():
    # Function that executes before the script ends
    display.display_message('Script stopped', True, 3)
    GPIO.cleanup()

def handler_term_signal(signum, frame):
    global run
    logging.info('The script was terminated by a kill command')
    stop_script()
    run = False

def get_data():
    # functions to get all data from DHT11 sensor + Raspberry Pi
    global pi_temp
    global cpu_usage
    global RAM_MAX
    global ram_usage
    global ram_used
    global DISK_MAX
    global disk_usage
    global disk_used
    global HOSTNAME
    global room_humidity
    global room_temp
    pi_temp, cpu_usage, RAM_MAX, ram_usage, ram_used, DISK_MAX, disk_usage, disk_used, HOSTNAME = sensor.get_pi_data()
    room_humidity, room_temp = sensor.get_dht11_data()

# ----------------------------
# ----------- Main -----------
# ----------------------------

# Kill term signal handler
signal.signal(signal.SIGTERM, handler_term_signal)

# Data measurement and update ThingSpeak through API
while run and button_scriptOFF_pressed is False:
    logging.info('Script Started')
    try:
        while 1:
            if GPIO.input(button_scriptOFF_pin) == 0:
                date_now = datetime.now()
                time_delta = date_now - last_api_update

                # Updating the API only if enabled AND for the laps specified
                if API is True and (time_delta.seconds > api_update_time_laps*60 or first_update):
                    GPIO.output(blueLED_pin, GPIO.HIGH)
                    display.display_message('Updating ThingSpeak...', False)
                    get_data()
                    first_update, last_api_update = \
                        thingspeak.update_thingspeak(first_update, pi_temp, room_temp, room_humidity,
                                                          cpu_usage, ram_usage, disk_usage)
                    display.display_clear()
                    GPIO.output(blueLED_pin, GPIO.LOW)

                if GPIO.input(button_LCD) == 1:
                    GPIO.output(blueLED_pin, GPIO.HIGH)
                    display.display_message('Measuring...', False)
                    get_data()
                    display.display_weather(room_temp, room_humidity)
                    display.display_config(pi_temp, cpu_usage, RAM_MAX, ram_usage, ram_used)
                    GPIO.output(blueLED_pin, GPIO.LOW)

            else:
                display.display_message('Script stopped', True, 3)
                logging.info('Button ScriptOff pressed, script will stop')
                button_scriptOFF_pressed = True
                break

    except KeyboardInterrupt as err:  # If CTRL+C exit cleanly
        logging.info(err)
        stop_script()

    finally:
        logging.info('Cleaning up in the Finally loop & script stopped')
        GPIO.cleanup()