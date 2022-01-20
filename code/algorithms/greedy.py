"""
greedy.py
This file contains the class greedy class which implements a greedy alogrithm for finding paths
This greedy algorithm based on Manhattan distance.
"""
import copy
from code.classes.net import Net

class Greedy:
    """
    The Greedy class that assigns the best possible value to each node one by one.
    """

    def __init__(self, chip):
        self.chip = copy.deepcopy(chip)
        self.create_netlist()
        
    def create_netlist(self):
        """Go over all connection that need to be made and ensure they are made"""
        for i in range (len(self.chip.netlist[0])):
            self.add_connection(self.chip.gates[self.chip.netlist[0][i]-1], self.chip.gates[self.chip.netlist[1][i] -1]) 

    def add_connection(self, start_gate, end_gate):
        """Make the connection between two gates first changing the x coordinates then the y coordinates"""
        start_gate = start_gate
        end_gate = end_gate
            
        x= start_gate.x
        y = start_gate.y
        z = 0
        path = [(x,y,z)]
        
        dx = end_gate.x - x
        dy = end_gate.y - y

        # Look if dx is negative of not to decide which way to go
        if dx > 0:
            i = 1
        elif dx == 0:
            i = 0
        else:
            i = -1

        if dy > 0:
            j = 1
        elif dy == 0:
            j = 0
        else:
            j = -1

        # Change the x coordinate till end x coordinate is reached
        for _ in range(abs(dx)): 
            x_new = x + i 
            z_new = z - 1
            
            # Make sure z goes down again if possible
            while z != 0 and self.chip.grid[x][y][z_new] == 0:
                z = z_new
                path.append((x ,y, z))
                self.chip.grid[x][y][z] += 1
                z_new = z - 1
           
            # Change x if possible otherwise go up
            while self.chip.grid[x_new][y][z] > 0 and z < self.chip.height :
                z +=1
                path.append((x ,y, z))
                self.chip.grid[x][y][z] += 1 
                    
            x = x_new 
            path.append((x ,y, z)) 
            self.chip.grid[x][y][z] += 1    

        # Change y coordinate till y coordinate is reached
        for _ in range(abs(dy)):
            y_new = y + j
            z_new = z - 1
                
            # Make sure z goes down again if possible
            while z != 0 and self.chip.grid[x][y][z_new] == 0:
                z = z_new
                path.append((x ,y, z))
                self.chip.grid[x][y][z] += 1
                z_new = z - 1
                
            # Change y if possible otherwise go up
            while self.chip.grid[x][y_new][z] > 0 and z < self.chip.height :
                z +=1
                path.append((x ,y, z))
                self.chip.grid[x][y][z] += 1 
                    
            y = y_new 
            path.append((x ,y, z))
            self.chip.grid[x][y][z] += 1 
            
        # Make sure the line goes to base layer if right x and y coordinates are reached
        if z != 0:
            z=0
            path.append((x ,y, z))
            self.chip.grid[x][y][z] += 1 
                
        # Create net
        net = Net(path)
        start_gate.connections.append(end_gate.id)
        end_gate.connections.append(start_gate.id)
        self.chip.nets.append(net)
