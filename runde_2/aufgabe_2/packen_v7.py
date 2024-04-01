#linear programming ansatz.

import pulp as pl


file = open("paeckchen6.txt", "r")
content = file.readlines()
file.close()
#print(content)

s,r = [eval(i) for i in content[0].split()]

passend = []
stopp_zeile = 0
for i in content:
    if i == "\n":
        stopp_zeile = content.index(i)
for i in range(1, stopp_zeile):
    passend.append([eval(j) for j in content[i].split()])

print("s, r:", s,r)

##wir erstellen ein dictionary.

stile_graph = {}

#datensruktur: name_des_knotens: [benachbarte_knoten][anzahl der kleidungsstücke]
for i in range(r):
    stile_graph[i+1] =[[],[0 for _ in range(s)]]

# einfügen der benachbarte knoten
for a, b in passend:
    stile_graph[a][0].append(b)
    stile_graph[b][0].append(a)#knoten sind immer gegenseitig

for i in content[stopp_zeile+1:]:
    
    sorte_i, stil_i, anzahl_i = [eval(j) for j in i.split()]
    #print(i, content_i)
    stile_graph[stil_i][1][sorte_i-1] = anzahl_i
    #tabelle[content_i[0]-1][content_i[1]-1] = content_i[2] 
    
print(stile_graph)  

#################################
##TEIL FINDEN MAXIMALER CLIQUEN##
#################################
def bron_kerbosch(graph):
    def bron_kerbosch_rekursiv(R, P, X):
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

cliquen = bron_kerbosch(stile_graph)
print("Cliquen: ", cliquen)

einfache_knoten, doppelte_knoten = finde_einfache_knoten(cliquen)
print("Einfache Knoten in Cliquen:", einfache_knoten)

############################
##TEIL LINEARE OPTIMIERUNG##
############################

def summe_der_sorten(clique, doppelt = True):#checkt ob eine Kombination funktionieren kann oder nicht. Eine Kombination funktioneirt dann NICHT, wenn max(Summe der knoten, die einem Clique angehören) 3 mal größer ist als min (summer aller knoten der cliquen für jeden knoten.)
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
    
        
print("gepackte Kleidungsstücke:     ", summe_der_kleidung)
summe_total = 0
for i in stile_graph:
    for j in stile_graph[i][1]:
        summe_total += j
print("tatsächliche Kleidungsstücke: ", summe_total)
print("Übrige Kleidungsstücke: ", summe_total-summe_der_kleidung)

for clique in cliquen:
    print("Clique: ", clique)

boxenverteilung = []
for count in range(len(cliquen)):
    boxenverteilung.append([int(cliquenvariablen[count][i].value()+sum([doppelknotenvariablen[count][j][i].value() for j in range(len(doppelte_knoten)) if doppelknotenvariablen[count][j]])) for i in range(s)])
    print(boxenverteilung[-1])
    
############################################
##TEIL UMWANDLUNG DER LÖSUNGEN IN PÄCKCHEN##
############################################
def printboxen():
    #tatsächliche Illustration der Boxen:
    packungen = []
    # Disclaimer: die Boxen werden nicht exakt nach den lösungen gepackt, weil einzelknoten kleidungen bevorzugt werden. 
    # das ergebnis bleibt aber gleich, es blebt nur häufiger was in doppelknoten was übrig.
    for count, clique in enumerate(cliquen):
        packung_clique = []

        boxen_anzahl = min(boxenverteilung[count])
        min_index = boxenverteilung[count].index(boxen_anzahl)

        for i in range(boxen_anzahl):
            packung_clique.append([[] for _ in range(s)])#erstellt dummy boxen die alle gepackt werden müssen

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
        # wir müssten fertig sein)
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
        
    summe_naher = 0
    for i in stile_graph:
        for j in stile_graph[i][1]:
            summe_naher += j
    print(summe_naher)

    o=0
    for item in packungen:
        print("clique:", o)
        o += 1
        for i in item:
            print(*i)

printboxen()
