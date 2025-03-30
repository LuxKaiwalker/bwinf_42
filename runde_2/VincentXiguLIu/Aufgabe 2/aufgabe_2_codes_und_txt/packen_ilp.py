#linear programming ansatz.

import pulp as pl
import time#zum Messen der Laufzeit

str = input("bitte eingeben, welche .txt Datei im selben Ordner geöffnet werden soll: ")

file = open(str, "r")#wir öffnen die .txt datei uns lesen diese aus
content = file.readlines()
file.close()

time_start = time.time()

s,r = [eval(i) for i in content[0].split()]

passend = []
stopp_zeile = 0
for i in content:
    if i == "\n":
        stopp_zeile = content.index(i)
for i in range(1, stopp_zeile):
    passend.append([eval(j) for j in content[i].split()])

##wir erstellen ein dictionary.

stile_graph = {}

#datensruktur: name_des_knotens: [anzahl der kleidungsstücke]
for i in range(r):
    stile_graph[i+1] =[[],[0 for _ in range(s)]]

# einfügen der benachbarte knoten
for a, b in passend:
    stile_graph[a][0].append(b)
    stile_graph[b][0].append(a)#knoten sind immer gegenseitig

#einfügen der Kleidungsstücke
for i in content[stopp_zeile+1:]:
    sorte_i, stil_i, anzahl_i = [eval(j) for j in i.split()]
    stile_graph[stil_i][1][sorte_i-1] = anzahl_i

#wir geben den Graphen aus
print(stile_graph)  

#################################
##TEIL FINDEN MAXIMALER CLIQUEN##
#################################

#Funktion: Bron-Kerbosch. 
#Parameter: Graph in Dictionary-Form
#Rückgabe: Liste von maximalen Cliquen 
#der Bron-Kerbosch-Algorithmus ist ein rekursiver Algorithmus, 
#der alle maximalen Cliquen in einem Graphen findet.
#wir benutzen hierbei eine Version ohne pivoting, welche sich trotzdem als sehr effizient erweist.
def bron_kerbosch(graph):
    def bron_kerbosch_rekursiv(R, P, X):#dies ist die eigentliche Rekursionfunktion
        if not P and not X:
            cliques.append(R)
            return
        for v in list(P):
            bron_kerbosch_rekursiv(R.union({v}), P.intersection(graph[v][0]), X.intersection(graph[v][0]))
            P.remove(v)
            X.add(v)

    cliques = []
    knoten = set(graph.keys())
    bron_kerbosch_rekursiv(set(), knoten, set())
    return cliques

#Funktion: Finde einfache Knoten
#Parameter: Liste von Cliquen
#Rückgabe: Liste von Knoten, die in genau einer Clique vorkommen
#Diese Funktion benötigen wir, um Variablen für die Lineare optimierung erstellen zu können.
#Dadurch gehen wir jeden Knoten/stil einmal durch und tragen Knoten, welche nur teil einer 
#einzigen Clique sind, in eine Liste ein.
def finde_einfache_knoten(cliquen):
    knoten = []
    doppelte_knoten = []
    for clique in cliquen:
        for k in clique:
            if k not in knoten:
                knoten.append(k)
            elif k not in doppelte_knoten:
                doppelte_knoten.append(k)
            else: 
                pass
    return list(set(knoten).difference(set(doppelte_knoten))), doppelte_knoten

#Ausführen des Bron-Kerbosch-Algorithmus
cliquen = bron_kerbosch(stile_graph)
print("Cliquen: ", cliquen)#ausgeben der Cliquen

#Ausführen der Funktion finde_einfache_knoten und erstellen einer zugehörigen liste
einfache_knoten, doppelte_knoten = finde_einfache_knoten(cliquen)
print("Einfache Knoten in Cliquen:", einfache_knoten)#ausgeben der einfachen Knoten

############################
##TEIL LINEARE OPTIMIERUNG##
############################

#Funktion: Summe der sorten
#Argumente: Clique, doppelt
#Rückgabe: Liste von Summen der Kleidungsstücke
#Diese Funktion checkt ob eine Kombination funktionieren kann oder nicht. 
#Eine Kombination funktioneirt dann NICHT, wenn max(Summe der knoten, die einem Clique angehören) 
#3 mal größer ist als min (summer aller knoten der cliquen für jeden knoten.)
#Dadurch ist die Funktion sehr wichtig, wenn wir die Legitimität bestimmter Cliquensummen überprüfen wollen
def summe_der_sorten(clique, doppelt = True):
    summe = [0 for _ in range(s)]
    if doppelt:
        for k in clique:#k steht für knoten
            summe = [sum(x) for x in zip(stile_graph[k][1], summe)]##hmm gucken ob das optimale geschwindigkeit ist?
        return summe
    else:
        for k in clique:
            if k in einfache_knoten:
                summe = [sum(x) for x in zip(stile_graph[k][1], summe)]##hmm gucken ob das optimale geschwindigkeit ist?
        return summe

