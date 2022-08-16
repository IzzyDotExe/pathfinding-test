import sys, os
import random
import math
import time
from collections import defaultdict

DEBUG = False

# Higer = less walls
PATHFIND_WALL_DENSITY = 10

GRID_X_LENGTH = 50 
GRID_Y_LENGTH = 10

# Delay between performing different algorithms
ALGO_DELAY = 0

# Slows down the algorithm with more delay.
# Below 0.01 sometimes breaks things
ANIMATE_PATHFINDING = False
ANIM_FRAME_DELAY = 0.01

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isExplored = False
        self.isPath = False
        self.isWalkable = random.randrange(0, PATHFIND_WALL_DENSITY)
        self.isStart = False
        self.isEnd = False

    def setWalkable(self, walkable):
        self.isWalkable = walkable

    def equals(self, node):

        if self.x == node.x and self.y == node.y and self.isWalkable == node.isWalkable:
            return True

        else:
            return False

    def __repr__(self):

        if DEBUG:

            if self.isStart:
                return f"(S, S)"

            if self.isEnd:
                return f"(E, E)"

            if self.isPath:
                return f"(O, O)"

            if self.isExplored:
                return f"(X, X)"

            if self.isWalkable:
                return f"({self.x}, {self.y})"
            else:
                return f"[{self.x}, {self.y}]"

        else:

            if self.isStart:
                return "⛳"

            if self.isEnd:
                return "🏁"

            if self.isPath:
                return "🟨"

            if self.isExplored:
                return "🟦"

            if self.isWalkable:
                return "⬜️"
            else:
                return "⬛️"
                
class Grid:
    
    def __init__(self, dimensionsX, dimensionsY):

        self.PLAYSPACE_GRID_LAYOUT : list[list[Node]] = []
        self.Xrange : int = dimensionsX
        self.Yrange : int = dimensionsY

        self.createPlaceSpaceGrid()

    # Creates a basic grid structure populated with nodes.
    def createPlaceSpaceGrid(self):

        for y in range(self.Yrange):

            dataRow = []

            for x in range(self.Xrange):

                dataRow.append(Node(x, y))

            self.PLAYSPACE_GRID_LAYOUT.append(dataRow)
    
    def isWalkable(self, x, y):
        return self.PLAYSPACE_GRID_LAYOUT[y][x].isWalkable
    
    def setWalkable(self, x, y, value):
        self.PLAYSPACE_GRID_LAYOUT[y][x].setWalkable(value)

    def adjacentNodes(self, node: Node):

        adjacentNodes = []

        if node.y != self.Yrange-1:

            newnode : Node = self.PLAYSPACE_GRID_LAYOUT[node.y+1][node.x]

            if newnode.isWalkable:
                adjacentNodes.append(newnode)

        if node.x != self.Xrange-1:

            newnode : Node = self.PLAYSPACE_GRID_LAYOUT[node.y][node.x+1]

            if newnode.isWalkable:
                adjacentNodes.append(newnode)

        if node.y != 0:

            newnode : Node = self.PLAYSPACE_GRID_LAYOUT[node.y-1][node.x]

            if newnode.isWalkable:
                adjacentNodes.append(newnode)

        if node.x != 0:

            newnode : Node = self.PLAYSPACE_GRID_LAYOUT[node.y][node.x-1]

            if newnode.isWalkable:
                adjacentNodes.append(newnode)

        # random.shuffle(adjacentNodes)

        return adjacentNodes

    def getNode(self, x, y):
        return self.PLAYSPACE_GRID_LAYOUT[y][x]
    
    def calcDistance(self, start: Node, target: Node):
        return math.sqrt(pow(float(start.x) - float(target.x), 2) + pow(float(start.y) - float(target.y), 2))
    
    def toList(self):

        list = []

        for y in range(self.Yrange):

            for x in range(self.Xrange):
                
                list.append(self.PLAYSPACE_GRID_LAYOUT[y][x])
        
        return list

