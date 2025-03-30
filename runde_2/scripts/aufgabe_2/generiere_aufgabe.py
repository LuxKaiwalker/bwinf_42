import random


sorten = 10
stile = 45

maxkleider = 10
minkleider = 0


print(sorten, stile)

for i in range(stile):
    for j in range(stile):
        if i>=j:
            continue
        if random.randint(0,1)==1:
            print(i+1, j+1)
print()

for i in range(sorten):
    for j in range(stile):
        if random.randint(0,1) >= 0:
            print(i+1, j+1, random.randint(minkleider, maxkleider))

