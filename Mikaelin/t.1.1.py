import time
import framebuf
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

#napit
SW_0 = Pin(9, Pin.IN, Pin.PULL_UP) #Oikealle
SW_2 = Pin(7, Pin.IN, Pin.PULL_UP) #Vasemmalle
SW_1 = Pin(8, Pin.IN, Pin.PULL_UP) #Keskitys

#oled
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

#aloituspaikka
x = 50
y = 50

while True:
    if SW_0.value() == 0:
        x += 2
        if x > oled_width - 24: #asetetaan raja
            x = oled_width -24
            
    if SW_2.value() == 0:
        x -= 2
        if x < 0: #asetetaan raja
            x = 0
            
    if SW_1.value() == 0:
        x = 50 #tuo kuvion keskelle
            
    oled.fill(0)
    oled.text('<=>', x, y, 1)
    oled.show()
    
    time.sleep(0.01) #viive