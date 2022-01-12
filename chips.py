"""
chips.py
This file contains the class Chip which forms a chip with gates on them
"""
from net import Net

class Chip:
    """Class for creating chip"""

    def __init__(self, netlist, gate_coordinates):
        # self.x = x
        # self.y = y
        #self.grid = [[None for _ in range(self.x)] for _ in range(self.y)]
        self.netlist = netlist
        self.gates= [gate_coordinates['x'].tolist(), gate_coordinates['y'].tolist()]
        self.nets = []
        self.create_netlist()
    
    def create_netlist(self):
        start_gate = self.netlist["chip_a"].tolist()
        end_gate = self.netlist["chip_b"].tolist()

        for i in range (len(start_gate)):
            start_coordinate = [self.gates[0][start_gate[i]-1], self.gates[1][start_gate[i]-1]]
            end_coordinate = [self.gates[0][end_gate[i]-1], self.gates[1][end_gate[i]-1]]
            self.add_net(start_coordinate, end_coordinate)
            
       
    def add_net(self, start_coordinate, end_coordinate):
        """create a new net path between two gates"""
        # Create a path variable and add starting coordinate
        x= start_coordinate[0]
        y = start_coordinate[1]
        path = [(x,y)]
        
        # Calculate the difference between the x and y coordinates of the start and end
        dx = end_coordinate[0] - x
        dy = end_coordinate[1] - y

        # Look if df is negative of not to decide which way to go
        if dx > 0:
            i = 1
        else:
            i = -1

        if dy > 0:
            j = 1
        else:
            j = -1

        # Change the x coordinate till end x coordinate is reached
        for _ in range(abs(dx)): 
            x = x + i  
            path.append((x ,y))

        #Change y coordinate till y coordinate is reached
        for _ in range(abs(dy)):
            y = y + j
            path.append((x,y))

        # Create net
        net = Net(path)
        self.nets.append(net)
      
    
    