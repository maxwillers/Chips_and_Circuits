# A* simple pseudocode
# Open list; the set nodes to be evaluated
# CLosed list; set of nodes already evaluated
# add the start node to OPENSSL_VERSION

# loop
#     current = node in Open list met de laagste f_cost (g+h)
#     remove current node from open list
#     add to close list

#     if current node = target node (path found)
#         return

#     for eacht neighbour of the current node
#         if neighbour not traversable or neighbour is in close_old_connections  
#             skip to next neighbour

#         if new path to neighbour is shorter (a, b, s example filmpje) or neighbour not in open
#             set f cost of neighbour
#             set parent of neighbour to current node (keeping track for retracing later on)
#             if neighbour is not in open
#                 add neighbour to open
#  we will be exited out of the loop when current == end node 

# als 2 neighbours zelfde f score, moet je algoritme eerste die pakken die als laatste ge add is
# algoritme niet stoppen voor de laatste stap; dus ookal is ht eindpunt al in "zicht", alsnog doorgaan met de loop, pas stoppen als de end == cuurent

# de open list is children a.k.a. possibilities; possible paths



# data structure that handles elements in order from a high to a low assigned priority
from queue import PriorityQueue

class State(object):
    """Base class that stores all the required components for a funcioning A* algorithm"""

    def __init__(self, value, parent, start = 0, goal = 0):

        # Initialize parameters
        self.parent = parent
        self.value = value

        # Initalize placeholder for the distance 
        self.distance = 0

        # Create a list to store all neighbouring possibilities
        self.neighbours = []

        # Check if the current position has a parent
        if parent:
            self.start = parent.start
            self.goal = parent.goal

            # Copy the parent path's list to our current one in order to keep track of where we're at
            self.path = parent.path[:]
            self.path.append(value)

        # No parent yet, so we create a list for the path and store our starting values
        else:
            self.path = [value]
            self.start = start
            self.goal = goal

    def getDistance(self):
        pass

    def generateChildren(self):
        pass

                    
class State_String(State):
    def __init__(self, value, parent, start=0, goal=0):

        # Initialize the base class in the sub class
        super(State_String, self).__init__(value, parent, start, goal)

        # Overwrite the placeholder from the base class with a function
        self.distance = self.getDistance()
    
    def getDistance(self):
        """Measures distance from our starting point on the grid to our goal"""

        # Check if goal has been reached, if so, return 0
        if self.value == self.goal:
            return 0
        distance = 0

        # TO DO: write algorithm to find the length between start and end coordinate

        # for i in range(len(self.goal)):
        #     letter = self.goal[i]
        #     try:
        #         distance += abs(i - self.value.index(letter))
        #     except:
        #         distance += abs(i - self.value.find(letter))
        # return distance

    def generateChildren(self):
        """Generates all possible moves that a path can make"""

        # Make sure children have not already been generated
        if not self.children:
            pass


def getDistance(startCoordinates, endCoordinates):
    """Calculates the distance with the Manhattan metric and returns the distance between two gates"""
    x1, y1, z1 = startCoordinates
    x1, y1, z1 = endCoordinates
    return abs(x1 - y1 -z1) + abs(x1 + y1 + z1)

def algorithm(grid, start, end):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))

    # Keep track of the path of the nodes
    cameFrom = {}

    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = getDistance

