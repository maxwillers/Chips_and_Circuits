"""
chips.py
This file contains the class Chip which forms a chip with gates on them
"""
from net import Net

class Chip:
    """Class for creating chip"""

    def __init__(self, width, length, netlist, gate_coordinates):
        self.width = width
        self.length = length
        self.height = 7
        self.grid =  [[[None for _ in range(self.width)] for _ in range(self.length)] for _ in range(self.height)]
        self.netlist = netlist
        self.gates= [gate_coordinates['x'].tolist(), gate_coordinates['y'].tolist()]
        self.nets = []
        self.create_netlist()
    
    def create_netlist(self):
        """ensure paths are made between the gates as listed in netlist"""
        start_gate = self.netlist["chip_a"].tolist()
        end_gate = self.netlist["chip_b"].tolist()

        
        for i in range (len(start_gate)):
            # get coordinates of start gate en end gate and make a net between them
            start_coordinate = [self.gates[0][start_gate[i]-1], self.gates[1][start_gate[i]-1]]
            end_coordinate = [self.gates[0][end_gate[i]-1], self.gates[1][end_gate[i]-1]]
            self.add_net(start_coordinate, end_coordinate)
            
       
    def add_net(self, start_coordinate, end_coordinate):
        """create a new net path between two gates"""
        # Create a path variable and add starting coordinate
        x= start_coordinate[0]
        y = start_coordinate[1]
        z = 0
        path = [(x,y,z)]

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
            x_new = x + i 
            z_new = z - 1
            
            # Make sure z goes down again if possible
            while z != 0 and self.grid[x][y][z_new] != None:
                z_new = z - 1
                z = z_new
                path.append((x ,y, z))
                self.grid[x][y][z] = 1
            
            # Change x if possible otherwise go up
            while self.grid[x_new][y][z] != None and z < self.height :
                z +=1
                path.append((x ,y, z))
                self.grid[x][y][z] = 1 
                
            x = x_new 
            path.append((x ,y, z)) 
            self.grid[x][y][z] = 1    

        #Change y coordinate till y coordinate is reached
        for _ in range(abs(dy)):
            y_new = y + j
            z_new = z - 1
            
            # Make sure z goes down again if possible
            while z != 0 and self.grid[x][y][z_new] != None:
                z_new = z - 1
                z = z_new
                path.append((x ,y, z))
                self.grid[x][y][z] = 1
            
            # Change y if possible otherwise go up
            while self.grid[x][y_new][z] != None and z < self.height :
                z +=1
                path.append((x ,y, z))
                self.grid[x][y][z] = 1 
                
            y = y_new 
            path.append((x ,y, z))
            self.grid[x][y][z] = 1 
        
        # Make sure the line goes to base layer if right x and y coordinates are reached
        if z != 0:
            z=0
            path.append((x ,y, z))
            self.grid[x][y][z] = 1 
            
        # Create net
        net = Net(path)
        self.nets.append(net)
      
    
    