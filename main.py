from decimal import Decimal

pathCount = 0
pathList = []
stationCount = 0
maxArriveTime = 0

#Node class, representing route
class Node:
    pT = 0  # Probability of normal departure
    pF = 1 - pT  # Probability of strikes
    startStation = 0  # Route departure station
    endStation = 0  # Route Destination Site
    startTime = 0  # Departure time
    endTime = 0  # Arrival time
    leftNode = None  # Left Subtree
    rightNodes = []  # Right Subtree

    def __init__(self, startStation, endStation, startTime, endTime, pT):
        self.startStation = int(startStation)
        self.endStation = int(endStation)
        self.startTime = int(startTime)
        self.endTime = int(endTime)
        self.pT = Decimal(pT)
        self.pF = Decimal(1.0) - self.pT

    def prt(self):
        print(self.startStation, self.endStation, self.startTime, self.endTime, self.pT, self.pF)

def printNodes(list):
    for node in list:
        node.prt()

#Load input data. /input1.txt
def loadInput(path):
    pathList = []
    f = open(path)
    ln = 0
    for line in f:
        if ln == 0:
            pathCount, stationCount = line.split()
        else:
            if ln == 1:
                maxArriveTime = line
            else:
                startStation, endStation, startTime, endTime, pT = line.split()
                node = Node(startStation, endStation, startTime, endTime, pT)
                pathList.append(Node(node.startStation, node.endStation, node.startTime, node.endTime, node.pT))
        ln = ln + 1
    f.close()
    return pathCount, stationCount, pathList, maxArriveTime

# Find a route starting from startStation
def findNodeStartAs(startStation, lastEndTime):
    stations = []
    for node in pathList:
        if (node.startStation == startStation and node.startTime > lastEndTime):
            stations.append(node)
    return stations

# Building a tree from a timetable
def buildTree(node):
    if node:
        # Fallback finds all routes starting from the last departure and adds them all to the right subtree
        rightStations = findNodeStartAs(node.startStation, node.startTime)

        # Find all the routes starting from the current station and select the first as the left subtree
        leftStations = findNodeStartAs(node.endStation, node.endTime)
        if len(leftStations) > 0:
            leftNode = leftStations[0]

        # No matter what the probability is, the first departure car is set to leftNode
        if node.endStation != 1:
            node.leftNode = leftNode
        # Construct left subtree recursively
        buildTree(node.leftNode)

        # Since the departure probability is less than 1, other considerations are needed, so a right subtree is added.
        if node.pT < 1:
            node.rightNodes = rightStations
            # Recursively build right subtree
            for rnode in node.rightNodes:
                buildTree(rnode)

# Calculate maximum probability
def caculateProbability(node):
    if node == None:
        return 0

    # Recursively find the maximum probability value of the right subtree, that is, the maximum probability value of the departure failure and transfer
    rightNodesP = []
    rightP = 0;
    if node.rightNodes and len(node.rightNodes) > 0:
        for rnode in node.rightNodes:
            rightNodesP.append(caculateProbability(rnode))
            rightP = max(rightNodesP)

    # Recursively find the maximum probability value of the left subtree, that is, the normal departure probability value
    leftP = 1;
    if node.leftNode:
        leftP = caculateProbability(node.leftNode)
    else:
        leftP = 1

    # Left subtree probability plus right subtree probability
    return node.pT * leftP + node.pF * rightP

# Step1: Read input samples
path = input("Enter Input File :")
pathCount, stationCount, pathList, maxArriveTime = loadInput("./"+path)

# Step2: Construct a virtual initial node
initNode = Node(0, 0, 0, -1, 1)

# Step3: Execute the method to construct the tree
buildTree(initNode)

# Step4: Execute the method of calculating probability
print("Sample output:",caculateProbability(initNode))
