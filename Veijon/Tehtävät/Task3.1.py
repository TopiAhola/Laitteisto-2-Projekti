from machine import UART, Pin, I2C, Timer, ADC, PWM
from ssd1306 import SSD1306_I2C
from fifo import Fifo

import time

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
LED = PWM(Pin(22), freq = 1000, duty_u16 = 0)

enc1 = Encoder(rota, rotb)

LED_on = False
LED_Brightness = 0
rot_push_on = False

def handling(rot):
    global rot_push_on
    rot_push_on = True
    
rot_push.irq(handler=handling, trigger=Pin.IRQ_RISING, hard=True)

while True:
    LED.duty_u16(LED_Brightness)
    if rot_push_on and LED_on == False:
        LED_on = True
        
    elif rot_push_on and LED_on == True:
        LED_on = False
        LED_Brightness = 0
    
    if enc1.fifo.has_data():
        enc1_input = enc1.fifo.get()
        
        if LED_on == True and enc1_input == 1 and LED_Brightness < 65535:
            LED_Brightness = LED_Brightness + 100
        elif LED_on == True and enc1_input == -1 and LED_Brightness > 0:
            LED_Brightness = LED_Brightness - 100
            
    rot_push_on = False
    time.sleep(0.01)

