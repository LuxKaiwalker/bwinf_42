###dephsearch alg (rein greedy, auskommentieren!)

import numpy as np
import random
import sys
import time


g = int(input("Bitte eine Zahl für i eingeben: "))
f = int(input("Bitte eine Zahl für j eingeben: "))
s = int(input("bitte eine Zahl für s eingeben: "))
t = int(input("bitte eine Zahl für t eingeben: "))
blaetter = int(input("bitte eine Zahl für die Anzahl der Blätter eingeben: "))

start_time = time.time()
groessen = (f,g)

zielquadrat = [s,t]

schulhof = np.full((groessen), blaetter)
pustpfad = []

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

#Funktion: enumerate_moves
#keine argumente
#Ausgabe: eine Liste von möglichen Zügen für den Schulhof
#Die Funktion prüft, ob ein möglicher Zug legitim ist und fügt diese der Liste von möglichen Zügen hinzu.
def enumerate_moves():#enumeriert alle legitime Züge für den Schulhof
    moves = []
    #zugstruktur: [[position],[richtung]]
    for i in range(groessen[0]):
        for j in range(groessen[1]):#prüfe für alle Felder auf den der Hasumeister stehen könnte, ob die Rcihtung...
            if i+1<groessen[0]:
                moves.append([[i,j],[1,0]])#oben
            if j+1<groessen[1]:
                moves.append([[i,j],[0,1]])#rechts
            if i-1>=0:
                moves.append([[i,j],[-1,0]])#links
            if j-1>=0:
                moves.append([[i,j],[0,-1]])#unten
                #...okay ist. wenn ja, liste diese auf und...
    return moves#gib die Liste zurück

#####################
#Greedy step analyse#
#####################

#Funktion: pusten_predict
#Argumente: position, richtung, hof
#Gibt zurück: den neuen Zustand des Schulhofs nach dem Pusten
#Die Funktion simuliert das Pusten der Blätter auf dem Schulhof und gibt den neuen Zustand zurück.
#Dabei arbeitet diese mit den berechneten Erwartungswerten und rundet diese auf 2 Nachkommastellen.
#Abgesehen davon ist sie der Hausmeisterfunktion vom Aufbau her ähnlich. Wir kommentieren diese Funktion also nur spärlich aus.
def pusten_predict(position, richtung, hof):# richtung: als vektor [a,b] angegeben a=0 oder b=0
    
    
    def istImHof(feld):
        if 0 <= feld[0] < groessen[0] and 0<= feld[1] < groessen[1]:
            return 1
        else:
            return 0
    
    pustfeld = np.add(position, richtung)
    ziel = np.add(pustfeld, richtung)#ziel bestimmt.
    ziel_links = np.add(ziel, [richtung[1], richtung[0]])
    ziel_rechts = np.add(ziel, [richtung[1]*-1, richtung[0]*-1])
    neuesziel = np.add(ziel, richtung)
    
    
    if istImHof(pustfeld)==0:
        
        print(f"FEHLER!!!: das pustfeld {pustfeld} ist nicht im Hof")
        exit()#wenn sich das gegebene Feld nicht im Hof befindet, dann ist ein Fehler aufgetreten.
    
    #ab hier ist der Aufbau der Hausmeisterfunktion sehr ähnlich.
    
    if not istImHof(ziel):#wenn das Ziel nicht im hof ist, werden 50% werden zur Seite geblasen
        haelfte_der_blaetter = hof[tuple(pustfeld)]
        if istImHof(np.add(pustfeld, [richtung[1], richtung[0]])):#ein seitfeld vom IstImHof??
            hof[tuple(np.add(pustfeld, [richtung[1], richtung[0]]))]+= haelfte_der_blaetter
            hof[tuple(pustfeld)]-= haelfte_der_blaetter
        if istImHof(np.add(pustfeld, [richtung[1]*-1, richtung[0]*-1])):
            hof[tuple(np.add(pustfeld, [richtung[1]*-1, richtung[0]*-1]))]+= haelfte_der_blaetter
            hof[tuple(pustfeld)]-= haelfte_der_blaetter
        return hof
    
    if istImHof (neuesziel):#ansonsten, puste wie normal.
        hof[tuple(neuesziel)] += np.round(hof[tuple(ziel)]*0.1, decimals = 2)
        hof[tuple(ziel)] = np.round(hof[tuple(ziel)]*0.9, decimals = 2)

    if istImHof(ziel_links):#pusten der Ränder legitimieren!
        hof[tuple(ziel_links)] += np.round(hof[tuple(pustfeld)]*0.1, decimals = 2)
    else:
        hof[tuple(ziel)] += np.round(hof[tuple(pustfeld)]*0.1, decimals = 2)
        
    if istImHof(ziel_rechts):
        hof[tuple(ziel_rechts)] += np.round(hof[tuple(pustfeld)]*0.1, decimals = 2)
    else:
        hof[tuple(ziel)] += np.round(hof[tuple(pustfeld)]*0.1, decimals = 2)
    
    hof[tuple(ziel)] += np.round(hof[tuple(pustfeld)]*0.8, decimals = 2)
    hof[tuple(pustfeld)] = 0
    
    return hof

