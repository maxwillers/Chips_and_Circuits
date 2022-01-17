"""
chips.py
This file contains the class Chip which forms a chip with gates on them
"""
from code.classes.net import Net
from code.classes.gate import Gate

class Chip:
    """Class for creating chip"""

    def __init__(self, width, length, netlist, gate_coordinates):
        self.width = width
        self.length = length
        self.height = 7
        self.grid =  [[[0 for _ in range(self.width)] for _ in range(self.length)] for _ in range(self.height)]
        self.gates= []
        self.nets = []
        self.intersections = []
        self.gate_coordinates = gate_coordinates
        self.netlist = [netlist["chip_a"].tolist(), netlist["chip_b"].tolist()]
        self.add_gates()


    def add_gates(self):
        """create gates with id and connections"""
        id_gates = self.gate_coordinates['chip'].tolist()
        x_gates = self.gate_coordinates['x'].tolist()
        y_gates = self.gate_coordinates['y'].tolist()
        
        for i in range (len(id_gates)):
            gate = Gate(id_gates[i], x_gates[i], y_gates[i])
            self.gates.append(gate)
    

    def available_neighbours(self, coordinates):
        """checks available neighbours for each position"""
        good_neighbours = []
        x, y, z = coordinates
        
        # check for each neighbour if they are available and exist
        for i in range(-1, 1, 2):
            if self.grid[x + i][y][z] == 0:      
                good_neighbours.append((x + i, y, z))
            if self.grid[x][y + i][z] == 0:
                good_neighbours.append((x, y + i, z))
            if self.grid[x][y][z + i] == 0:
                good_neighbours.append((x, y, z + i))
        
        # return list of tuples of all possible neighbours 
        return good_neighbours 

    
    def get_violations(self):
        """Returns if any of the nets cross eachother"""
        violations = []
        for x in range (self.width):
            for y in range (self.length):
                for z in range (self.height):
                    if self.grid[x][y][z] > 1:
                        violations.append((x,y,z))
        return violations


    def is_solution(self):
        """Returns if all gates in netlist are connected"""
        start_gates = self.netlist["chip_a"].tolist()
        end_gates = self.netlist["chip_b"].tolist()

        for i in range(len(start_gates)):
            if self.gates[end_gates[i] -1].id not in self.gates[start_gates[i]-1].connections:
                return False

        return True
    
    
    def calculate_value(self):
        """Returns the cost of placing the wires"""
        value = 300
        for net in self.nets:
            value += len(net.path)
        value = value * len(self.intersections)
        
        return value
      

    
    