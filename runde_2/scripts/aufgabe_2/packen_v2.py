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
    return list(set(knoten).difference(set(doppelte_knoten)))

def kombi_funktioniert(clique):#checkt ob eine Kombination funktionieren kann oder nicht. Eine Kombination funktioneirt dann NICHT, wenn max(Summe der knoten, die einem Clique angehören) 3 mal größer ist als min (summer aller knoten der cliquen für jeden knoten.)
    summe_ueber_alle_knoten = [0 for _ in range(s)]
    summe_ueber_einfache_knoten = [0 for _ in range(s)]
    for k in clique:#k steht für knoten
        summe_ueber_alle_knoten = [sum(x) for x in zip(stile_graph[k][1], summe_ueber_alle_knoten)]##hmm gucken ob das optimale geschwindigkeit ist?
        if k in einfache_knoten:
            summe_ueber_einfache_knoten = [sum(x) for x in zip(stile_graph[k][1], summe_ueber_einfache_knoten)]
    
    print(summe_ueber_alle_knoten)
    print(summe_ueber_einfache_knoten)
    print((max(summe_ueber_einfache_knoten)/3), min(summe_ueber_alle_knoten))
    
    if (max(summe_ueber_einfache_knoten)/3)+1 > min(summe_ueber_alle_knoten):
        return False
    elif (max(summe_ueber_einfache_knoten)/3)+1 < min(summe_ueber_alle_knoten):
        return True
    else:
        sys.exit("Fehler: Irgendwas hat in kombi_funktioniert() nicht geklappt.")


cliquen = bron_kerbosch(stile_graph)
print("Cliquen: ", cliquen)

einfache_knoten = finde_einfache_knoten(cliquen)
print("Einfache Knoten in Cliquen:", einfache_knoten)

print("Funktionierende Cliquen:")
for clique in cliquen:
    print(clique)
    if kombi_funktioniert(clique):
        print(clique)

        
#print(len(result))
#print(len(hat_eindeutige_zuordnung()))#