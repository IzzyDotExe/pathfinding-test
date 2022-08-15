import sys, os
import random
import time
from collections import defaultdict

DEBUG = False

# Higer = less walls
PATHFIND_WALL_DENSITY = 3

GRID_X_LENGTH = 50 
GRID_Y_LENGTH = 10

ANIMATE_PATHFINDING = True
ANIM_FRAME_DELAY = 0.05

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

class LinkedListNode:
    
    def __init__(self, data):
        self.nextValue = None
        self.data = data


"""
def coolGrid():

    playspace.PLAYSPACE_GRID_LAYOUT[1][3].setWalkable(0)
    playspace.PLAYSPACE_GRID_LAYOUT[1][4].setWalkable(0)
    playspace.PLAYSPACE_GRID_LAYOUT[2][4].setWalkable(0)
    playspace.PLAYSPACE_GRID_LAYOUT[0][1].setWalkable(0)
    playspace.PLAYSPACE_GRID_LAYOUT[1][1].setWalkable(0)
    playspace.PLAYSPACE_GRID_LAYOUT[2][1].setWalkable(0)
    playspace.PLAYSPACE_GRID_LAYOUT[3][1].setWalkable(0)
    playspace.PLAYSPACE_GRID_LAYOUT[1][0].setWalkable(0)
    playspace.PLAYSPACE_GRID_LAYOUT[2][0].setWalkable(0)
    playspace.PLAYSPACE_GRID_LAYOUT[4][0].setWalkable(0)
"""

playspace = Grid(GRID_X_LENGTH, GRID_Y_LENGTH)

# coolGrid()

def printPlayspace():

    for y in range(playspace.Yrange):

        print("", end="")

        for x in range(playspace.Xrange):

            print(playspace.PLAYSPACE_GRID_LAYOUT[y][x], end="")
        
        print("")

# printPlayspace()

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


def pathfind(grid: Grid, root: Node, goal: Node):

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

    return explored


endpoint = playspace.getNode(endx, endy)

endpoint.isEnd = True
pathfinded = pathfind(playspace, startpoint, endpoint)

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

os.system('cls' if os.name == 'nt' else 'clear')    
printPlayspace()
