import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

#button = Pin(9, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

btn_up = Pin(7, Pin.IN, Pin.PULL_UP) #ylös
btn_clear = Pin(8, Pin.IN, Pin.PULL_UP) #puhdistaa näytön
btn_down = Pin(9, Pin.IN, Pin.PULL_UP) #alas

x = 0
y= 32

while True:
    if btn_up.value() == 0 and y > 0:
        y -= 1
        time.sleep(0.01)
        
    if btn_down.value() == 0 and y < 63:
        y += 1
        time.sleep(0.01)
        
    if btn_clear.value() == 0:
        oled.fill(0)
        x = 0
        y = 32
        oled.show()
        time.sleep(0.01)
        
    oled.pixel(x, y, 1)
    #oled.text('', x, y, 1)
    oled.show()
    
    x += 1
    if x >= 128:
        x = 0
        
    time.sleep(0.01)