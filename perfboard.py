import digitalio
import board
import time

# ----------------------------------
# ------- Preliminary setup --------
# ----------------------------------

# Raspberry Pi pin definitons
greenLED_pin = board.D20
blueLED_pin = board.D8 
redLED_pin = board.D16
button3_pin = board.D21       
button2_pin = board.D27           
button1_pin = board.D10             

# Raspberry Pi pin Setup:
#blueLED
blueLED = digitalio.DigitalInOut(blueLED_pin)
blueLED.direction = digitalio.Direction.OUTPUT
blueLED.value = False

#greenled
greenLED = digitalio.DigitalInOut(greenLED_pin)
greenLED.direction = digitalio.Direction.OUTPUT
greenLED.value = True

#redLED
redLED = digitalio.DigitalInOut(redLED_pin)
redLED.direction = digitalio.Direction.OUTPUT
redLED.value = False

button1 = digitalio.DigitalInOut(button1_pin)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.DOWN

button2 = digitalio.DigitalInOut(button2_pin)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.DOWN

button3 = digitalio.DigitalInOut(button3_pin)
button3.direction = digitalio.Direction.INPUT
button3.pull = digitalio.Pull.DOWN



while True:
        blueLED.value = button1.value
        greenLED.value = button2.value
        redLED.value = button3.value
