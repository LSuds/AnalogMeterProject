import RPi.GPIO as IO
import time
import socket
import json
from rpi_ws281x import *

#GPIO SETUP
IO.setwarnings(False)
IO.setmode(IO.BCM)

meter_gpio_pins  = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,19,20,21, 22]
meter_vars = {}
IO.setup(meter_gpio_pins, IO.OUT)

for x in range(len(meter_gpio_pins)):
        i = IO.PWM(meter_gpio_pins[x], 100)
        i.start(0)
        meter_vars[str(x)] = i

#LED SETTINGS / SETUP
LED_COUNT      = 40
LED_PIN        = 18
LED_FREQ       = 800000
LED_DMA        = 10
LED_BRIGHTNESS = 250
LED_CHANNEL    = 0

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ, LED_DMA, 0, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

#CLIENT SETUP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(5.0)
addr = ("10.1.44.12", 12000)
message = "Are you there?"

class Payload(object):
        def __init__(self, j):
                self.__dict__ = json.loads(j)

def SetMeterColor(percent, index):
        strip.setPixelColor(index * 2, Color(int(2.55*percent), int(255 - percent * 2.55), 0))
        strip.setPixelColor(index * 2 + 1, Color(int(2.55*percent), int(255 - percent * 2.55), 0))

while(1):
        client_socket.sendto(message, addr)
        try:
                meterCounter = 0
                data, server = client_socket.recvfrom(1024)
                object = Payload(data.decode())
                print(object.Data)
                for x in range(len(object.Data)):
                        meterCounter = x
                        SetMeterColor(object.Data[x], x)
                        meter_vars[str(x)].ChangeDutyCycle(object.Data[x])
                        strip.show()

        except socket.timeout:
                print('REQUEST FAILURE. TIMEOUT')


