file = open("paeckchen7.txt", "r")
content = file.readlines()
file.close()

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

#datensruktur: name_des_knotens: [benachbarte_knoten][anzahl der kleidungsstücke]
for i in range(r):
    stile_graph[i+1] =[[],[0 for _ in range(s)]]

# einfügen der benachbarte knoten
for a, b in passend:
    stile_graph[a][0].append(b)
    stile_graph[b][0].append(a)#knoten sind immer gegenseitig

for i in content[stopp_zeile+1:]:
    sorte_i, stil_i, anzahl_i = [eval(j) for j in i.split()]
    stile_graph[stil_i][1][sorte_i-1] = anzahl_i
    
print("Eingelester Stile-Graph: ", stile_graph)  

#jetzt die ganzen Funktionen
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
    return list(set(knoten).difference(set(doppelte_knoten))), doppelte_knoten

def summe_der_sorten(clique):
    summe = [0 for _ in range(s)]
    for k in clique:#k steht für knoten
        summe = [sum(x) for x in zip(stile_graph[k][1], summe)]##hmm gucken ob das optimale geschwindigkeit ist?
    return summe

def packe_paeckchen(clique_nummer):
    uebrige_sorten = [1 for _ in range(s)]
    for k in list(set(cliquen[clique_nummer]).intersection(set(einfache_knoten))):
        for i in range(s):
            if stile_graph[k][1][i] > 0 and uebrige_sorten[i] == True:
                stile_graph[k][1][i] -= 1
                uebrige_sorten[i] = 0   
    for k in list(set(cliquen[clique_nummer]).difference(set(einfache_knoten))):
        for i in range(s):
            if stile_graph[k][1][i] > 0 and uebrige_sorten[i] == True:
                stile_graph[k][1][i] -= 1
                uebrige_sorten[i] = 0
    if sum(uebrige_sorten)<=0:
        paeckchen[clique_nummer] = [sum(x) for x in zip(paeckchen[clique_nummer], [1 for _ in range(s)])]#sorten

def fuelle_paeckchen(knoten):
    for count_c, clique in enumerate(cliquen):
        if knoten in clique:#was ist wenn bei doppelten Knoten besser andere Lücken gefülltwerden können?
            for count_s, stil in enumerate(stile_graph[knoten][1]):
                diff1 = min(paeckchen[count_c])*3-paeckchen[count_c][count_s]
                if stil <= diff1:
                    paeckchen[count_c][count_s] += stil
                    stile_graph[knoten][1][count_s] = 0
                else:
                    diff2 = min(paeckchen[count_c])*3-paeckchen[count_c][count_s]
                    stile_graph[knoten][1][count_s] -= diff2
                    paeckchen[count_c][count_s] += diff2

cliquen = bron_kerbosch(stile_graph)
print("Cliquen: ", cliquen)

einfache_knoten, doppelte_knoten = finde_einfache_knoten(cliquen)
print("Einfache Knoten in Cliquen:", einfache_knoten)

paeckchen = [[0 for _ in range(s)] for _ in range(len(cliquen))]

summe_vorher = 0
for i in stile_graph:
    for j in stile_graph[i][1]:
        summe_vorher += j
print("Summe vor dem Packen: ", summe_vorher)

for lll in range(199):## für sehr lang zeit die päckchen packen! dabei die einzelnen knoten bevorzugen.
    for i in range(len(cliquen)):
        #print(cliquen[i])
        if min(summe_der_sorten(cliquen[i])) > 0:##die cliquen werden in beliegiber reihenfolge gepackt...
            ## wenn die kleinste Sorte größer 0 ist:
            packe_paeckchen(i)

for knoten in einfache_knoten:#anschließend:  weiterpacken diese ausfüllen! an dieser stelle wurden also alle päckchen schon gepackt, die gepackt werden können.
    fuelle_paeckchen(knoten)#funktion muss noch geschrieben werden!
for knoten in doppelte_knoten:
    fuelle_paeckchen(knoten)#füllt alle päckchen mit doppelten knoten. vllt. braucht man eine andere Funktion???

for clique in cliquen:
    print("Clique: ", clique)
for packung in paeckchen:
    print(packung)

summe_naher = 0
for i in stile_graph:
    for j in stile_graph[i][1]:
        summe_naher += j
print(summe_naher)