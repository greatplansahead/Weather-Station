# This code will run a weather station that sends the data to ThingSpeak

# External module imports
import digitalio
import board
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
greenLED_pin = board.D20               # Green LED: ON when script is running
blueLED_pin = board.D8                 # Blue LED: ON when weather conditions measured and sent to Thing Speak
button_scriptOFF_pin = board.D21       # Push button to stop the script manually
button_LCD = board.D27                 # Push button to write data on oled screen
button_poweroff_pin = board.D16             # Push button to turn off Raspberry Pi
button_scriptOFF_pressed = False

# Raspberry Pi pin Setup:
#greenled
greenLED = digitalio.DigitalInOut(greenLED_pin)
greenLED.direction = digitalio.Direction.OUTPUT
greenLED.value = True

#blueLED
blueLED = digitalio.DigitalInOut(blueLED_pin)
blueLED.direction = digitalio.Direction.OUTPUT
blueLED.value = False

#scriptbutton
button_scriptOFF = digitalio.DigitalInOut(button_scriptOFF_pin)
button_scriptOFF.direction = digitalio.Direction.INPUT
button_scriptOFF.pull = digitalio.Pull.DOWN

#oledbutton
button_LCD = digitalio.DigitalInOut(button_LCD)
button_LCD.direction = digitalio.Direction.INPUT
button_LCD.pull = digitalio.Pull.DOWN

#poweroffbutton
button_poweroff = digitalio.DigitalInOut(button_poweroff_pin)
button_poweroff.direction = digitalio.Direction.INPUT
button_poweroff.pull = digitalio.Pull.DOWN

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
    
    greenLED.value =  False
    blueLED.value = False
    
    greenLED.deinit()
    blueLED.deinit()
    button_scriptOFF.deinit()
    button_LCD.deinit()
    button_poweroff.deinit()

    logging.info("GPIO cleanup complete.")

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
        while True:
            if not button_scriptOFF.value:
                date_now = datetime.now()
                time_delta = date_now - last_api_update

                # Updating the API only if enabled AND for the laps specified
                if API is True and (time_delta.seconds > api_update_time_laps*60 or first_update):
                    blueLED.value = True
                    display.display_message('Updating ThingSpeak...', False)
                    get_data()
                    first_update, last_api_update = \
                        thingspeak.update_thingspeak(first_update, pi_temp, room_temp, room_humidity,
                                                          cpu_usage, ram_usage, disk_usage)
                    display.display_clear()
                    blueLED.value = False

                if button_LCD.value:
                    blueLED.value = True
                    display.display_message('Measuring...', False)
                    get_data()
                    display.display_weather(room_temp, room_humidity)
                    display.display_config(pi_temp, cpu_usage, RAM_MAX, ram_usage, ram_used)
                    blueLED.value = False

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
        stop_script()


