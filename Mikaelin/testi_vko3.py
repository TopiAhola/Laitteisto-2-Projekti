from machine import UART, Pin, I2C, Timer, ADC, PWM
from ssd1306 import SSD1306_I2C
from fifo import Fifo
import time

led_on = False
brightness = 0
rot_push_on = False
last_brightness = 0

class Encoder:
    def button_handler(self, pin):
        if self.b.value():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)
            
    def __init__(self, rot_a, rot_b):
        self.a = rot_a
        self.b = rot_b
        self.fifo = Fifo(30, typecode = 'i')
        self.a.irq(handler = self.button_handler, trigger = Pin.IRQ_RISING, hard = True)

rot_push = Pin(12, Pin.IN, Pin.PULL_UP)
rot_a = Pin(10, Pin.IN, Pin.PULL_UP)
rot_b = Pin(11, Pin.IN, Pin.PULL_UP)
LED = PWM(Pin(22), freq = 1000, duty_u16 = 0)
            
rot = Encoder(rot_a, rot_b)

def handling(rotat):
    global rot_push_on
    rot_push_on = True

rot_push.irq(handler=handling, trigger=Pin.IRQ_RISING, hard=True)

# Main loop for software PWM
while True:
    LED.duty_u16(brightness)
    if rot_push_on and led_on == False:
        led_on = True
        #brightness = last_brightness
        
    elif rot_push_on and led_on == True:
        led_on = False
        brightness = 0
        #last_brightness = brightness
        
    if rot.fifo.has_data():
        rot_input = rot.fifo.get()
        
        if led_on == True and rot_input == 1 and brightness < 65535:
            brightness = brightness + 100
        elif led_on == True and rot_input == -1 and brightness > 0:
            brightness = brightness - 100
            
        rot_push_on = False
        time.sleep(0.01)