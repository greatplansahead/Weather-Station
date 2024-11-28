import digitalio
import board
import adafruit_dht
import psutil
import socket
from math import pow
from time import sleep

#pin definition
sensor_pin = board.D14

#initialize DHT sensor
sensor = adafruit_dht.DHT11(sensor_pin)

def get_pi_data():
    # Calculate CPU temperature of Raspberry Pi in Degrees C
    pi_temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3  # Get Raspber>
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
       try:
           humid = sensor.humidity
           temp = sensor.temperature
           sleep(3)
           if humid is not None and humid < 100:
               measure = False
       except RuntimeError as e:
           print(f"Error reading DHT11: {e}")
           sleep(2)
    return humid, temp

