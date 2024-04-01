## Der "einfache alg", verallgemeinert auf gerade Felder

import numpy as np
import sys #eventuell optional

groessen = (11,11)
schulhof = np.full((groessen), 1.0)
schritte = 0

def pusten(position, richtung):# richtung: als vektor [a,b] angegeben a=0 oder b=0
    
    def istImHof(feld):
        if feld[0] < groessen[0] and feld[1] < groessen[1]:
            return 1
        else:
            return 0
    
    position = np.add(position, richtung)
    global schritte
    ziel = np.add(position, richtung)#ziel bestimmt.
    ziel_links = np.add(ziel, [richtung[1], richtung[0]])
    ziel_rechts = np.add(ziel, [richtung[1]*-1, richtung[0]*-1])
    neuesziel = np.add(ziel, richtung)
    
    if istImHof (ziel_links) and istImHof(ziel_rechts):
        schulhof[tuple(neuesziel)] += schulhof[tuple(ziel)]*0.1    
        schulhof[tuple(ziel)] = schulhof[tuple(ziel)]*0.9

    if istImHof(ziel_links) and istImHof(ziel_rechts) and istImHof(ziel):
        schulhof[tuple(ziel_links)] = schulhof[tuple(ziel_links)] + schulhof[tuple(position)]*0.1
        schulhof[tuple(ziel_rechts)] = schulhof[tuple(ziel_rechts)] + schulhof[tuple(position)]*0.1
        schulhof[tuple(ziel)] = schulhof[tuple(ziel)] + schulhof[tuple(position)]*0.8
    schulhof[tuple(position)] = 0.0
    
    print(np.round(schulhof, decimals = 1), "\n")
    schritte += 1


###PUSTEN ZU EINER REIHE(UNGERADE)
for y in range(int(groessen[0]/2)-1):#anzahl der Schritte, die gegangen sein müssen, von oben und unten jeweils
    for x in range(groessen[1]-2):#anzahl der Schritte, die "quer" nötig sind
        print([(y+1)*-1, x+1], [y*-1, x+1])
        pusten(np.array([(y+1)*-1, x+1]), np.array([-1, 0]))
        pusten(np.array([y, x+1]), np.array([1, 0]))

###PUSTEN ZU EINEM FELD(UNGERADE)
for x in range(int(groessen[1]/2)-1):
    pusten([int(groessen[0]/2), x], [0,1])
    pusten([int(groessen[0]/2), (x+1)*-1], [0,-1])

print(f"verwendete Schritte: {schritte}")