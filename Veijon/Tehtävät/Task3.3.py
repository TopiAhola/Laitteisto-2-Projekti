from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from fifo import Fifo
import time

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

#encoder
class Encoder:
    def __init__(self, rota, rotb):
        self.a = rota
        self.b = rotb
        self.fifo = Fifo(30, typecode='i')
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)

    def handler(self, pin):
        if self.b.value():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)

#pins
rota = Pin(10, Pin.IN, Pin.PULL_UP)
rotb = Pin(11, Pin.IN, Pin.PULL_UP)

enc1 = Encoder(rota, rotb)

data = []
try:
    with open("capture_250Hz_01.txt", "r") as file:
        data = [int(line.strip()) for line in file.readlines()[:1000]]
except Exception as e:
    print("Error reading file:", e)

#checks 1000 data
if len(data) < 1000:
    data += [0] * (1000 - len(data)) 

#min & max
min_val = min(data)
max_val = max(data)

#scale for oled
def scale_value(value):
    return int((value - min_val) / (max_val - min_val) * 63) if max_val > min_val else 0

#window
start_idx = 0
window_size = 128
max_idx = len(data) - window_size

#display fun
def update_display():
    oled.fill(0)
    for i in range(window_size):
        oled.pixel(i, 63 - scale_value(data[start_idx + i]), 1)
    oled.show()

update_display()

while True:
    if enc1.fifo.has_data():
        enc1_input = enc1.fifo.get()
        
        #scroll
        if enc1_input == 1:
            start_idx = min(start_idx + 10, max_idx)
        elif enc1_input == -1:
            start_idx = max(start_idx - 10, 0)

        update_display()
    

