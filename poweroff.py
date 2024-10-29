# This is a a code to poweroff the Raspberry Pi when pressing and holding a defined button

# External module imports
import digitalio
import board
import time
import os

# Raspberry Pi pin & variables definitons &
hold_time = 3                   # Hold time in sec to poweroff
button_poweroff_pin = board.D1 

#setups up the button
button_poweroff = digitalio.DigitalInOut(button_poweroff_pin)
button_poweroff.direction = digitalio.Direction.INPUT
button_poweroff.pull = digitalio.Pull.DOWN


while True:
   while not button_poweroff.value:
    start = time.time()
    time.sleep(0.2)     # Switch debounce

    while button_poweroff.value:
        time.sleep(0.01)
    length = time.time() - start

    if length > hold_time:
        os.system("sudo bash -c 'echo ""PowerOff Button pressed"" >> weather_station.log'")
        os.system("sudo poweroff")