#Funktion eval: evaluiert den Schulhof und bewertet diesen nach Erwartungswerten
#Argumente: hof
#Gibt zurück: die Bewertung des Schulhofs
#Eval orientiert sich an der in der Doku erwähnten Heuristik und gibt entsprechend nach der 
#Bewertung einen Score zu einem Pustfeld, das als Argument eingegeben wird, zurück. 
def eval(hof = None):
    score = 0
    for i in range(groessen[0]):
        for j in range(groessen[1]):#für jedes Feld im eigegebenen Hof:
            dis = np.subtract([i,j], zielquadrat)#Distanz berechnen
            dis = np.absolute(dis)
            if not(i==0 or i==groessen[0]-1) and not(j==0 or j==groessen[1]-1):#wenn nicht am Rand liegend, distanz zur Bewertung addieren.
                score += dis[0]*hof[i][j]
                score += dis[1]*hof[i][j]
                continue
            if i==0 or i==groessen[0]-1:#sonst: extra viel dazuaddieen als "Strafe"
                score += (g)*hof[i][j]
            if j==0 or j==groessen[1]-1:
                score += (g)*hof[i][j]
    return score#score zurückgeben

#Funktion greedy_step
#Argumente: Schulhof
#Gibt zurück: den besten Zug, den der Hausmeister machen kann
#Die Greedy-Step funktion ist die Hauptfunktion des Greedy-Algorithmus. 
#Sie berechnet die besten Züge, die der Hausmeister machen kann
def greedy_step(schulhof):

    global pustpfad
    evals = []
    for i in moves:#suche für jeden Zug nach der Evaluation und füge sie einer Liste an
        evals.append(eval(pusten_predict(i[0], i[1], np.copy(schulhof).astype(float))))

    best_eval = min(evals)#ermittle die beste Bewertung
    best_move = moves[evals.index(best_eval)]#ermittle daraus den besten zug und...
    pustpfad.append(best_move)#...füge diesen dem Pustpfad hinzu

    if eval(schulhof) <= best_eval:#gib diesen zurück wenn dieser Zug den Zustand des Schulhofes verbessert
        return 0#beende das Programm
    else:
        return best_move#sonst gib den besten Zug zurück
    
###############
#Hauptprogramm#
###############

moves = enumerate_moves()#enumeriere alle möglichen Züger zunächst
count = 0
while True:#wiederhole bis returned wird
    info = greedy_step(schulhof)
    #print(info)
    if info:
        hausmeister_pustet(info[0], info[1])
        print(schulhof)
        count += 1
    else:
        print(schulhof)
        print(f"count: {count}")
        print(f"eval: {eval(schulhof)}")
        print(pustpfad)
        end_time = time.time()
        print(f"Time: {end_time-start_time}")
        sys.exit()

