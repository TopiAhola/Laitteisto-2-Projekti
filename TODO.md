TODO:

-Raportti pitää tehdä.
-Powerpoint pitää tehdä.



Topi:
Kellonaika lisättävä mittaustuloksiin

Mikael tekee:
pulssimittaus funktiona

Veijo:
2.Button class handler function needs to be rewritten. Button values still need to be read with .get() function



Daniil:
1. Pitää tehdä paikallinen HRV analyysi funktio joka ottaa mittaustuloksen ja muodostaa paikallisen analyysin.:

local analysis: = {
"mean_hr": mean_hr,
"mean_ppi": mean_ppi,
"rmssd": rmssd,
"sdnn": sdnn
}


TEHTY:

-Pulssimittaus ei tyhjennä nappuloiden arvoja joten menu valitsee pullimittauksen 
uudestaan. Pitää laittaa nappuloiden arvojen tyhjennys pulssimenuun mittausfunktion jälkeen. 
