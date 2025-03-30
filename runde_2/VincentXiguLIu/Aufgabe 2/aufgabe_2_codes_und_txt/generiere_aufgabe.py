#Aufgabengenerator für Aufgabe 2.
import random

#Eingeben aller relevanter Parameter
sorten = int(input("bitte anzahl Sorten eingeben: "))
stile = int(input("bitte anzahl Stile eingeben: "))
graphendichte = int(input("bitte Graphendichte eingeben (jede nte Zahl hat eine Verbindung): "))

maxkleider = int(input("bitte maxkleider eingeben: "))
minkleider = int(input("bitte minkleider eingeben: "))
kleidungsdichte = int(input("bitte Kleidungsdichte eingeben (JEde Nte zelle hat Kleidungsstücke): "))

#wir öffnen das beigefügte .txt Dokument (am Anfang noch leer)
file = open("paeckchengen.txt", "w")

file.write(f"{sorten} {stile}\n")

#erstelle zufällige Stile, die zusammenpassen
for i in range(stile):
    for j in range(stile):
        if i>=j:
            continue
        if not random.randint(0,graphendichte):
            file.write(f"{i+1} {j+1}\n")
file.write("\n")

#erstelle zufällige Kleidungsstücke
for i in range(sorten):
    for j in range(stile):
        if not random.randint(0,graphendichte):
            file.write(f"{i+1} {j+1} {random.randint(minkleider, maxkleider)}\n")

#fertig!
file.close()
print("die Ausgabe wurde unter 'paeckchengen.txt' gespeichert.")
