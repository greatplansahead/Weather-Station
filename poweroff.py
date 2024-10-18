# This is a a code to poweroff the Raspberry Pi when pressing and holding a defined button

# External module imports
import RPi.GPIO as GPIO
import time
import os

# Raspberry Pi pin & variables definitons &
hold_time = 3                   # Hold time in sec to poweroff
button_poweroff = 1             # Push button to turn off Raspberry Pi
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(button_poweroff, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Button set as input

while True:
    GPIO.wait_for_edge(button_poweroff, GPIO.RISING)
    start = time.time()
    time.sleep(0.2)     # Switch debounce

    while GPIO.input(button_poweroff) == 1:
        time.sleep(0.01)
    length = time.time() - start

    if length > hold_time:
        os.system("sudo bash -c 'echo ""PowerOff Button pressed"" >> weather_station.log'")
        os.system("sudo poweroff")