class LinkedList:
    
    def __init__(self):
        self.head = None

    def insert(self, data):
        insNode = LinkedListNode(data)
        if self.head is None:
            self.head = insNode
            return
        
        lastNode = self.head
        while(lastNode.nextValue):
            lastNode = lastNode.nextValue
        
        lastNode.nextValue = insNode

    def pop(self):

        if self.head is None:
            return None
        
        lastnode = self.head
        while (lastnode.nextValue):
            lastnode = lastnode.nextValue
        
        self.remove(lastnode.data)

        return lastnode.data

    def remove(self, key):
        Headval = self.head

        if (Headval is not None):
            if (Headval.data == key):
                self.head = Headval.nextValue
                Headval = None
                return
        while (Headval is not None):
            if Headval.data == key:
                break
            prev = Headval
            Headval = Headval.nextValue

        if Headval == None:
            return
        
        prev.nextValue = Headval.nextValue
        Headval = None

    def insertAt(self, node, data):

        if node is None:
            print("Node does not exist")
            return
        
        newNode = LinkedListNode(data)
        newNode.nextValue = node.nextValue
        node.nextValue = newNode

    def listprint(self):
        printval = self.head
        while printval is not None:
            print(printval.data)
            printval = printval.nextValue

    def toList(self):
        list = []
        val = self.head
        while val is not None:
            list.append(val.data)
            val = val.nextValue
        
        return list

class LinkedListNode:
    
    def __init__(self, data):
        self.nextValue = None
        self.data = data

playspace = Grid(GRID_X_LENGTH, GRID_Y_LENGTH)

def printPlayspace():

    for y in range(playspace.Yrange):

        print("", end="")

        for x in range(playspace.Xrange):

            print(playspace.PLAYSPACE_GRID_LAYOUT[y][x], end="")
        
        print("")

def bfsPathfind(grid: Grid, root: Node, goal: Node):

    queue = LinkedList()
    explored = defaultdict(lambda: {"last_pos": None, "explored" : False})
    explored[root]["explored"] = True
    root.isExplored = True
    queue.insert(root)

    while (queue.head is not None):

        if ANIMATE_PATHFINDING:
            os.system('cls' if os.name == 'nt' else 'clear')    
            printPlayspace()
            time.sleep(ANIM_FRAME_DELAY)

        focus = queue.pop()

        if focus.equals(goal):
            return explored
        
        for node in grid.adjacentNodes(focus):

            if not explored[node]["explored"]:
                explored[node]["explored"] = True
                explored[node]["last_pos"] = focus
                node.isExplored = True
                queue.insert(node)

                if node.equals(goal):
                    return explored

    return explored

def bfsTracePath():
    pathfinded = bfsPathfind(playspace, startpoint, endpoint)

    path = []
    discoveryStart = playspace.getNode(endx, endy)

    while playspace.getNode(startx, starty) not in path:
        try:
            discoveryStart.isPath = True
        except AttributeError:
            print("COULD NOT PATHFIND TO SPECIFIED LOCATION")
            exit()

        path.append(discoveryStart)
        discoveryStart = pathfinded[discoveryStart]['last_pos']

    path.reverse()
    return path

def getLowestFscore(nodes, explored):
    lowestF = nodes[0]

    for node in nodes:
        if explored[node]["fscore"] < explored[lowestF]["fscore"]:
            lowestF = node

    lowestFs = []
    lowestFs.append(lowestF)

    for node in nodes:
        if explored[node]["fscore"] == explored[lowestF]["fscore"] and not node.equals(lowestF):
            lowestFs.append(node)
    
    if len(lowestFs) > 1:
        for node in lowestFs:
            if explored[node]["hscore"] < explored[lowestF]["hscore"]:
                lowestF = node
    return lowestF

