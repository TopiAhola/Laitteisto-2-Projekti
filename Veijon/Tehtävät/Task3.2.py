from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C
from fifo import Fifo
import time

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

y = 0

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

rot_push = Pin(12, Pin.IN, Pin.PULL_UP)
rota = Pin(10, Pin.IN, Pin.PULL_UP)
rotb = Pin(11, Pin.IN, Pin.PULL_UP)
led1 = PWM(Pin(22), freq=1000, duty_u16=0)
led2 = PWM(Pin(21), freq=1000, duty_u16=0)
led3 = PWM(Pin(20), freq=1000, duty_u16=0)

enc1 = Encoder(rota, rotb)

led1_on = False
led2_on = False
led3_on = False

rot_push_on = False

def handling(rot):
    global rot_push_on
    rot_push_on = True
    
rot_push.irq(handler=handling, trigger=Pin.IRQ_RISING, hard=True)

def menu(number):
    oled.fill(0)
    oled.text("[LED1 - ON]" if led1_on else "[LED1 - OFF]", y, 1) if number == 0 else oled.text(" LED1 - ON " if led1_on else " LED1 - OFF ", y, 1)
    oled.text("[LED2 - ON]" if led2_on else "[LED2 - OFF]", y, 12) if number == 1 else oled.text(" LED2 - ON " if led2_on else " LED2 - OFF ", y, 12)
    oled.text("[LED3 - ON]" if led3_on else "[LED3 - OFF]", y, 24) if number == 2 else oled.text(" LED3 - ON " if led3_on else " LED3 - OFF ", y, 24)
    oled.show()

oled.fill(0)
oled.text("[LED1 - OFF]", y, 1)
oled.text(" LED2 - OFF ", y, 12)
oled.text(" LED3 - OFF ", y, 24)
oled.show()

selection = 0
while True:
    if rot_push_on:
        if selection == 0:
            if led1_on:
                led1.duty_u16(0)
                led1_on = False
            else:
                led1.duty_u16(1000)
                led1_on = True
        elif selection == 1:
            if led2_on:
                led2.duty_u16(0)
                led2_on = False
            else:
                led2.duty_u16(1000)
                led2_on = True
        elif selection == 2:
            if led3_on:
                led3.duty_u16(0)
                led3_on = False
            else:
                led3.duty_u16(1000)
                led3_on = True
    
    if enc1.fifo.has_data():
        enc1_input = enc1.fifo.get()
        
        if enc1_input == 1 and selection < 2:
            selection = selection + 1
        elif enc1_input == -1 and selection > 0:
            selection = selection - 1
            
    rot_push_on = False
    menu(selection)
    time.sleep(0.05)

