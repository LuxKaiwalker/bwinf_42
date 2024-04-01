#version mit doppelknotenspeicher
import sys
import numpy as np
import math
import copy


file = open("paeckchen-1.txt", "r")
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

def bron_kerbosch(graph):
    def bron_kerbosch_recursive(R, P, X):
        if not P and not X:
            cliques.append(R)
            return
        for v in list(P):
            bron_kerbosch_recursive(R.union({v}), P.intersection(graph[v][0]), X.intersection(graph[v][0]))
            P.remove(v)
            X.add(v)

    cliques = []
    knoten = set(graph.keys())
    bron_kerbosch_recursive(set(), knoten, set())
    #cliques.sort(key = len, reverse = True)#############################################
    #cliques.sort(key = len, reverse = False)#wieso funktioniert das am besten??
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

def summe_der_sorten(clique):#helper funktion, die alle kleidungsstücke über einen Graph aufsummiert
    summe = [0 for _ in range(s)]
    for k in clique:#k steht für knoten
        summe = [sum(x) for x in zip(stile_graph[k][1], summe)]##hmm gucken ob das optimale geschwindigkeit ist?
    return summe

def erstelle_speicher(doppelte_knoten):#erstellt eine Dictionary für doppelte Knoten.
    doppelte_knoten_speicher = {}
    for i in doppelte_knoten:
        doppelte_knoten_speicher[i] = list(stile_graph[i][1])
        for j in range(len(stile_graph[i][1])):
            stile_graph[i][1][j] = 0
    return doppelte_knoten_speicher

def packe_paeckchen(clique):#packt die päckchen einer clique zusammen, wie es hinhaut. packt soviel wie möglich, dann ist Schluss. Die reihenfolge innerhlb einer kohärenten clique ist dabei egal, die kleidugnen sind substituierbar.
    packung = [clique, summe_der_sorten(clique)]##erstelle packet, gegliedert nach btrachteter clique und anzahl der Kleidung
    uebrige_kleidung = []
    minimal = min(packung[1])#bestimmen der kleinsten kleidungssorte
    max = minimal*3
    
    for p in range(len(packung[1])):
        if packung[1][p] > max:
            uebrige_kleidung.append(packung[1][p]-max)
            packung[1][p] = max
        else:
            uebrige_kleidung.append(0)
    
    for k in clique:
        stile_graph[k][1] = [0 for _ in range(s)]
    
    for count, k in enumerate(clique):
        if k in einfache_knoten:
            stile_graph[clique[count]][1] = uebrige_kleidung
            break
        
    return packung
        
def finde_score(clique):##s muss mindestens 2 sein als einschränkung!
    #score in sinne [ordnung der klasse, [score der Klasse]]
    #wichtig: wenn Score = 0 bedeutet das mega kacke!
    score = [0, 0]
    summe = summe_der_sorten(clique)
    summe.sort()
        
    for i in range(s):
        if summe[i] != 0:
            score[0] = i
            score[1] = summe[i]#wieviele Kleidungsstücke damit gepackt werden können
            break
        else: 
            pass
    return score
            
def finde_differenzen(knoten):
    print("DEBUG: ",knoten)
    relevante_scores = []
    for count, clique in enumerate(cliquen):
        if knoten in clique:
            if scores[count] not in relevante_scores:
                relevante_scores.append(scores[count])
    
    print("relevante scores: ", relevante_scores)
    #die dringlchkeit eines Scores wird aus der Differenz des größten und kleinsten scores genommen.
    #klassen gehen immer vor. ist die Differenz in Klassen gleich, guckt man sch die kleinere Klassen an. sonst ist es egal
    #(yay heuristik)
    
    for score in relevante_scores:
        pass
    
    return
        
    


#######################################
#findet den maximalen score, den man mithilfe von ergänzenden kleidungsstücken erzielen kann
#und gibt dies kleidungsstücke an.
#######################################
def maximiere_score_mit_kleidung(clique):#Achtung: die Clique hier ist ohne doppelte knoten! wir gucken, wieviele Kleidugnsstücke benötigt werden, um den Score zu maximiern
    summe = summe_der_sorten(clique)
    benoetigte_kleidung = []
    groesster_wert = max(summe)
    for zahl in summe:
        #print(groesster_wert, groesster_wert/3 - zahl)
        if groesster_wert/3 - zahl<0:
            benoetigte_kleidung.append(0)
        else:
            benoetigte_kleidung.append(math.ceil(groesster_wert/3)-zahl)
    return benoetigte_kleidung

##ermitteln des lost wertes für jede clique wenn man die benachbarten zuerst nimmt und dann beste kombi rauskriegen.



cliquen = bron_kerbosch(stile_graph)
print("Cliquen: ", cliquen)

einfache_knoten, doppelte_knoten = finde_einfache_knoten(cliquen)
print("Einfache Knoten in Cliquen:", einfache_knoten)
print("Doppelte Knoten in Cliquen:", doppelte_knoten)

doppelknotenspeicher = erstelle_speicher(doppelte_knoten)#packt doppelte knoten in einen seperaten dictionary, um darauf zugreifen zu können und die cliquen direkt behandeln zu können.
print("doppeltknotenspeicher:", doppelknotenspeicher)
print("leergeräumter graph:", stile_graph)

kleidung = []
for clique in cliquen:
    kleidung.append(packe_paeckchen(list(clique)))
print("gepackte_päckchen: ", kleidung)
print(stile_graph)

scores = []
for clique in cliquen: 
    scores.append(finde_score(clique))
print("scores der cliquen: ",scores)

diff = []
for k in doppelte_knoten:
    diff.append(finde_differenzen(k))
print(doppelte_knoten)
print("größte Differenzen der Knoten:",diff)

##weiteres Vorgehen:
#1. finde den score von jeder clique**

#-----todo:
#2. ermittle von jedem doppelten knoten den maximalen benachbarten score differenz und den minimalen
#3. ausgehend vom maximalen scoredifferenz, teile die Kleidung, die benötigt wird zu. 
#4. wiederhole schritt 1-3 bis nichts mehr geht.

#5. wenn alle cliquen keine kleidung mehr haben ist der score -inf und wir versuchen neue eindeutige cliquen aus dem was übrig bleibt zu bilden (muss noch überlegt werden.)
#6. wenn alle zyklen fertig sind und keine neuen cliquen mehr gebildet werden können, alle übrigen Kleidungen möglichst auf die boxn verteilen.

    
    #für das weitere finden: 
        #zähle alle vielfachen knoten;
        #iteriere durch alle kombinationen durch und finde die kombination mit höchstem Score (nicht so einfach!)
        
        #packe dieses Päckchen mit 1, 1, ... 1
    


        ###Bemerkung: evtl. das ermitteln der einzelknoten vor erstem Ausshluss der Cliqunen für höhere Effizienz???
#print(len(result))
#print(len(hat_eindeutige_zuordnung()))#