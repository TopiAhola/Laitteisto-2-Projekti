# Projekti - Ryhmä 3
## Micropython muistiinpanoja

### Tarvittavat importit
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
from fifo import Fifo

## Raspin IO

### Tactile switches
sw2 = Pin(7, Pin.IN, Pin.PULL_UP)   <br>
sw1 = Pin(8, Pin.IN, Pin.PULL_UP)   <br>
sw0 = Pin(9, Pin.IN, Pin.PULL_UP)   <br> <br>
Nappulan arvon voi lukea näin:     <br>
if sw2.value()==0:                      <br>


### LED
d1 = Pin(22, Pin.OUT)
d2 = Pin(21, Pin.OUT)
d3 = Pin(20, Pin.OUT)
#LED päälle (1) ja pois (0)
d1.value(1)
d1.value(0)


### I2C pinni näyttöä varten    
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)


### PWM luokan LEDit                                               <br>
PWM luokalla voi säätää LEDien kirkkautta välillä 0-65536      <br>
                                                                <br>
PWM LEDit pitää määritellä näin:                        <br>
d1 = PWM(Pin(22), freq = 1000, duty_u16 = 0)            <br>
d2 = PWM(Pin(21), freq = 1000, duty_u16 = 0)            <br>
d3 = PWM(Pin(20), freq = 1000, duty_u16 = 0)            <br>
                                                        <br>
Kirkkauden asettaminen:                         <br>
d1.duty_u16(1000) #asettaa kohtalaisen kirkkauden   <br>
d2.duty_u16(0) #sammuttaa LEDin                     <br>

### Rotary encoder vaatii hardware interruptin Pin.irq - metodin kautta:
Määritellään pinnit:                                    <br>
rot_push = Pin(12, Pin.IN, Pin.PULL_UP)                 <br>
rota = Pin(10, Pin.IN, Pin.PULL_UP) #clock signal       <br>
rotb = Pin(11, Pin.IN, Pin.PULL_UP) #clockwise rot      <br>
Tehdään Encoder luokka jolla on handler-metodi ja pinni-a.irq -attribuutti:

    class Encoder:
        def __init__(self, rota, rotb):
            self.a = rota
            self.b = rotb
            self.fifo = Fifo(30, typecode = 'i')
            self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
    

        def handler(self, pin):
            print("handler called")
            if self.b():
                self.fifo.put(-1)
            else:
                self.fifo.put(1)


<br>encoder1 määritellään Encoder luokkaan:

    encoder1 = Encoder(rota, rotb)

<br>#encoder1 arvo luetaan tämän jälkeen näin:

    encoder1_input =0
    if encoder1.fifo.has_data():
        encoder1_input = encoder1.fifo.get()
        print(encoder1_input)