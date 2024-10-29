#with the ssd1306 library from circuit python

import adafruit_ssd1306
import digitalio
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import sleep

WIDTH = 128
HEIGHT = 64
# 128x32 display with hardware I2C:
i2c = board.I2C()
disp = adafruit_ssd1306.SSD1306_128_32(WIDTH, HEIGHT, i2c, addr=0x3C)

#random numbers for testing purposes
pi_temp = 21
cpu_usage = 21
ram_used = 21
RAM_MAX = 21
ram_usage = 21
room_temp = 21
room_humidity = 21
                                       
def display_clear():
    # Initialize library.
    disp.begin()

    # Clear display.
    disp.fill(0)
    disp.show()

def display_message(msg, clear_screen, display_time=10):
    display_clear()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    top = -2
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Load default font.
    font = ImageFont.load_default()

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    draw.text((x, top), str(msg), font=font, fill=255)
    disp.image(image)
    disp.show()

    if clear_screen is True:
        sleep(display_time)

        disp.fill(0)
        disp.display()

def display_weather(room_temp, room_humidity):
    display_clear()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    top = -2
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Load default font.
    font = ImageFont.load_default()

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    draw.text((x, top), "WEATHER CONDITIONS", font=font, fill=255)
    draw.text((x, top + 8), "Temperature: " + str(room_temp) + "degC", font=font, fill=255)
    draw.text((x, top + 16), "Humidity: " + str(room_humidity) + "%", font=font, fill=255)


    # Display image.
    disp.image(image)
    disp.show()

    sleep(10)

    disp.fill(0)
    disp.show()
  

def display_config(pi_temp, cpu_usage, RAM_MAX, ram_usage, ram_used):
    display_clear()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    top = -2
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    # Load default font.
    font = ImageFont.load_default()

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    

    draw.text((x, top), "RASPBERRY PI", font=font, fill=255)
    draw.text((x, top + 8), "Temperature: " + str(int(round(pi_temp))) + "degC", font=font, fill=255)
    draw.text((x, top + 16), "CPU: " + str(cpu_usage) + "%", font=font, fill=255)
    draw.text((x, top + 25), "RAM: " + str(ram_used) + "/" + str(RAM_MAX) + "MB " + str(int(round(ram_usage))) + "%",
              font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()

    sleep(10)

    disp.fill(0)
    disp.show()
