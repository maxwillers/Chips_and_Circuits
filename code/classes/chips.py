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
        self.create_netlist()

    def add_gates(self):
        """create gates with id and connections"""
        id_gates = self.gate_coordinates['chip'].tolist()
        x_gates = self.gate_coordinates['x'].tolist()
        y_gates = self.gate_coordinates['y'].tolist()
        
        for i in range (len(id_gates)):
            gate = Gate(id_gates[i], x_gates[i], y_gates[i])
            self.gates.append(gate)
  
    # def create_netlist(self):
    #     """ensure paths are made between the gates as listed in netlist"""
    #     start_gate = self.netlist["chip_a"].tolist()
    #     end_gate = self.netlist["chip_b"].tolist()

    #     for i in range (len(start_gate)):
    #         self.add_net(self.gates[start_gate[i]-1], self.gates[end_gate[i] -1])       
       
    # def add_net(self, start_gate, end_gate):
    #     """create a new net path between two gates"""
    #     # Create a path variable and add starting coordinate
    #     x= start_gate.x
    #     y = start_gate.y
    #     z = 0
    #     path = [(x,y,z)]

    #     # Calculate the difference between the x and y coordinates of the start and end
    #     dx = end_gate.x - x
    #     dy = end_gate.y - y


    #     # Look if df is negative of not to decide which way to go
    #     if dx > 0:
    #         i = 1
    #     else:
    #         i = -1

    #     if dy > 0:
    #         j = 1
    #     else:
    #         j = -1

    #     # Change the x coordinate till end x coordinate is reached
    #     for _ in range(abs(dx)): 
    #         x_new = x + i 
    #         z_new = z - 1
            
    #         # Make sure z goes down again if possible
    #         while z != 0 and self.grid[x][y][z_new] == 0:
    #             z = z_new
    #             path.append((x ,y, z))
    #             self.grid[x][y][z] += 1
    #             z_new = z - 1
            
    #         # Change x if possible otherwise go up
    #         while self.grid[x_new][y][z] > 0 and z < self.height :
    #             z +=1
    #             path.append((x ,y, z))
    #             self.grid[x][y][z] += 1 
                
    #         x = x_new 
    #         path.append((x ,y, z)) 
    #         self.grid[x][y][z] += 1    

    #     #Change y coordinate till y coordinate is reached
    #     for _ in range(abs(dy)):
    #         y_new = y + j
    #         z_new = z - 1
            
    #         # Make sure z goes down again if possible
    #         while z != 0 and self.grid[x][y][z_new] == 0:
    #             z = z_new
    #             path.append((x ,y, z))
    #             self.grid[x][y][z] += 1
    #             z_new = z - 1
            
    #         # Change y if possible otherwise go up
    #         while self.grid[x][y_new][z] > 0 and z < self.height :
    #             z +=1
    #             path.append((x ,y, z))
    #             self.grid[x][y][z] += 1 
                
    #         y = y_new 
    #         path.append((x ,y, z))
    #         self.grid[x][y][z] += 1 
        
    #     # Make sure the line goes to base layer if right x and y coordinates are reached
    #     if z != 0:
    #         z=0
    #         path.append((x ,y, z))
    #         self.grid[x][y][z] += 1 
            
    #     # Create net
    #     net = Net(path)
    #     start_gate.connections.append(end_gate.id)
    #     end_gate.connections.append(start_gate.id)
    #     self.nets.append(net)

    
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
      

    
    