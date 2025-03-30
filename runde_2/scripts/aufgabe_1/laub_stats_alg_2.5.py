###Der "schnelle Alg"
#Modifikation im Pusten-Funktion: Input = zwei angeklickte feldern, nicht Input = position+ richtung.

import numpy as np
import sys #eventuell optional

groessen = (11,11)
schulhof = np.full((groessen), 1.0)
schritte = 0

def pusten(position, richtung):# richtung: als vektor [a,b] angegeben a=0 oder b=0
    
    richtung = np.subtract(richtung,position)
    
    def istImHof(feld):
        if feld[0] < groessen[0] and feld[1] < groessen[1]:
            return 1
        else:
            print("irgenwa ist nicht im Hof.")
            print(feld)
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

for i in range(-1, (int(groessen[0]/2)+1)*-1-1, -1):
    print("i+1, groessen[1]-i-2:", i+1, groessen[1]-i-2)
    for j in range(i*-1, groessen[1]-(i*-1)-2):
        print("i,j: ",i,j)
        first_click = [i, j]
        second_click = [i-1, j]
        pusten(np.array(first_click), np.array(second_click))
    for j in range(i*-1, groessen[1]-(i*-1)-2):
        print("i,j: ",i,j)
        first_click = [i, j]
        second_click = [i-1, j]
        pusten(np.array([(first_click[0]+1)*-1, (first_click[1]+1)*-1]), np.array([(second_click[0]+1)*-1, (second_click[1]+1)*-1]))
    for j in range(i*-1, groessen[1]-(i*-1)-2):
        print("i,j: ",i,j)
        first_click = [i, j]
        second_click = [i-1, j]
        pusten([(first_click[1]+1)*-1, first_click[0]], [(second_click[1]+1)*-1, second_click[0]])
    for j in range(i*-1, groessen[1]-(i*-1)-2):
        print("i,j: ",i,j)
        first_click = [i, j]
        second_click = [i-1, j]
        pusten([first_click[1], (first_click[0]+1)*-1], [second_click[1], (second_click[0]+1)*-1])
    
    first_click = [i, groessen[1]-(i*-1)-2]
    second_click = [i-1, groessen[1]-(i*-1)-2]
    pusten(np.array(first_click), np.array(second_click))
    pusten([(first_click[1]+1)*-1, first_click[0]], [(second_click[1]+1)*-1, second_click[0]])
    pusten(np.array([(first_click[0]+1)*-1, (first_click[1]+1)*-1]), np.array([(second_click[0]+1)*-1, (second_click[1]+1)*-1]))
    pusten([first_click[1], (first_click[0]+1)*-1], [second_click[1], (second_click[0]+1)*-1])

    print(np.round(schulhof, decimals = 1), "\n")
    print(f"verwendete Schritte: {schritte}")