#wir ermitteln zunächst die maximale Summe der Kleidungsstücke in Cliquen ohne Doppelknoten für die obere Schranke
summen_ohne_doppelknoten = []
for clique in cliquen:
    summen_ohne_doppelknoten.append(summe_der_sorten(clique, doppelt = False))
print("summen ohne Doppelknoten:")
print(summen_ohne_doppelknoten)

#erstelle Problem
problem = pl.LpProblem("StilvollePackungen", pl.LpMaximize)

#erstelle Entscheidungsvariablen
cliquenvariablen = []
for i in range(len(cliquen)):
    stile = []
    for j in range(s):
        stile.append(pl.LpVariable(f"clique{i}_sorte_{j}", lowBound = 0, cat = 'Integer'))
    cliquenvariablen.append(stile)
print("Cliquenvariablen: ", cliquenvariablen)
    
doppelknotenvariablen = []
for i, clique in enumerate(cliquen):
    c = []#vorläufige liste aller variablen der Doppelknoten der Clique
    for count, k in enumerate(doppelte_knoten):
        if k in clique:
            stile = []
            for j in range(s):
                stile.append(pl.LpVariable(f"doppelknoten_clique{i}_knoten{k}_sorte_{j}", lowBound = 0, cat = 'Integer'))
            c.append(stile)
        else:
            c.append(None)
    doppelknotenvariablen.append(c)
print("Doppelknotenvariablen: ", doppelknotenvariablen)

#maximierungsgleichung hinzufügen:
gleichung = None
for clique in doppelknotenvariablen:
    for knoten in clique:
        if knoten:
            for var in knoten:
                gleichung += var
for clique in cliquenvariablen:
    for var in clique:
        gleichung += var
problem += gleichung        

#ungleichungen hinzufügen
for count, clique in enumerate(cliquen):
    #die summe darf die summe ohne doppelte knoten nicht übersteigen.
    for sorte in range(s):
        problem += cliquenvariablen[count][sorte] <= summen_ohne_doppelknoten[count][sorte]
    
for count, k in enumerate(doppelte_knoten):
    #die summe der doppelten knoten muss immer zueinander passen.
    for sorte in range(s):
        linke_seite = None
        for clique, cliquenknoten in enumerate(doppelknotenvariablen):#fügt alle doppelknoten innerhalb einer Clique
            if cliquenknoten[count]:
                linke_seite += cliquenknoten[count][sorte]
        problem += linke_seite <= stile_graph[k][1][sorte]

for count, clique in enumerate(cliquen):#die summe der gepackten variablen dürfen nicht größer als die dreifache Summe der korrespondierenden Summen der anderen Variablen sein
    for stila in range(s):
        for stilb in range(s):
            if stila == stilb:
                continue#wir vermeiden selbstschleifen, dort ist die zu zeigende Ungleichugn trivial
            linke_seite = None
            linke_seite += cliquenvariablen[count][stila]
            linke_seite -= 3*cliquenvariablen[count][stilb]
            for k in clique:
                if k in doppelte_knoten and doppelknotenvariablen[count][doppelte_knoten.index(k)]:
                    linke_seite += doppelknotenvariablen[count][doppelte_knoten.index(k)][stila]
                    linke_seite -= 3*doppelknotenvariablen[count][doppelte_knoten.index(k)][stilb]
            problem += linke_seite <= 0

#löse das Problem
problem.solve()

summe_der_kleidung = 0

#ausgabe aller relevanten Variablen        
print("Status:", pl.LpStatus[problem.status])
print("Doppelknotenvariablen:")
for clique in doppelknotenvariablen:
    for knoten in clique:
        if knoten:
            for var in knoten:
                print(f"{var.name}: {var.value()}")
                summe_der_kleidung += var.value()
                
print("cliquenvariablen:")
for clique in cliquenvariablen:
    for var in clique:
        print(f"{var.name}: {var.value()}")
        summe_der_kleidung += var.value()
    

