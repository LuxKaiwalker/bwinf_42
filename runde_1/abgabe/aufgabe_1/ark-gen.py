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
feld[-1][-3] = 1
feld[-2][-1] = 1
feld[-1][-1] = 2
feld[-3][-2] = 2
paare = paare - 2

#Durch alle übrigen Spalten iterieren und Paare platzieren.
zahl = 3
for spalten in range(feldgroesse):
    for zeilen in range(0, feldgroesse, 2):
        if(paare == 0):
            break
        feld[zeilen][spalten] = zahl
        feld[zeilen+1][spalten] = zahl
        paare = paare -1
        zahl = zahl + 1

for reihe in feld:
    print (*reihe)
