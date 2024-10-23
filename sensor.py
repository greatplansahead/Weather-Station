# Module with all the functions to measure the data from the DHT11 sensors
# and from the Raspberry Pi operating system.
# It requires  Adafruit_DHT library to be installed prior to using this module.
# Adafruit_DHT web link: https://github.com/adafruit/Adafruit_Python_DHT


import RPi.GPIO as GPIO
import Adafruit_DHT
import psutil
import socket
from math import pow
from time import sleep

# Pin definition
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
sensor_pin = 14


def get_pi_data():
    # Calculate CPU temperature of Raspberry Pi in Degrees C
    pi_temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3  # Get Raspberry Pi CPU Temperature
    # CPU system load in %
    cpu_usage = psutil.getloadavg()[0]
    # RAM usage
    RAM_MAX = psutil.virtual_memory()[0] / 1024 / 1024          # in MB
    ram_usage = psutil.virtual_memory()[2]                      # in %
    ram_used = psutil.virtual_memory()[3] / 1024 / 1024         # in MB
    # Disk space
    DISK_MAX = psutil.disk_usage('/')[0] / 1024 / 1024 / 1024   # in GB
    disk_usage = psutil.disk_usage('/')[3]                      # in %
    disk_used = psutil.disk_usage('/')[1] / 1024 / 1024 / 1024  # in GB
    # Hostname & IP address
    HOSTNAME = socket.gethostname()
    # IP = socket.gethostbyname(HOSTNAME)
    return pi_temp, cpu_usage, RAM_MAX, ram_usage, ram_used, DISK_MAX, disk_usage, disk_used, HOSTNAME

def get_dht11_data():
    measure = True
    while measure:
        humid, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, sensor_pin)    # If different sensor, change the type
        sleep(3)
        if humid is not None:       # Check if measure successful or not
            if humid < 100:         # Basic data check: if humidity level is above 100%, then remeasure
                measure = False
    return humid, temp
