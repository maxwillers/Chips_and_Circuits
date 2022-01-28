"""This file contains the class Chip, which forms a chip with gates on them"""

from traceback import print_tb
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
        self.connections = []
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
                    if self.grid[x][y][z] == 0 or self.grid[x][y][z] == -1:
                        gate_neighbors.append((x + i, y, z))
                    elif (x + i, y , z) not in self.grid[x][y][z]:
                        gate_neighbors.append((x + i, y, z))
                else:
                    wire = self.grid[x + i][y][z]
                    if coordinates not in wire:
                        intersect_neighbors.append((x + i, y, z))
                    
            # Check for neighbors with varying y coordinate
            if y + i >= 0 and y + i <= self.length:
                if self.grid[x][y + i][z] == 0:
                    good_neighbors.append((x, y + i, z))
                
                elif self.grid[x][y + i][z] == -1:
                    if self.grid[x][y][z] == 0 or self.grid[x][y][z] == -1:
                        gate_neighbors.append((x, y + i, z))
                    elif (x, y + i, z) not in self.grid[x][y][z]:
                        gate_neighbors.append((x, y + i, z))
                else:
                    wire = self.grid[x][y + i][z]
                    if coordinates not in wire:
                        intersect_neighbors.append((x, y + i, z))
            
            # Check for neighbors with varying z coordinate
            if z + i >= 0 and z + i <= self.height:
                if self.grid[x][y][z + i] == 0:
                    good_neighbors.append((x, y, z + i))
                elif self.grid[x][y][z + i] == -1:
                    if self.grid[x][y][z] == 0 or self.grid[x][y][z] == -1:
                        gate_neighbors.append((x, y, z + i))
                    elif (x, y, z + i) not in self.grid[x][y][z]:
                        gate_neighbors.append((x, y, z + i))
                else:
                    wire = self.grid[x][y][z + i]
                    if coordinates not in wire:
                        intersect_neighbors.append((x, y, z + i))

        
        # return list of tuples of all possible neighbours 
        return good_neighbors, gate_neighbors, intersect_neighbors

    
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
                    if self.grid[x][y][z] != 0 and self.grid[x][y][z] != -1:
                        if len(self.grid[x][y][z][0]) == 2 :
                            intersections += 1
        print(f"intersections: {intersections}")
        return intersections

    def calculate_value(self):
        """Returns the cost of placing the wires"""
        value = 0
        for net in self.nets:
            value = value + (len(net.path) - 2)
        print(f"value:{value}")
        print(f"intersections:{self.calculate_intersections()}")
        value = value + (300 * self.calculate_intersections())
        
        return value
    
    def df_output(self):
        """Returns the output in a dataframe"""
        wires =[]
        nets = []
        for net in self.nets:
            wires.append(net.path)
    
        for connection in self.connections: 
            nets.append((connection['start_gate'].id, connection['end_gate'].id))

        return pd.DataFrame(data = {'net': nets, 'wires' : wires})

    def cost(self, neighbor):


        choose, gates, intersections = self.available_neighbors(neighbor)
            
        # self.weights[neighbor] = 300 * self.intersection(neighbor) 
        if gates:
            return self.weights.get(neighbor, 1) + 10 * len(gates)
        else:
            return self.weights.get(neighbor, 1)


    def intersection(self, neighbor):
        intersections = 0
        counter = 0
        for z in range(self.height):
            if self.grid[neighbor[0]][neighbor[1]][z] > 0:
                counter += 1
        if counter > 1:
            intersections = intersections + (counter - 1)
        return intersections


