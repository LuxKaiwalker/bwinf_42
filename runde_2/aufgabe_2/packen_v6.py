#neue, optimierte datenstruktur. Zudem brute force ansatz.


import sys
import numpy as np
import math


file = open("paeckchen2.txt", "r")
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
    stile_graph[i+1] =[]

# einfügen der benachbarten knoten
for a, b in passend:
    stile_graph[a].append(b)
    stile_graph[b].append(a)#knoten sind immer gegenseitig
    
print(stile_graph)  

def bron_kerbosch(graph):
    def bron_kerbosch_recursive(R, P, X):
        if not P and not X:
            cliques.append(R)
            return
        for v in list(P):
            bron_kerbosch_recursive(R.union({v}), P.intersection(graph[v]), X.intersection(graph[v]))
            P.remove(v)
            X.add(v)

    cliques = []
    knoten = set(graph.keys())
    bron_kerbosch_recursive(set(), knoten, set())
    #cliques.sort(key = len, reverse = True)#############################################
    #cliques.sort(key = len, reverse = False)#wieso funktioniert das am besten??
    return cliques        

def finde_doppelte_knoten(cliquen): 
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
    return doppelte_knoten

## ändert den grphen etwas um: knoten, die in meheren Ckqiuen auftauchen, werden nun getrennt für jede cliqu betrahctet, sodass die Clqieun paarweise disjunkt sind
# diese werden einfach durch neue Knoten sehr großer zahl dargestellt, z.B: 200, 300 etc.
def separiere_cliquen(cliquen):
    separierte_cliquen = []
    for index, clique in enumerate(cliquen):
        separierte_cliquen.append({})
        for k in clique:
            separierte_cliquen[index][k] = [0 for _ in range(s)]#hier werden die kleinen Clqieun erstellt. deise werden im nächsten schritt dann aufgefüllt. (kommt aber noch)
    return separierte_cliquen

def einfuegen_der_werte():
    #einfügen der Werte in die getrennten Cliquen, wird jetzt später woanders gebraucht
    for i in content[stopp_zeile+1:]:
        sorte_i, stil_i, anzahl_i = [eval(j) for j in i.split()]
        for index, clique in enumerate(cliquen):
            if stil_i in clique:
                cliquen_getrennt[index][stil_i][sorte_i-1] = anzahl_i
                break

def summe_der_sorten(clique_i, doppelknoten = True):#helper funktion, die alle kleidungsstücke über einen Graph aufsummiert
    
    def ohne_doppelte_knoten():
        neue_liste = []
        for knoten, anzahl in cliquen_getrennt[clique_i].items():
            if knoten not in doppelte_knoten:
                neue_liste.append(anzahl)
        return neue_liste
    
    summe = [0 for _ in range(s)]
    
    #print("Debug: ", ohne_doppelte_knoten())
    #print("Debug2: ", cliquen_getrennt[clique_i])
    #print(cliquen_getrennt[clique_i].keys())
    
    if doppelknoten:
        for werte in ohne_doppelte_knoten():
            summe = [sum(x) for x in zip(werte, summe)]
        return summe
    else:
        for k in cliquen_getrennt[clique_i].keys():
            summe = [sum(x) for x in zip(cliquen_getrennt[clique_i][k], summe)]#hier +1 weil k der schlüssel ist
        return summe
    
def finde_score():
    score = 0
    for clique in range(len(cliquen)):
        summe = summe_der_sorten(clique)
        minimum = min(summe)
        for i in summe: 
            if i<=minimum*3:
                score += i
            else:
                score += minimum*3
    return score

def benoetigte_kleidung(clique_i, doppelte_knoten_miteinbeziehen = True):#die Clique hier ist ohne doppelte knoten! wir gucken, wieviele Kleidugnsstücke benötigt werden, um den Score zu maximiern
    summe = summe_der_sorten(clique_i, doppelknoten = doppelte_knoten_miteinbeziehen)
    benoetigte_kleidung = []
    groesster_wert = max(summe)
    for zahl in summe:
        #print(groesster_wert, groesster_wert/3 - zahl)
        if groesster_wert/3 - zahl<0:
            benoetigte_kleidung.append(0)
        else:
            benoetigte_kleidung.append(math.ceil(groesster_wert/3)-zahl)
    return benoetigte_kleidung

cliquen = bron_kerbosch(stile_graph)
print("Cliquen: ", cliquen)

doppelte_knoten = finde_doppelte_knoten(cliquen)
print("Doppelte Knoten: ", doppelte_knoten)

cliquen_getrennt = separiere_cliquen(cliquen)
print("Cliquen getrennt:", cliquen_getrennt)

einfuegen_der_werte()
print(print("Cliquen nach einfügen der Werte:", cliquen_getrennt))

max_score = 0
max_moeglich = 0
for dic in cliquen_getrennt:
    print(dic)
    for i in dic:
        print(dic[i])
        max_moeglich += sum(dic[i])
print("max_moeglich: ", max_moeglich)
        
print("aktueller_score: ",finde_score())

##jetzt ist die tabelle in der richtigen nutzbaren Datenstruktur eingelesen. Wenn die Tabelle lösbar ist, knnen wir diese nun durch die finde kleidung tabelle lösen.
