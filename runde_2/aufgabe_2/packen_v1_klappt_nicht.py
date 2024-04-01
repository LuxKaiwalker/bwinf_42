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

def finde_alle_teilgraphen(graph):#muss noch auf deutsch umgeschrieben werden.
    
    def ist_komplett(graph, nodes):#ist das ein kompletter teilgraph?
        for node1 in nodes:
            for node2 in nodes:
                if node1 != node2 and node2 not in graph[node1][0]:
                    return False
        return True

    def find_complete_subgraphs(graph, current_node, remaining_nodes, current_subgraph):
        current_subgraph.append(current_node)

        for next_node in remaining_nodes:
            if ist_komplett(graph, current_subgraph + [next_node]):
                find_complete_subgraphs(graph, next_node, remaining_nodes - {next_node}, current_subgraph.copy())

        complete_subgraphs.append(current_subgraph)
        
        
    complete_subgraphs = []
    nodes = set(graph.keys())

    for node in nodes:
        find_complete_subgraphs(graph, node, nodes - {node}, [])
    #find_complete_subgraphs(graph, 1, nodes - {1}, [])

    return complete_subgraphs

def sort_permutations(list_of_lists):
    permutations_dict = {}

    for lst in list_of_lists:
        sorted_lst = tuple(sorted(lst))

        # Check if the sorted list is already in the dictionary
        if sorted_lst in permutations_dict:
            permutations_dict[sorted_lst].append(lst)
        else:
            permutations_dict[sorted_lst] = [lst]

    # Filter out non-permutations and return the result
    result = [group for group in permutations_dict.values() if len(group) > 1]
    return result

r = sort_permutations(finde_alle_teilgraphen(stile_graph))
result = []
for i in r:
    result.append(i[0])

for subgraph in result:
    print(subgraph)

def hat_eindeutige_zuordnung():
    global s
    relevante_teilgraphen = []
    for i in result:#checkt alle teilgrpahen ab die drankommen
        for number in i:
            if knoten == number:
                relevante_teilgraphen.append(i)
    print("knoten:",knoten)
    print("len(relevante teilgraphe n:)",len(relevante_teilgraphen))
    funktioniert = []
    for teilgraph in relevante_teilgraphen:
        summen = [0 for _ in range(s)]
        for i in teilgraph:
            summen = [sum(x) for x in zip(stile_graph[i][1], summen)]
        #print(summen)
        max = 0
        max_index = 0
        for i in range(len(stile_graph[knoten][1])):
            if stile_graph[knoten][1][i] > max:
                max = stile_graph[knoten][1][i]
                max_index = i
        alles_klappt = True
        for i in summen:
            if max_index!=i and math.ceil(float(max)/3)>i:
                alles_klappt = False
            else:
                pass
        if alles_klappt:
            funktioniert.append(teilgraph)
    #print("len(funktioniert:)", len(funktioniert))
    return funktioniert

def packeBox(funktioniert):
    pass

noch_zu_untersuchende_knoten = set(stile_graph.keys())

for knoten in noch_zu_untersuchende_knoten:#für jeden knoten:
    funktioniert = hat_eindeutige_zuordnung()
    print(funktioniert)
    if len(funktioniert) == 1:# wenn es genau 1 teilgraph gibt der klappt
        #while sum(stile_graph[knoten][1])>0:
            #packeBox(funktioniert)
        pass
        
print(len(result))
#print(len(hat_eindeutige_zuordnung()))#