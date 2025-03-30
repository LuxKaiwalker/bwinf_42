import sys

# argv Struktur: [1] = anzahl felder, [2] = anzahl paare. output= [n][n] - array mit paaren
feldgroesse = int(sys.argv[1])
paare = int(sys.argv[2])
feld = []
for x in range(feldgroesse):
    reihe = []
    for y in range(feldgroesse):
        reihe.append(0)
    feld.append(reihe)

#Ausgeben der Inputs
print(feldgroesse)
print(paare)

#Die ersten zwei Paare platzieren, damit diese für das programm unlösbar wird.
feld[1][0] = 1
feld[1][2] = 1
feld[0][1] = 2
feld[2][1] = 2
paare = paare - 2

#Durch alle übrigen Spalten iterieren und Paare platzieren.
for spalten in range(3, feldgroesse):
    if(paare == 0):
        break
    feld[0][spalten] = spalten
    feld[-1][spalten] = spalten
    paare = paare -1

for reihe in feld:
    print (*reihe)
