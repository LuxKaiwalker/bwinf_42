#entscheidungsproblem: kann es vllt gehen? oder nicht? 

import sys
import numpy as np
import math


file = open("paeckchen7.txt", "r")
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

def summe_der_sorten(clique, kleidung = []):#helper funktion, die alle kleidungsstücke über einen Graph aufsummiert
    if kleidung:
        summe = kleidung
    else:
        summe = [0 for _ in range(s)]
    for k in clique:#k steht für knoten
        summe = [sum(x) for x in zip(stile_graph[k][1], summe)]##hmm gucken ob das optimale geschwindigkeit ist?
    return summe

##################
#findet den maximalen score, den man mit gegebenen knoten + ggfs. kleidungsstücken erreichen kann
###################
def finde_score(clique, kleidung = []):#findet, wieviele Kleidungsstücke gepackt werden können in einer clique, ohne diese zu packn. Damit kann bei der Auswahl von Cliquen der Score verglichen werden.
    score = 0
    if len(clique)==0:##wenn die clique ganicht mehr existiert, ist der maximale score, den man damit machen kann, 0
        return 0
    summe = summe_der_sorten(clique, kleidung)
    kleinste_anzahl = min(summe)
    for zahl in summe:
        if zahl <= kleinste_anzahl*3:
            score += zahl
        elif zahl > kleinste_anzahl*3:
            score += kleinste_anzahl*3
    return score

#######################################
#findet den maximalen score, den man mithilfe von ergänzenden kleidungsstücken erzielen kann
#und gibt dies kleidungsstücke an.
#######################################
def maximiere_score_mit_kleidung(clique):#Achtung: die Clique hier ist ohne doppelte knoten! wir gucken, wieviele Kleidugnsstücke benötigt werden, um den Score zu maximiern
    summe = summe_der_sorten(clique)
    benoetigte_kleidung = []
    groeßter_wert = max(summe)
    for zahl in summe:
        if groeßter_wert/3 - zahl<0:
            benoetigte_kleidung.append(0)
        else:
            benoetigte_kleidung.append(math.ceil(groeßter_wert/3)-zahl)
    return benoetigte_kleidung

##ermitteln des lost wertes für jede clique wenn man die benachbarten zuerst nimmt und dann beste kombi rauskriegen.
       
    
    


cliquen = bron_kerbosch(stile_graph)
print("Cliquen: ", cliquen)

einfache_knoten, doppelte_knoten = finde_einfache_knoten(cliquen)
print("Einfache Knoten in Cliquen:", einfache_knoten)

#paeckchen = [[0 for _ in range(s)] for _ in rang#
             
for clique in cliquen: ##nur debug, zeigt maximalscore und minimalscore an der möglich ist.
    print(clique)
    print(finde_score(clique))
    print(finde_score(list(set(clique).difference(set(doppelte_knoten)))))
    print(maximiere_score_mit_kleidung(list(set(clique).difference(set(doppelte_knoten)))))
    print(finde_score(list(set(clique).difference(set(doppelte_knoten))), maximiere_score_mit_kleidung(list(set(clique).difference(set(doppelte_knoten))))))
    print("")

noetige_kleidung = 0
for clique in cliquen:
    noetige_kleidung += sum(maximiere_score_mit_kleidung(list(set(clique).difference(set(doppelte_knoten)))))

print(noetige_kleidung)
print(sum(summe_der_sorten(doppelte_knoten)))

if sum(summe_der_sorten(doppelte_knoten)) < noetige_kleidung:
    print("unmöglich, alle zu packen")
else:
    print("kann sein, dass es geht!")
    
    #für das weitere finden: 
        #zähle alle vielfachen knoten;
        #iteriere durch alle kombinationen durch und finde die kombination mit höchstem Score (nicht so einfach!)
        
        #packe dieses Päckchen mit 1, 1, ... 1
    


        ###Bemerkung: evtl. das ermitteln der einzelknoten vor erstem Ausshluss der Cliqunen für höhere Effizienz???
#print(len(result))
#print(len(hat_eindeutige_zuordnung()))#