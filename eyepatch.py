# Gemma IO demo
# Welcome to CircuitPython 5 :)

import usb_hid
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn, AnalogOut
from touchio import TouchIn
import adafruit_dotstar as dotstar
import microcontroller
import board
import time
import busio
import array

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Capacitive touch on A2
touch_in = TouchIn(board.A0)
uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
arr_on = bytes("Y", ascii)
arr_off = bytes("N", ascii)

time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems

######################### HELPERS ##############################

# Helper to convert analog input to voltage

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0:
        return [0, 0, 0]
    if pos > 255:
        return [0, 0, 0]
    if pos < 85:
        return [int(pos * 3), int(255 - (pos * 3)), 0]
    elif pos < 170:
        pos -= 85
        return [int(255 - pos * 3), 0, int(pos * 3)]
    else:
        pos -= 170
        return [0, int(pos * 3), int(255 - pos * 3)]


######################### MAIN LOOP ##############################

i = 0
seen = False
while True:
    # spin internal LED around!
    dot[0] = wheel(i)
    dot.show()
    data = uart.read(32)
    if i % 10 is 0:
        seen = False
    if data is not None:
        seen = True
    # use A0 as capacitive touch to turn on internal LED
    if touch_in.value:
        uart.write(arr_on)
        print(arr_on)
    else:
        uart.write(arr_off)
        print(arr_off)
        # optional! uncomment below & save to have it sent a keypress
        # keyboard.press(Keycode.A)
        # keyboard.release_all()
    # uart.write(seen.encode("utf-8"))
    led.value = seen

    i = (i + 1) % 256  # run from 0 to 255
