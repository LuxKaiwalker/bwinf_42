#"Der alg mit bestem Ergebnis"
#funktioniert aber nur mit den realen blattsimulationen!

import numpy as np
import random
import sys #eventuell optional

groessen = (11,11)
blaetter = 100
schulhof = np.full((groessen), blaetter)
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
    
    for blatt in range(schulhof[tuple(ziel)]):
        zufall = random.randint(0,9)
        if zufall == 0 and istImHof(neuesziel):
        #if True:
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
#    print(schulhof, "\n")
    schritte += 1
    
def fuelle_rand_mit_nullen(array):
    if len(array.shape) != 2 or array.shape[0] != array.shape[1]:
        sys.exit("der Schulhof hat die falsche Dimension")
        
    #fuelle mit nullen auf
    array[:2, :] = 0  #oben
    array[-2:, :] = 0  #unten
    array[:, :2] = 0  #links
    array[:, -2:] = 0  #rechts
    return array

schulhof = fuelle_rand_mit_nullen(schulhof)

print(schulhof)
print("pusten...")
        
###PUSTEN ZU EINER REIHE(UNGERADE)

for y in range(int(groessen[0]/2)-2):#anzahl der Schritte, die gegangen sein müssen, von oben und unten jeweils
    for x in range(groessen[1]-2):#anzahl der Schritte, die "quer" nötig sind
        #print([(y+1)*-1, x+1], [y*-1, x+1])
        while schulhof[(y+3)*-1, x+1]>0:
            #print(schulhof[(y+3)*-1, x+1], (y+3)*-1, x+1)
            pusten(np.array([(y+1)*-1, x+1]), np.array([-1, 0]))#unten pusten
        while schulhof[y+2, x+1]>0:
            #print(schulhof[y+2, x+1], y+2, x+1)
            pusten(np.array([y, x+1]), np.array([1, 0]))#oben pusten


###PUSTEN ZU EINEM FELD(UNGERADE)
for x in range(int(groessen[1]/2)-2):
    while schulhof[int(groessen[0]/2), x+2]>0:
        pusten([int(groessen[0]/2), x], [0,1])
    while schulhof[int(groessen[0]/2), (x+3)*-1]>0:
        pusten([int(groessen[0]/2), (x+1)*-1], [0,-1])
        

print(schulhof)
#print("Anzahl Blätter in der Mitte: ", schulhof[55][55])
print(f"verwendete Schritte: {schritte}")