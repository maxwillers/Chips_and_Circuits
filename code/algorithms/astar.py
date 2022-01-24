
# data structure that handles elements in order from a high to a low assigned priority
import copy
from code.classes.net import Net
from queue import PriorityQueue


class Astar(object):
    """Base class that stores all the required components for a funcioning A* algorithm"""

    def __init__(self, chip, value, parent, start_gate = 0, end_gate = 0):
        self.chip = copy.deepcopy(chip)
        self.create_netlist()

        # Initialize parameters
        self.parent = parent
        self.value = value

        # Initalize placeholder for the distance 
        self.distance = 0

        # Create a list to store all neighbouring possibilities
        self.neighbours = []

        # Check if the current position has a parent
        if parent:
            self.start_gate = parent.start_gate
            self.end_gate = parent.goal

            # Copy the parent path's list to our current one in order to keep track of where we're at
            self.path = parent.path[:]
            self.path.append(value)

        # No parent yet, so we create a list for the path and store our starting values
        else:
            self.path = [value]
            self.start = start_gate
            self.goal = end_gate


    def create_netlist(self):
        """Go over all the connections that need to be made and ensure that they are made"""
        for i in range(len(self.chip.netlist[0])):
            self.add_connection(self.chip.gates[self.chip.netlist[0][i]-1], self.chip.gates[self.chip.netlist[1][i]-1])


    def getDistance(self):
        pass


    def generateChildren(self):
        pass


class CreatePath(Astar):
    def __init__(self, value, parent, start_gate = 0, end_gate = 0):

        # Initialize the base class in the sub class
        super(CreatePath, self).__init__(value, parent, start_gate, end_gate)

        # Overwrite the placeholder from the base class with a function
        self.distance = self.getDistance()
    

    def getDistance(self, start_gate, end_gate):
        """Calculates the distance with the Manhattan metric and returns the distance between two gates"""
        """Constitutes the h in the formula f(n) = g(n) + h(n)"""
        x1, y1, z1 = start_gate
        x1, y1, z1 = end_gate
        return abs(x1 - y1 -z1) + abs(x1 + y1 + z1)
   
    

# TO DO: algorithm for calculating both g and f
    def generateChildren(grid, start_gate, end_gate):
        count = 0
        openSet = PriorityQueue()
        openSet.put((0, count, start_gate))

        # Keep track of the path of the nodes
        cameFrom = {}

        g_score = {spot: float("inf") for row in grid for spot in row}
        g_score[start_gate] = 0
        f_score = {spot: float("inf") for row in grid for spot in row}
        f_score[start_gate] = getDistance(start_gate)


        

    # Create a net on the chip
    net = Net(path)
    start_gate.connections.append(end_gate.id)
    end_gate.connections.append(start_gate.id)
    self.chip.nets.append(net)