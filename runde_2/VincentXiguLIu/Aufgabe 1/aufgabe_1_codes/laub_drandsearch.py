###sehr schnelle heuristik, die die Ränder pustet und dann die Mitte pustet.

#wir importieren numpy und random, um die Simulation zu erstellen bzw besser mit vektoren umzugehen
import time
import numpy as np
import random


#Input muss noch abgeändert werden !!!!!!
g = int(input("Bitte eine Zahl für i eingeben: "))
f = int(input("Bitte eine Zahl für j eingeben: "))
s = int(input("bitte eine Zahl für s eingeben: "))
t = int(input("bitte eine Zahl für t eingeben: "))
blaetter = int(input("bitte eine Zahl für die Anzahl der Blätter eingeben: "))

time_start = time.time()
groessen = (f,g)

zielquadrat = [s,t]

schulhof = np.full((groessen), blaetter)

schritte = 0

#die Hausmeister-Pustefunktion. 
#Argumente: Position des Hausmeisters und Richtung des Pustens
#Simuliert das Pusten der Blätter auf dem Schulhof.
def hausmeister_pustet(position, richtung):
    def istImHof(feld):
        if 0 <= feld[0] < groessen[0] and 0<= feld[1] < groessen[1]:
            return 1
        else:
            return 0
    
    #Definieren der in der Doku angegebenen einzelnen Felder:
    pustfeld = np.add(position, richtung)
    ziel = np.add(pustfeld, richtung)
    ziel_links = np.add(ziel, [richtung[1], richtung[0]])
    ziel_rechts = np.add(ziel, [richtung[1]*-1, richtung[0]*-1])
    neuesziel = np.add(ziel, richtung)
    
    if istImHof(pustfeld)==0:#wenn das gegebene Feld sich nicht im Hof befindet...
        print(f"FEHLER!!!: das pustfeld {pustfeld} ist nicht im Hof")#ist ein Fehler aufgetreten
        exit()
    
    if not istImHof(ziel):#wenn das Ziel sich nicht im Schulhof befindet, wird die Hälfte einfahc zur Seite geblasen.
        haelfte_der_blaetter = schulhof[tuple(pustfeld)]
        if istImHof(np.add(pustfeld, [richtung[1], richtung[0]])):#ist das Eine Seitfeld im hof? 
            for i in range(schulhof[tuple(pustfeld)]):
                if not random.randint(0,1):
                    schulhof[tuple(np.add(pustfeld, [richtung[1], richtung[0]]))]+=1
                    schulhof[tuple(pustfeld)]-=1
            if istImHof(np.add(pustfeld, [richtung[1]*-1, richtung[0]*-1])):#Addiere die restlichen Blätter zum anderen Seitenfeld, sofern dieser auch im Hof ist
                schulhof[tuple(np.add(pustfeld, [richtung[1]*-1, richtung[0]*-1]))]+= schulhof[tuple(pustfeld)]
                schulhof[tuple(pustfeld)] = 0
        elif istImHof(np.add(pustfeld, [richtung[1]*-1, richtung[0]*-1])):#ist das andere Seitfeld im hof?
            for i in range(schulhof[tuple(pustfeld)]):
                if random.randint(0,1):
                    schulhof[tuple(np.add(pustfeld, [richtung[1]*-1, richtung[0]*-1]))]+=1
                    schulhof[tuple(pustfeld)]-=1
        return schulhof
    
    if istImHof (neuesziel):#ist das Feld neues ziel im Hof (also das hinterste Feld)? Wenn nicht, puste wie normal die restliche Blätter. Wenn doch:
        for i in range(schulhof[tuple(ziel)]):#für jedes Blatt aus den Feld "ziel"
            if not random.randint(0,9):#wahrscheinlichkeit 10%
                schulhof[tuple(neuesziel)] += 1
                schulhof[tuple(ziel)]-=1

    #Wir simulieren die Blätter auf den Seitenrändern.
    for i in range(schulhof[tuple(pustfeld)]):
        if not random.randint(0,9):#erstelle eine zufallszahl
            if istImHof(ziel_links):#wenn das linke Ziel im Hof ist, dann füge ein Blatt hinzu
                schulhof[tuple(ziel_links)] += 1
                schulhof[tuple(pustfeld)] -= 1
            else:
                pass
        if not random.randint(0,9):#erstelle eine andere zufallszahl
            if istImHof(ziel_rechts):#wenn das rechte Ziel im Hof ist, dann füge ein Blatt hinzu
                schulhof[tuple(ziel_rechts)] += 1
                schulhof[tuple(pustfeld)] -= 1
            else:
                pass

    #wir entfernen die Blätter aus dem Pustfeld und fügen sie dem Ziel hinzu
    schulhof[tuple(ziel)] += schulhof[tuple(pustfeld)]
    schulhof[tuple(pustfeld)] = 0
    
    return#fertig

