import sys
filename = sys.argv[1]
file = open(filename, "r")
content = file.readlines()
file.close()
print(content)
#kantenlänge initialisieren:
zeile_1 = content[0].split()
klen = int(zeile_1[0])
#blocks initialisieren:
blocks = []
for i in range(int(content[1])):
    zeile_i = content[2+i].split()
    block = []
    for j in range(3):
        block.append(int(zeile_i[j]))
    blocks.append(block)
#unplaced und placed initialisieren:
unplaced =[i for i in range (len(blocks))]
placed =[]
#box initialisieren:
box = [[[0 for x in range(klen)] for y in range(klen)] for z in range (klen)]
mitte = int((klen-1)/2)
box[mitte][mitte][mitte]='  G'


def findLocation(number):
    for x in range(klen):
        for y in range(klen):
            for z in range(klen):
                if box[x][y][z] == number:
                    return x, y, z

def findRot(which):#returns rot 0, 1 or 2
    a, b, c = findLocation(which+1)
    block_x, block_y, block_z = 0, 0, 0
    while (a + block_x < len(box[0])) and (box[a+block_x][b][c]==which+1):
        block_x = block_x+1
    while (b + block_y < len(box[0])) and (box[a][b+block_y][c]==which+1):
        block_y = block_y+1
    while (c + block_z < len(box[0])) and (box[a][b][c+block_z]==which+1):
        block_z = block_z+1
    if (block_x == block_y) and (block_y == block_z):
        return 2
    for i in range(3):
        if [block_x, block_y, block_z]==[blocks[which][(0+i)%3], blocks[which][(1+i)%3], blocks[which][(2+i)%3]]:
            return i
        
def printBox(message):
    print("###############################")
    print(message)
    print("unplaced:",*unplaced)
    print("placed:", *placed)
    print("blockCounter:", blockCounter)
    print("###############################")
    for ebene in box:
        print ("ebene", box.index(ebene)+1)
        for row in ebene:
            for number in row:
                print("{:3}".format(number), end=" ")
            print()
    print("\n")
    return
    
    
def placeBlock(x, y, z, which, rot):
    for a in range(blocks[which][(0+rot)%3]):
        for b in range(blocks[which][(1+rot)%3]):
            for c in range(blocks[which][(2+rot)%3]):
                box[x+a][y+b][z+c] = which+1
    unplaced.remove(which)
    placed.append(which)
#    print("placed")
    return
                        
def isValid(x, y, z, which, rot):## checks if there is valid position for block

    if klen >= max([x+blocks[which][(0+rot)%3],y+blocks[which][(1+rot)%3],z+blocks[which][(2+rot)%3]]):
        for a in range(blocks[which][(0+rot)%3]):
            for b in range(blocks[which][(1+rot)%3]):
                for c in range(blocks[which][(2+rot)%3]):
                    if box[x+a][y+b][z+c] != 0:
                        return 0
        return 1
    else:
        return 0  
    
def removePrev(justRemove):
    last = placed[-1]
    prevRot = findRot(last)
    for x in range(klen):
        for y in range(klen):
            for z in range(klen):
                if box[x][y][z] == last+1: #remove previous block
                    box[x][y][z] = 0
    unplaced.append(last)
    unplaced.sort()
    placed.pop(-1)
    if (justRemove == 1) and (prevRot == 2):
        a, b = removePrev(justRemove = 1)
        return a, b
    elif prevRot < 2:
        return unplaced.index(last), prevRot+1
    elif (last != unplaced[-1]):
        return unplaced.index(last)+1, 0
    else:
        a, b = removePrev(justRemove = 1)
        return a, b
            

rot  = 0 #can be 0,1,2
blockCounter = 0

#printBox("vor while")

while len(unplaced)>0:#while unplaced blocks exist
    x, y, z = findLocation(0)#find smallest square
    if isValid(x, y, z, unplaced[blockCounter], rot):#can you place which?
        placeBlock(x, y, z, unplaced[blockCounter], rot)#yea: place, remove from unplaced 
        blockCounter = 0 #next block iterating through unplaced list
        rot = 0
    else:#dont fit?
        if rot < 2:#try rotating
            rot = rot+1
        elif blockCounter<len(unplaced)-1:#still dont fit?
            blockCounter += 1#next block from unplaced list
            rot = 0
        else:#still dont fit??
            blockCounter, rot = removePrev(justRemove = 0)#remove last block, get 1 step forward
#            print(blockCounter, rot)
printBox("Endergebnis:")
