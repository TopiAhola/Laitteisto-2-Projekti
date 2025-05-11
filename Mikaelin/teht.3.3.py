import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from fifo import Fifo

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

x = 0
y = 0  

# GPIO pins
ENCODER_A_PIN = 10
ENCODER_B_PIN = 11
ENCODER_BUTTON_PIN = 12

# rot encoder pins
encoder_a = Pin(ENCODER_A_PIN, Pin.IN, Pin.PULL_UP)
encoder_b = Pin(ENCODER_B_PIN, Pin.IN, Pin.PULL_UP)

# fifo
encoder_fifo = Fifo(30, typecode='i')

# read 1000 values
data = []
with open('capture_250Hz_01.txt', 'r') as file:
    for line in file:
        if len(data) < 1000:
            data.append(int(line.strip()))
        else:
            break

# min, max values
min_value = min(data)
max_value = max(data)

# variables
last_encoder_a = encoder_a.value()
scroll_position = 0

def encoder_isr(pin):
    global last_encoder_a, scroll_position
    new_encoder_a = encoder_a.value()
    new_encoder_b = encoder_b.value()
    
    if new_encoder_a != last_encoder_a:
        if new_encoder_a == new_encoder_b:
            if scroll_position < len(data) - 128:
                scroll_position += 1
        else:
            if scroll_position > 0:
                scroll_position -= 1
        encoder_fifo.put(scroll_position)
    
    last_encoder_a = new_encoder_a

# interruptit
encoder_a.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=encoder_isr)

def update_display(start_index):
    oled.fill(0)
    for i in range(128):
        if start_index + i < len(data):
            value = data[start_index + i]
            #oled.text(str(value), 0, i * 5)
            oled.pixel(x, y, 0)
    oled.show()

update_display(scroll_position)

# Main loop
while True:
    if encoder_fifo.has_data():
        scroll_position = encoder_fifo.get()
        update_display(scroll_position)
    time.sleep(0.01)