def pusten(position, richtung):# richtung: als vektor [a,b] angegeben a=0 oder b=0
    
    richtung = np.subtract(richtung, position)
    #print("es wird gepustet:", position, richtung)
    
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

#Funktion: puste_raender
#Argumente: f,g
#diese Funktion pustet die Ränder, wie in der Doku gezeigt, entsprechend zusammen. 
def puste_raender(f,g):
    global schritte
    
    while schulhof[f-1][g-1]>0:
        hausmeister_pustet([f-2,g-1],[1,0])
        schritte += 1
        print(schulhof)
        
    for i in range(f-1, 0, -1):
        hausmeister_pustet([i,g-1],[-1,0])
        schritte += 1
        print(schulhof)
        
    while schulhof[0][g-1]>0:
        hausmeister_pustet([1,g-1],[-1,0])
        schritte += 1
        print(schulhof)
        
    for i in range(g-1, 0, -1):
        hausmeister_pustet([f-1,i],[0,-1])
        schritte += 1
        print(schulhof)
    
    while schulhof[f-1][0]>0:
        hausmeister_pustet([f-1,1],[0,-1])
        schritte += 1
        print(schulhof)
        
    for i in range(f-1, 0, -1):
        hausmeister_pustet([i,0],[-1,0])
        schritte += 1
        print(schulhof)
    
    for i in range(f-1, 1, -1):
        hausmeister_pustet([0,i],[0,-1])
        schritte +=1
        print(schulhof)
        
def makeSequence(j):#erstellt die Pustesequenz für die Heuristik
    # j = Reihe, die betrachtet wird.
    
    seq = [j*-1]#enthält das erste element bereits.
    
    for i in range(1, groessen[1]-(j*-1)*2-1):#das erste element in der liste ist schon da!
        if i%2 == 1:
            seq.append((seq[-1]+2)*-1)
        else:
            seq.append((seq[-1]*-1)-1)
    return seq
    
    
###############
#Hauptprogramm#
###############

puste_raender(f,g)


for i in range(-1, (int(groessen[0]/2))*-1, -1):
    for j in makeSequence(i):
        stehfeld = [i, j]
        richtungsfeld = [i-1, j]
        
        pusten(np.array(stehfeld), np.array(richtungsfeld))
        pusten(np.array([(stehfeld[0]+1)*-1, (stehfeld[1]+1)*-1]), np.array([(richtungsfeld[0]+1)*-1, (richtungsfeld[1]+1)*-1]))
        pusten([(stehfeld[1]+1)*-1, stehfeld[0]], [(richtungsfeld[1]+1)*-1, richtungsfeld[0]])
        pusten([stehfeld[1], (stehfeld[0]+1)*-1], [richtungsfeld[1], (richtungsfeld[0]+1)*-1])
        schritte += 4
    
print(np.round(schulhof, decimals = 1), "\n")
print(f"verwendete Schritte: {schritte}")

time_end = time.time()
print("benötigte Zeit: ", time_end-time_start)