import sys
import numpy as np

file = open("paeckchen0.txt", "r")
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
tabelle = np.zeros((s,r), dtype = int)
for i in content[stopp_zeile+1:]:
    content_i = [eval(j) for j in i.split()]
    #print(i, content_i)
    tabelle[content_i[0]-1][content_i[1]-1] = content_i[2]

print("  ", end="")
for i in range(len(tabelle[0])):
    print(f"{i} ", end="")
print("")

print(tabelle)