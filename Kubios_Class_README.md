# Kubios luokka
### Käytetään Kubios analyysin hakemiseen pilvestä

Pääohjelmassa käytetään näin:


    my_kubios = Kubios() #Objektin määrittely
    my_kubios.connect() #Yhdistää WLANiin, kestää 0-4s tulostaa konsoliin mutta ei palauta virheilmoitusta
    bool = my_kubios.test() #Testaa Kubios-yhteyden testiviestillä. Palauttaa True/False.

Kun halutaan saada analyysi:

    my_kubios.send_request(measurement): 
    my_kubios.check_response(): #Hakee viestin self.response attribuuttiin. Päivittää self.response_bool arvon jos response on saapunut. Palauttaa kyseisen bool arvon.
    my_response = my_kubios.get_response() #Palauttaa responsen ja tyhjentää self.responsen
    print(my_response) #Normaali tulostus

Koska vastauksissa kestää pitää käyttää toistorakenteessa esimerkiksi näin:

    my_kubios.send_request(measurement): 
    while True:
        if my_kubios.check_response():
            my_response = my_kubios.get_response() 
            break
        else:
            time.sleep(1)
    print(my_response) 



Sydänmittaukset mitää muotoilla näin jotta Kubios toimii:   

    measurement = { "id": 666,
                  "type": "PPI",
                    "data": [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 812, 756, 820, 812, 800],
                    "analysis": { "type": "readiness" } }


### Luokan Metodit:

    class Kubios:
        def __init__(self):
            self.response = {} #Kubios response tallennetaan tähän
            self.response_bool = False #Kertoo onko vastausta saatavilla.
            self.mqtt_client = object #Viittaus MQTT luokkaan
            self.wlan = object #Viittaus WLAN luokkaan
    
        def connect(self):
            Yhdistää Picon WLANiin määrittelemällä Kubios.wlan attribuutin.
            Tulostaa konsoliin: "Wlan is connected." tai "Wlan is not connected!"
            Ei palauta mitään.

        def fast_connect_wlan(self):
            Yhdistää vain WLANin. Ei odota tai tarkista yhteyttä.
            Tarkoitus ajaa osana aloituslogoanimaatiota, säästää aikaa.
            Ei palauta mitään.            

        def fast_connect_mqtt(self):
            Yhdistää vain MQTTn. WLAN pitää yhdistää ensin ja odottaa hyvää yhteyttä.
            Tarkoitus ajaa osana aloituslogoanimaatiota, säästää aikaa.
            Ei palauta mitään.
    
        def send_request(self,measurement):
            #Lähettää mittaustuloksen Kubiokseen. Mittaus pitää muotoilla kuten esimerkissä.
            #Ei palauta mitään.
    
        def check_response(self):
            #Hakee viestejä MQTT:n kautta.
            #Tallentaa viestin self.response
            #Palauttaa True tai False jos response on saatavilla.
    
        def get_response(self):
            #Palauttaa responsen,
            # tyhjentää self.response ja asettaa self.response_bool = False
    
        def test(self):
            #Ajaa testin, palauttaa True/False jos yhteys toimii.
    
        def response_callback(self, topic, message):
            # Tätä ei tarvitse käyttää itse.
            # Saves incoming response to self.response. Sets response_bool = True
            # Ei palauta mitään.
