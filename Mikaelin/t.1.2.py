import time
import framebuf
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
button = Pin(9, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
OLED_WIDTH = 128
OLED_HEIGHT = 64
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

buffer = bytearray(OLED_WIDTH * OLED_HEIGHT // 8)
fb = framebuf.FrameBuffer(buffer, OLED_WIDTH, OLED_HEIGHT, framebuf.MONO_VLSB)

CHAR_HEIGHT = 8
MAX_LINES = OLED_HEIGHT // CHAR_HEIGHT

lines = []

def draw_text():
    fb.fill(0) #resetoi framebufferin
    for i, line in enumerate(lines):
        fb.text(line, 0, i * CHAR_HEIGHT, 1)
    oled.blit(fb, 0, 0)
    oled.show()
    
while True:
    user_input = input("Enter text: ") #lukee mitä käyttäjä syöttää
    
    if user_input.lower() == "exit": #lopettaa ohjelman
        break
    
    lines.append(user_input) #lisää listaan
    
    #jos rivit menee yli max määrän poistaa vanhimman rivin
    if len(lines) > MAX_LINES:
        lines.pop(0)
        
    draw_text() #päivittää näytön uusimmalla tekstillä