def astarPathFind(grid: Grid, root: Node, goal: Node):
    
    queue = LinkedList()

    explored = defaultdict(lambda: {"last_pos": None, "explored" : False, "gscore": math.inf, "hscore": math.inf, "fscore": math.inf})
    root.isExplored = True
    explored[root]["gscore"] = 0
    explored[root]["hscore"] = grid.calcDistance(root, goal)
    explored[root]["fscore"] = explored[root]["gscore"] + explored[root]["hscore"]

    queue.insert(root)

    while (queue.head is not None):

        if ANIMATE_PATHFINDING:
            os.system('cls' if os.name == 'nt' else 'clear')    
            printPlayspace()
            time.sleep(ANIM_FRAME_DELAY)
        
        nodes = queue.toList()
        
        current = getLowestFscore(nodes, explored)

        queue.remove(current)

        if current.equals(goal):
            return explored
        
        for node in grid.adjacentNodes(current):

            if not explored[node]["explored"]:

                gscore = explored[current]["gscore"] + grid.calcDistance(node, current)
                hscore = grid.calcDistance(node, goal)
                fscore = gscore + hscore

                explored[node]["last_pos"] = current
                explored[node]["gscore"] = gscore
                explored[node]["hscore"] = hscore
                explored[node]["fscore"] = fscore
                explored[node]["explored"] = True

                node.isExplored = True
                
                queue.insert(node)
            
                

    return explored

def astarTracePath():
    
    pathfinded = astarPathFind(playspace, startpoint, endpoint)

    path = []

    discoveryStart = playspace.getNode(endx, endy)

    while playspace.getNode(startx, starty) not in path:
        try:
            discoveryStart.isPath = True
        except AttributeError:
            print("COULD NOT PATHFIND TO SPECIFIED LOCATION")
            exit()
        path.append(discoveryStart)
        discoveryStart = pathfinded[discoveryStart]["last_pos"]
    
    path.reverse()
    return path     

def clearPathfindingData():
    for node in playspace.toList():
        node : Node = node
        if node.isExplored:
            node.isExplored = False
        
        if node.isPath:
            node.isPath = False

sPick = False
while not sPick:
    flush_input()

    printPlayspace()

    print("Please enter your x y coords for the start point: ")
    startx = int(input("Enter X coord: "))
    starty = int(input("Enter Y coord: "))

    startpoint = playspace.getNode(startx, starty)

    if not startpoint.isWalkable:
        os.system('cls' if os.name == 'nt' else 'clear')  
        print("Choose another spot! that spot is blocked off.")

        continue

    if not playspace.adjacentNodes(startpoint):
        os.system('cls' if os.name == 'nt' else 'clear')   
        print("Start point has nowhere to pathfind to, please choose a different space.") 

        continue

    startpoint.isStart = True

    os.system('cls' if os.name == 'nt' else 'clear')    
    printPlayspace()
    satisfied = str(input("Are you satisfied with this start location? (Y, N) "))

    if satisfied.lower()[0] == "y":

        sPick = True
        os.system('cls' if os.name == 'nt' else 'clear')    
    
    else: 

        startpoint.isStart = False
        os.system('cls' if os.name == 'nt' else 'clear')    

ePick = False
while not ePick:
    flush_input()

    printPlayspace()

    print("Please enter your x y coords for the end point: ")
    endx = int(input("Enter X coord: "))
    endy = int(input("Enter Y coord: "))

    endpoint = playspace.getNode(endx, endy)

    if not endpoint.isWalkable:
        os.system('cls' if os.name == 'nt' else 'clear')  
        print("Choose another spot! that spot is blocked off.")

        continue

    if not playspace.adjacentNodes(endpoint):
        os.system('cls' if os.name == 'nt' else 'clear')   
        print("Start point has nowhere to pathfind to, please choose a different space.") 

        continue

    endpoint.isEnd = True

    os.system('cls' if os.name == 'nt' else 'clear')    
    printPlayspace()
    satisfied = str(input("Are you satisfied with this end location? (Y, N) "))

    if satisfied.lower()[0] == "y":

        ePick = True
        os.system('cls' if os.name == 'nt' else 'clear')    
    
    else: 

        endpoint.isEnd = False
        os.system('cls' if os.name == 'nt' else 'clear')    

# bfsPathfind(playspace, startpoint, endpoint)
# bfsTracePath()
astarTracePath()

os.system('cls' if os.name == 'nt' else 'clear')
print("A* PATHFINDING")
printPlayspace()

time.sleep(ALGO_DELAY)

clearPathfindingData()

bfsTracePath()

print("BFS PATHFINDING")
printPlayspace()


# print(playspace.calcDistance(startpoint, endpoint))
