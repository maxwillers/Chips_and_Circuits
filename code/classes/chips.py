"""This file contains the class Chip, which forms a chip with gates on them"""

<<<<<<< HEAD
from traceback import print_tb
=======
>>>>>>> 10648f2959b7e3a24df76f6087742cee4eae03c0
from code.classes.net import Net
from code.classes.gate import Gate
import pandas as pd

class Chip:
    """Class for creating chip"""

    def __init__(self, width, length, netlist, gate_coordinates):
        self.width = width 
        self.length = length 
        self.height = 7
        self.grid = [[[0 for _ in range(self.height + 1)] for _ in range(self.length + 1)] for _ in range(self.width + 1)]
        self.gates= []
        self.nets = []
        self.gate_coordinates = gate_coordinates
        self.netlist = [netlist["chip_a"].tolist(), netlist["chip_b"].tolist()]
        self.weights = {}
        self.add_gates()

    def add_gates(self):
        """create gates with id and connections"""
        id_gates = self.gate_coordinates['chip'].tolist()
        x_gates = self.gate_coordinates['x'].tolist()
        y_gates = self.gate_coordinates['y'].tolist()
        
        for i in range (len(id_gates)):
            gate = Gate(id_gates[i], x_gates[i], y_gates[i])
            
            # set gate value to -1 
            x = gate.x
            y = gate.y
            z = 0
            self.grid[x][y][z] = -1
            self.gates.append(gate)
            

    def available_neighbors(self, coordinates):
        """checks available neighbours for each position"""
        good_neighbors = []
        gate_neighbors = []
        intersect_neighbors = []

     
        x, y, z = coordinates
      
        # Check for each neighbour (a location on the grid) if they exist and if they are available
        for i in range(-1, 2, 2):
            
            # Check if the coordinates stay in the grid
            if x + i >= 0 and x + i <= self.width: 
                
                # If the location on the grid is free, it is a option or so-called "good neighbour"
                if self.grid[x + i][y][z] == 0:      
                    good_neighbors.append((x + i, y, z))

                
                # If the location on the grid is a gate, it might be the endpoint 
                elif self.grid[x + i][y][z] == -1:
                    gate_neighbors.append((x + i, y, z))
                else:
<<<<<<< HEAD
                    wire = self.grid[x + i][y][z]
                    if coordinates in wire:
=======
                    wires = self.grid[x + i][y][z]
                    if coordinates not in wires:
>>>>>>> 10648f2959b7e3a24df76f6087742cee4eae03c0
                        intersect_neighbors.append((x + i, y, z))
                    

            if y + i >= 0 and y + i <= self.length:
                if self.grid[x][y + i][z] == 0:
                    good_neighbors.append((x, y + i, z))
                elif self.grid[x][y + i][z] == -1:
                    gate_neighbors.append((x, y + i, z))
                else:
<<<<<<< HEAD
                    wire = self.grid[x][y + i][z]
                    if coordinates in wire:
                        intersect_neighbors.append((x, y + i, z))
            
=======
                    wires = self.grid[x][y + i][z]
                    if coordinates not in wires:
                        intersect_neighbors.append((x, y + i, z))
                    
                        
            # Check for neighbors with varying z coordinate
>>>>>>> 10648f2959b7e3a24df76f6087742cee4eae03c0
            if z + i >= 0 and z + i <= self.height:
                if self.grid[x][y][z + i] == 0:
                    good_neighbors.append((x, y, z + i))
                elif self.grid[x][y][z + i] == -1:
                    gate_neighbors.append((x, y, z + i))
                else:
<<<<<<< HEAD
                    wire = self.grid[x][y][z + i]
                    if coordinates in wire:
                        intersect_neighbors.append((x, y, z + i))

=======
                    wires = self.grid[x][y][z + i]
                    if coordinates not in wires:
                        intersect_neighbors.append((x, y, z + i))
                    
>>>>>>> 10648f2959b7e3a24df76f6087742cee4eae03c0
        
        # return list of tuples of all possible neighbours 
        return good_neighbors, gate_neighbors, intersect_neighbors

<<<<<<< HEAD
    
=======

    ########### Moet nog aangepast worden, maar is dit uberhaupt relevant???#############
>>>>>>> 10648f2959b7e3a24df76f6087742cee4eae03c0
    def get_violations(self):
        """Returns the violations if any of the nets cross eachother"""
        violations = []
        for x in range (self.width):
            for y in range (self.length):
                for z in range (self.height):
                    if self.grid[x][y][z] > 1:
                        violations.append((x, y, z))
        return violations


    def is_solution(self):
        """Returns True if all gates in netlist are connected"""
        start_gates = self.netlist["chip_a"].tolist()
        end_gates = self.netlist["chip_b"].tolist()

        for i in range(len(start_gates)):
            if self.gates[end_gates[i] -1].id not in self.gates[start_gates[i]-1].connections:
                return False
        return True
    
    def calculate_intersections(self):
        """Calculate how many intersections the chip has"""
        intersections = 0 
        for x in range(self.width):
            for y in range(self.length):
                for z in range(self.height):
<<<<<<< HEAD
                    if len(self.grid[x][y][z]) > 1:
                        intersections += 1
=======
                    
                    if self.grid[x][y][z] != 0 and self.grid[x][y][z] != -1:
                        if len(self.grid[x][y][z]) == 4:
                            intersections += 1
                        elif len(self.grid[x][y][z]) > 4:
                            intersections += len(self.grid[x][y][z]) - 4     
>>>>>>> 10648f2959b7e3a24df76f6087742cee4eae03c0
        return intersections

    def calculate_value(self):
        """Returns the cost of placing the wires"""
        value = 0
        for net in self.nets:
            value += (len(net.path) - 2)
        value = value + (300 * self.calculate_intersections())
        
        return value
    
    def df_output(self):
        """Returns the output in a dataframe"""
        wires =[]
        nets = []
        for net in self.nets:
            wires.append(net.path)
    
        for i in range (len(self.netlist[0])): 
            nets.append((self.netlist[0][i], self.netlist[1][i]))

        return pd.DataFrame(data = {'net': nets, 'wires' : wires})

<<<<<<< HEAD
    def cost(self, location, neighbor):
        choose, gates = self.available_neighbors(neighbor)
            
        self.weights[neighbor] = 300 * self.intersection(neighbor) 

        return self.weights[neighbor]


    def intersection(self, neighbor):
        intersections = 0
        counter = 0
        for z in range(self.height):
            if self.grid[neighbor[0]][neighbor[1]][z] > 0:
                counter += 1
        if counter > 1:
            intersections = intersections + (counter - 1)
        return intersections
=======

    def cost(self, neighbor):
        """Returns costs for the next step (used in astar algorithm)"""
        gates = self.available_neighbors(neighbor)[1]
            
        if gates:
            return self.weights.get(neighbor, 1) + 10 * len(gates) + 300 * self.intersection(neighbor)
        else:
            return self.weights.get(neighbor, 1) + 300 * self.intersection(neighbor) 

>>>>>>> 10648f2959b7e3a24df76f6087742cee4eae03c0
