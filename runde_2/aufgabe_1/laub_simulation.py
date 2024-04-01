import numpy as np
import random
import sys #eventuell optional

groessen = (5,5)
blaetter = 100
schulhof = np.full((groessen), blaetter)

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
    
    for blatt in range(schulhof[tuple(ziel)]):
        zufall = random.randint(0,9)
        if zufall == 0 and istImHof(neuesziel):
            schulhof[tuple(ziel)] -= 1
            schulhof[tuple(neuesziel)] += 1
        elif 1 <= zufall <= 9:
            pass
        else:
            sys.exit("Fehler im Zahlengenerieren oder blatt außer Hof!")
    for blatt in range(schulhof[tuple(position)]):
        schulhof[tuple(position)] -= 1
        zufall = random.randint(0,9)
        if zufall == 0 and istImHof(ziel_links):
            schulhof[tuple(ziel_links)] += 1
        elif zufall == 1 and istImHof(ziel_rechts):
            schulhof[tuple(ziel_rechts)] += 1
        elif 2 <= zufall <= 9 and istImHof(ziel):#if not out of square +fits into everythng
            schulhof[tuple(ziel)] += 1 #leaf falls there
        else: 
            sys.exit("Fehler im Zahlengenerieren oder blatt außer Hof!")##vielleicht ein return code einbauen?

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