    
    for sorte in range(s):
        for knoten in clique: #wir iterieren durch die ganzen knoten
            if stile_graph[knoten][1][sorte] > 0:
                counter = stile_graph[knoten][1][sorte]
                for i in range(len(packung_clique)):
                    if len(packung_clique[i][sorte]) == 0 and counter > 0:
                        counter -= 1
                        packung_clique[i][sorte].append([knoten, sorte])#appended ein kleidungsstück in form knoten und stil und ist damit eindeutig bestimmt
    for count_b in range(len(boxenverteilung[count])):
        boxenverteilung[count][count_b] -= boxen_anzahl
        
for packung in packungen:
    print(*packung)
        
    

#klappt nt
for count, clique in enumerate(cliquen):
    print("Boxenverteilungen: ", boxenverteilung)
    while min(boxenverteilung[count]) > 0:#wenn es noch zu packende Kleidungen gibt:
        box = [[] for _ in range(s)]#macht eine Box zunächst
        for knoten in clique:#gehe durch die knoten
            gefuellt = 0
            for count_b, kleidung in enumerate(box):
                if len(kleidung) > 0:
                    gefuellt += 1
                elif len(kleidung) == 0 and stile_graph[knoten][1][count_b] > 0:#wenn man kleidung mit entsprechenden stil aus einem Knoten entnehmen kann:
                    stile_graph[knoten][1][count_b] -= 1 # packe die kleidung aus dem graphen
                    boxenverteilung[count][count_b] -= 1 # packe sie aus den zu packenden Kleidungsstücken
                    box[count_b] = [knoten, count_b]# packe sie in die box, genaueres Labeln des Knotens und der Sorte
            if gefuellt == len(box):#wenn nichts mehr gepackt wurde und alles gepackt wurde:
                break#breche die for schleife ab und mache neue box die man packen muss
        packungen.append(box)#füge die box eben mit an

for packung in packungen:
    print(*packung)
        
                    