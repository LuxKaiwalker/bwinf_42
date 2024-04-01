import numpy as np
import sys #eventuell optional

groessen = (5,5)

schulhof = np.full((groessen), 1.0)

def pusten(position, richtung):# richtung: als vektor [a,b] angegeben a=0 oder b=0
    
    def istImHof(feld):
        if feld[0] < groessen[0] and feld[1] < groessen[1]:
            return 1
        else:
            return 0
    
    position = np.add(position, richtung)
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
    
a=1
while a:
    arr1 = np.array([2,1])
    arr2 = np.array([0,1])
    arr1 = np.asarray([eval(i) for i in input("position pls: ").split()])
    arr2 = np.asarray([eval(i) for i in input("richtung pls: ").split()])
    print(arr1, arr2)
    pusten(arr1, arr2)
    print(schulhof)
    if(input("Exit?(Y/n)") == "y"):
        a = 0