import time

import random
import matplotlib.pyplot as plt
import math

# get the start time
st = time.time()


blätter = [100*_ for _ in range(1,16)]
ergebnisse = []

a = 1000

def pusten(a):
    test_cases = 5000
    pustdaten = []
    i = [a for _ in range(test_cases)]
    for count, item in enumerate(i):
        pusten = 0
        while i[count] != 0:
            counter = 0
            for j in range(i[count]):
                random_var = random.randint(0,9)
        
                if random_var == 1:
                    counter +=1
                else:
                    pass
            i[count] -= counter
            pusten += 1
        pustdaten.append(pusten)
        
    return sum(pustdaten)/len(pustdaten)

for i in blätter:
    ergebnisse.append(pusten(i))
    
plt.plot(blätter, ergebnisse)
xes = [i for i in range(100,1600)]
yes = []
for x in xes:
    yes.append(math.log(0.5/x, 0.9))
plt.plot(xes,yes)
plt.show()

# get the end time
et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')


plt.show()