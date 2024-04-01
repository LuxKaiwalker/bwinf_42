file = open("raetsel5.txt", "r")
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
#unplaced initialisieren:
unplaced =[i for i in range (len(blocks))]
#box initialisieren:
box = [[[0 for x in range(klen)] for y in range(klen)] for z in range (klen)]
mitte = int((klen-1)/2)
box[mitte][mitte][mitte]='G'

print("klen:", klen)
print("blocks:", blocks)
print("unplaced:", unplaced)
for ebene in box:
    print ("ebene", box.index(ebene)+1)
    for row in ebene:
        print(*row)
print("\n")
