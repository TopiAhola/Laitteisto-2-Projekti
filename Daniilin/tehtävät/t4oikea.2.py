from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from filefifo import Filefifo
import time

# Näytön asetukset
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# FIFO asetukset
fifo = Filefifo(10, name="capture03_250Hz.txt", repeat=False)
SAMPLES_PER_PIXEL = 5 
DISPLAY_WIDTH = 128


buffer = []

while True:
    # Täytä puskuria tarpeeksi näytteillä
    while len(buffer) < DISPLAY_WIDTH * SAMPLES_PER_PIXEL:
        try:
            buffer.append(fifo.get())
        except RuntimeError:
            break  
    
    if len(buffer) < DISPLAY_WIDTH * SAMPLES_PER_PIXEL:
        break  
    
    # skaalausarvot
    min_val = min(buffer)
    max_val = max(buffer)
    scale = (max_val - min_val) or 1  # Estä jako nollalla näytössä
    
    
    oled.fill(0)
    
    # Piirrä viiva
    prev_y = None
    for x in range(DISPLAY_WIDTH):
        # Laske keskiarvo 5 näytteelle
        start = x * SAMPLES_PER_PIXEL
        end = start + SAMPLES_PER_PIXEL
        avg = sum(buffer[start:end]) / SAMPLES_PER_PIXEL
        
        # Skaalaa arvo näytön korkeudeksi
        y = 63 - int((avg - min_val) * 63 / scale)
        
        oled.pixel(x, y, 1)
        
        # Piirrä viiva edelliseen pisteeseen
        if prev_y is not None:
            oled.line(x-1, prev_y, x, y, 1)
        prev_y = y
    
    oled.show()
    
    # Poista käytetyt näytteet puskurista
    buffer = buffer[DISPLAY_WIDTH * SAMPLES_PER_PIXEL:]
    

    time.sleep(0.01)