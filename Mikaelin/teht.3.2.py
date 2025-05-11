import time
from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C
from fifo import Fifo

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# GPIO pins
LED_PINS = [22, 21, 20]

# rot GPIO
ENCODER_A_PIN = 10
ENCODER_B_PIN = 11
ENCODER_BUTTON_PIN = 12

# led
leds = [PWM(Pin(pin), freq=1000, duty_u16=0) for pin in LED_PINS]

# menu
menu = ["LED1", "LED2", "LED3"]
selection = 0

class Encoder:
    def __init__(self, rota, rotb, button):
        self.a = rota
        self.b = rotb
        self.button = button
        self.fifo = Fifo(30, typecode='i')
        self.last_button_press_time = 0
        #self.button_pressed = False

        self.a.irq(handler=self.handle_turn, trigger=Pin.IRQ_RISING, hard=True)
        self.button.irq(handler=self.handle_button, trigger=Pin.IRQ_RISING, hard=True)

    def handle_turn(self, pin):
        if self.b.value():
            self.fifo.put(-1)
        else:
            self.fifo.put(1)

    def handle_button(self, pin):
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_button_press_time) > 50:
            #self.button_pressed = True
            self.fifo.put(0)
            self.last_button_press_time = current_time

def update_menu(selection, leds):
    oled.fill(0)
    for i, led in enumerate(leds):
        state = "ON" if led.duty_u16() > 0 else "OFF"
        prefix = "[{} - {}]".format(menu[i], state) if i == selection else " {} - {} ".format(menu[i], state)
        oled.text(prefix, 0, i * 12)
    oled.show()

def toggle_led(led):
    if led.duty_u16() > 0:
        led.duty_u16(0)
    else:
        led.duty_u16(1000)

# encoder
encoder = Encoder(Pin(ENCODER_A_PIN, Pin.IN, Pin.PULL_UP), Pin(ENCODER_B_PIN, Pin.IN, Pin.PULL_UP), Pin(ENCODER_BUTTON_PIN, Pin.IN, Pin.PULL_UP))

# menu display
update_menu(selection, leds)

# Main loop
while True:
    if encoder.fifo.has_data():
        event = encoder.fifo.get()
        if event == 0:
            toggle_led(leds[selection])
        elif event == 1 and selection < len(menu) - 1:
            selection += 1
        elif event == -1 and selection > 0:
            selection -= 1

        update_menu(selection, leds)
    time.sleep(0.05)