#Wir summieren die gepackten und tatsächlichen Kleidungsstücke zusammen und gucken,
#wieviele Kleidungsstücke noch übrigbleiben
print("gepackte Kleidungsstücke:     ", summe_der_kleidung)
summe_total = 0
for i in stile_graph:
    for j in stile_graph[i][1]:
        summe_total += j
print("tatsächliche Kleidungsstücke: ", summe_total)
print("Übrige Kleidungsstücke: ", summe_total-summe_der_kleidung)

#wir fangen an die Boxen zu erstellen und erstellen dazu erst die Boxenverteilungen. 
#die Bosenverteilung gibt dabei an, wieviele Kleidungsstücke welcher Sorte in einer Clique
#gepackt werden muss.
boxenverteilung = []
for count in range(len(cliquen)):
    boxenverteilung.append([int(cliquenvariablen[count][i].value()+sum([doppelknotenvariablen[count][j][i].value() for j in range(len(doppelte_knoten)) if doppelknotenvariablen[count][j]])) for i in range(s)])
    
############################################
##TEIL UMWANDLUNG DER LÖSUNGEN IN PÄCKCHEN##
############################################

#FUNKTION: Printboxen
#Parameter: Keine
#Rückgabe: Keine
#Gibt die zu packenden Boxen anhand der Boxenverteilungen aus.
def printboxen():
    #tatsächliche Illustration der Boxen:
    packungen = []
    for count, clique in enumerate(cliquen):#wir erstellen eine Packungsliste für jede Clique einzeln und geben diese auch Cliquenweise aus
        packung_clique = []

        boxen_anzahl = min(boxenverteilung[count])
        min_index = boxenverteilung[count].index(boxen_anzahl)

        for i in range(boxen_anzahl):
            packung_clique.append([[] for _ in range(s)])#erstellt leere Boxen boxen die gepackt werden müssen

        #nimmt aus den ganzen doppelten knoten die zugeteilten Kleider und packt diese in die Boxen
        for sorte in range(s):
            box_counter = 0
            zu_packende_kleidung = 0
            for k in range(len(doppelte_knoten)):#für alle doppelten knoten
                if doppelknotenvariablen[count][k]:
                    zu_packende_kleidung += doppelknotenvariablen[count][k][sorte].value()
            for k, knoten in enumerate(doppelte_knoten):#für alle doppelten knoten
                if zu_packende_kleidung == 0:
                    break
                if doppelknotenvariablen[count][k]:
                    for i in range(int(doppelknotenvariablen[count][k][sorte].value())):#für jede zu packende kleidung:
                        zu_packende_kleidung -= 1
                        stile_graph[knoten][1][sorte] -= 1
                        packung_clique[box_counter%boxen_anzahl][sorte].append([knoten, sorte])
                        box_counter += 1

        #füllt in jede box 1 im minimum index (jetzt für auf jede sorte erweitern und 
        #wir sind fertig)
        for sorte in range(s):
            for k in list(set(clique).difference(set(doppelte_knoten))):#füllt erst mal ein Kleidungsstück pro clique auf.
                for i in range(boxen_anzahl):
                    if packung_clique[i][sorte] == []:#die sorte ist noch leer! packe ein Kleidungsstück rein.
                        stile_graph[k][1][sorte] -= 1
                        packung_clique[i][sorte].append([k, sorte])#packt das kleidungsstück in eine richtige box
                        boxenverteilung[count][sorte] -= 1#nimmt eins weg von den zu packenden kleidungsstücken
                    else:
                        pass#fertig, wir müssen nichts machen
                    
            box_counter = 0
            for knoten in list(set(clique).difference(set(doppelte_knoten))):#füllt alle kleidungsstücke auf
                if boxenverteilung[count][sorte] == 0:#die sorte ist fertig!
                    break 
                while stile_graph[knoten][1][sorte] > 0:#die sorte ist fertig!
                    if boxenverteilung[count][sorte] == 0:
                        break
                    stile_graph[knoten][1][sorte] -= 1
                    packung_clique[box_counter%boxen_anzahl][sorte].append([knoten, sorte])#packt das kleidungsstück in eine richtige box
                    boxenverteilung[count][sorte] -= 1#nimmt eins weg von den zu packenden kleidungsstücken
                    box_counter += 1
        packungen.append(packung_clique)

    #ausgabe aller Packungen, die gepackt wurden
    o=0
    for item in packungen:
        print("clique:", o)
        o += 1
        for i in item:
            print(*i)

#ausführen der printboxen funktion
printboxen()

#Zeit stoppen, laufzeit berechnen und ausgeben
time_end = time.time()
print("Time: ", time_end-time_start)#Ausgeben der Laufzeit