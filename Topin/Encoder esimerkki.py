from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
from fifo import Fifo
import time, random


class Encoder:
    def __init__(self, rota, rotb):
        self.a = rota
        self.b = rotb
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)

    def handler(self, pin):
        print("handler called")
        if self.b():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)

rot_push = Pin(12, Pin.IN, Pin.PULL_UP)
rota = Pin(10, Pin.IN, Pin.PULL_UP)
rotb = Pin(11, Pin.IN, Pin.PULL_UP)

enc1 = Encoder(rota, rotb)

enc1_input =0
if enc1.fifo.has_data():
    enc1_input = enc1.fifo.get()
    print(enc1_input)