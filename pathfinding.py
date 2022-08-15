import sys, pygame
import random
from collections import defaultdict

class Node:

    def __init__(self, walkable, x, y):
        self.x = x
        self.y = y
        self.isExplored = False
        # self.isWalkable = walkable
        self.isWalkable = 1

    def setWalkable(self, walkable):
        self.isWalkable = walkable

    def equals(self, node):

        if self.x == node.x and self.y == node.y and self.isWalkable == node.isWalkable:
            return True

        else:
            return False

    def __repr__(self):

        if self.isWalkable:
            return f"({self.x}, {self.y})"
        else:
            return f"[{self.x}, {self.y}]"

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

                dataRow.append(Node(True, x, y))

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

playspace = Grid(5, 5)

coolGrid()

for x in range(playspace.Yrange):

    print("[ ", end="")

    for y in range(playspace.Yrange):

        print(playspace.PLAYSPACE_GRID_LAYOUT[x][y], end=" ")
    
    print("]")

print("Please enter your x y coords for the start point: ")
startx = int(input("Enter X coord: "))
starty = int(input("Enter Y coord: "))

print("Please enter your x y coords for the end point: ")
endx = int(input("Enter X coord: "))
endy = int(input("Enter Y coord: "))

def pathfind(grid: Grid, root: Node, goal: Node):

    queue = LinkedList()
    explored = defaultdict(lambda: {"last_pos": None, "explored" : False})
    explored[root]["explored"] = True
    queue.insert(root)

    while (queue.head is not None):

        focus = queue.pop()

        if focus.equals(goal):
            return explored
        
        for node in grid.adjacentNodes(focus):
            if not explored[node]["explored"]:
                explored[node]["explored"] = True
                explored[node]["last_pos"] = focus
                queue.insert(node)

    return explored

pathfinded = pathfind(playspace, playspace.getNode(startx, starty), playspace.getNode(endx, endy))

path = []
discoveryStart = playspace.getNode(endx, endy)

while playspace.getNode(startx, starty) not in path:
    path.append(discoveryStart)
    discoveryStart = pathfinded[discoveryStart]['last_pos']

path.reverse()
print(path)
