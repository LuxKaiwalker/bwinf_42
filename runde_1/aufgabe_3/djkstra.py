import copy
file = open("zauberschule_5.txt", "r")
content = file.readlines()
file.close()
x, y = content[0].split()
x = int(x)
y = int(y)

maze =[]
print("Reading content...")
#print(content)
#print("\n\n")
#print(len(content), len(content[0]), y)
for i in range(2):
    plane = []
    for j in range(1, x+1):
        row = content[j+(i*(x+1))].split()
        row = list(row[0])
        plane.append(row)
    maze.append(plane)

#for k in range(2): 
#    for i in range(len(maze[0])):
#        for j in range(len(maze[0][0])):
#            print(maze[k][i][j], end = " ")
#        print("")

graph =  {} #einführung des dicts
mazeWithNums = copy.deepcopy(maze)


def findNeighbours(z, y, x):#finds neighbours for an block. returns: [[a,b,c,d],[lengh lengh lengh lengh]]
    nodes = []
    lenghs = []
    if (maze_x-1 >= x+1 and mazeWithNums[z][y][x+1]!= "#"):
        nodes.append(mazeWithNums[z][y][x+1])
        lenghs.append(1)
    if (0 <= x-1 and mazeWithNums[z][y][x-1]!= "#"):
        nodes.append(mazeWithNums[z][y][x-1])
        lenghs.append(1)
    if (maze_y-1 >= y+1 and mazeWithNums[z][y+1][x]!= "#"):
        nodes.append(mazeWithNums[z][y+1][x])
        lenghs.append(1)
    if (0 <= y-1 and mazeWithNums[z][y-1][x]!= "#"):
        nodes.append(mazeWithNums[z][y-1][x])
        lenghs.append(1)
    if (maze_z-1 >= z+1 and mazeWithNums[z+1][y][x]!= "#"):
        nodes.append(mazeWithNums[z+1][y][x])
        lenghs.append(3)
    if (0 <= z-1 and mazeWithNums[z-1][y][x]!= "#"):
        nodes.append(mazeWithNums[z-1][y][x])
        lenghs.append(3)
    return [nodes, lenghs]

def dijkstra (graph, start, end):
    unsolved_nodes = {}
    for i in graph:
        graph[i].append(float("inf"))## now graph[i][2]
        graph[i].append(None)## previous node
        unsolved_nodes[i] = graph[i]
    graph[start][2] = 0
    print(graph, "\n")
#    print("\n\n\n")
#    print(unsolved_nodes, "\n", *unsolved_nodes)
  
    while unsolved_nodes:
        u = None#index of shortest path
        shortest = float("inf")#value of shortest path
        for keys, values in unsolved_nodes.items():
            if values[2]<shortest:
                shortest = values[2]
                u = keys
        unsolved_nodes.pop(u)
        
        for i in range(len(graph[u][0])):#for every neighbour
#            print(v)
            v = graph[u][0][i]
            new = graph[u][2]+graph[u][1][i]
            if new < graph[v][2]:
                graph[v][2] = new#dist
                graph[v][3] = u#previous
        if u == end:
            return 0
    return 1
    
def printPath(current, next):
    
    maze_z = len(maze)
    maze_y = len(maze[0])
    maze_x = len(maze[0][0])
    for k in range(maze_z): 
        for i in range(maze_y):
            for j in range(maze_x):
                if mazeWithNums[k][i][j] == current:
                    if (maze_x-1 >= j+1 and mazeWithNums[k][i][j+1]==next):
                        maze[k][i][j] = ">"
                    elif (0 <= j-1 and mazeWithNums[k][i][j-1]==next):
                        maze[k][i][j] = "<"
                    elif (maze_y-1 >= i+1 and mazeWithNums[k][i+1][j]==next):
                        maze[k][i][j] = "v"
                    elif (0 <= i-1 and mazeWithNums[k][i-1][j]==next):
                        maze[k][i][j] = "^"
                    elif (maze_z-1 >= k+1 and mazeWithNums[k+1][i][j]==next):
                        maze[k][i][j] = "!"
                    elif (0 <= k-1 and mazeWithNums[k-1][i][j]==next):
                        maze[k][i][j] = "!"

    
nodeNumber = 0
#print(len(maze), len(maze[0]), len(maze[0][0]))
#print(x,y)
maze_z = len(maze)
maze_y = len(maze[0])
maze_x = len(maze[0][0])
for z in range(maze_z):
    for x in range(maze_y):
        for y in range (maze_x):
            if (maze[z][x][y] == "."):
                mazeWithNums[z][x][y] = nodeNumber
                nodeNumber += 1
            elif(maze[z][x][y] == "A"):
                mazeWithNums[z][x][y] = -1# Start            
            elif(maze[z][x][y] == "B"):
                mazeWithNums[z][x][y] = -2# Stop
for z in range(maze_z):
    for x in range(maze_y):
        for y in range (maze_x):
            if(maze[z][x][y]!= "#"):
                graph[mazeWithNums[z][x][y]] = findNeighbours(z, x, y)#make graph

# for debug
#for k in range(2):
#    for i in range(len(mazeWithNums[0])):
#        for j in range(len(mazeWithNums[0][0])):
#            print(mazeWithNums[k][i][j], end = " ")
#        print("")
#    print("\n\n")
#print(graph)

print("Dijkstra search started, please wait.")
print("Dijkstra terminated, Return code:", dijkstra (graph, -1, -2))# not complete yet!

route = [-2]
last_node = -2
while last_node !=- 1:
    route.insert(0, graph[last_node][3])
    last_node = route[0]
print("distance:", graph[-2][2])
print("sequence:\n", route)

len_route = len(route)
for i in range(len_route-1): 
    printPath(route[i], route[i+1])
    
for k in range(2): 
    for i in range(len(maze[0])):
        for j in range(len(maze[0][0])):
            print(maze[k][i][j], end = "")
        print("\n", end ="")
    print("\n")

#print("END OF GRAPH:\n#####################\n", graph)