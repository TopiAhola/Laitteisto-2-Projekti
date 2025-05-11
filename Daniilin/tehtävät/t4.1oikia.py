from filefifo import Filefifo

naytteenottotaajuus = 250  
tiedosto = "capture02_250Hz.txt"

fifo = Filefifo(10, name=tiedosto, repeat=False)
data = []
rivit_luettu = 0  
max_rivit = 5000  


while True:
    if rivit_luettu >= max_rivit:  
        break
    try:
        data.append(fifo.get())  
        rivit_luettu += 1  
    except RuntimeError:
        break  

# Lasketaan näytteiden muutokset
muutokset = [data[i] - data[i - 1] for i in range(1, len(data))]

# Etsitään huiput (positiivinen -> negatiivinen siirtymä)
huiput = []
for i in range(1, len(muutokset)):
    if muutokset[i - 1] > 0 and muutokset[i] < 0:
        huiput.append(i)

# Lasketaan huippujen välit (näytteitä ja sekunteina)
vali_naytteina = [huiput[i] - huiput[i - 1] for i in range(1, len(huiput))]
vali_sekunneissa = [v / naytteenottotaajuus for v in vali_naytteina]


print("Huippujen välit (näytteitä):", vali_naytteina[:3])
print("Huippujen välit (sekunteja):", vali_sekunneissa[:3])

# Lasketaan ja tulostetaan taajuus, jos huippuja on tarpeeks
if len(vali_sekunneissa) > 0:
    keskiarvo_vali = sum(vali_sekunneissa) / len(vali_sekunneissa)
    taajuus = 1 / keskiarvo_vali
    print("Arvioitu taajuus: {:.2f} Hz".format(taajuus))
else:
    print("Ei tarpeeksi huippuja taajuuden laskemiseen.")
