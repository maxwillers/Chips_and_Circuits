"""
This file contains the Random class which implements a random algorithm for finding paths between chips.
"""
import sys 
from calendar import c
import random
import copy
from tracemalloc import start

import jinja2
from code.algorithms.sorting import manhatan_dis_sort
from code.classes import chips
from code.classes.chips import Chip
from code.classes.net import Net

sys.setrecursionlimit(5000)


def run_random(self):
    """Go over all connection that need to be made and ensure they are made"""
    
    
    # Iterate over the netlist
    for i in range(len(self.chip.netlist[0])):
        self.chip.connections.append((self.chip.gates[self.chip.netlist[0][i]-1], self.chip.gates[self.chip.netlist[1][i] -1])) 
    
    self.chip.connections = manhatan_dis_sort(self.chip.connections)
            
    for connection in self.chip.connections:
        start_gate = connection['start_gate']
        end_gate = connection['end_gate']

        path = self.random_path(start_gate, end_gate)
        for i in range(len(path)):
            x, y, z = path[i]
            if self.chip.grid[x][y][z] != -1: 
                if self.chip.grid[x][y][z] == 0:
                    self.chip.grid[x][y][z] = [(path[i - 1]), (path[i + 1])]
                else:
                    self.chip.grid[x][y][z] = self.chip.grid[x][y][z] + [(path[i - 1]), (path[i + 1])]
        
        net = Net(path) 
        start_gate.connections.append(end_gate.id)
        end_gate.connections.append(start_gate.id)
        self.chip.nets.append(net)
               
    

def random_path(chip, start_gate, end_gate):
    """
    Assign each net with a randomized path
    """
    path = [] 
    set_path = set(path)
    counter = 0
    sx = start_gate.x
    sy = start_gate.y
    sz = 0

    current_coordinates = (sx, sy, sz)

    ex = end_gate.x
    ey = end_gate.y 
    ez = 0

    end_coordinates = (ex, ey, ez)

    path.append(current_coordinates)

    # While the connection has not been made, make random choices for a new line  
    while current_coordinates != end_coordinates:

        # If there are neighbour points available, make a random choice between these neighbouring points
        choose, gates, intersections = self.chip.available_neighbors(current_coordinates)
        
        choose.extend(intersections)
        # iterate over possible neighbour gates
        for end in gates:

            # If the current coordinates match the end gate coordinate, check if the coordinates are unique
            if end == end_coordinates:
                path.append(end)
                return path
            
        # if there are neighbours available pick one randomly
        if choose: 
            

            new_line = random.choice(choose)

            # Keep track of the lines which have been laid
            
            if new_line not in set_path:
                path.append(new_line)
                set_path.add(new_line)

                
                current_coordinates = new_line
            # Keep track of the current position
            
            elif counter == 1000:
                try:
                    return self.random_path(start_gate, end_gate)

                # if a recursion error is occurring quit the program
                except RecursionError:
                    print('stuck')
                    quit()     
            else:
                counter += 1

        else:
            # if possible try again to find a connection
            try:
                return self.random_path(start_gate, end_gate)

            # if a recursion error is occurring quit the program
            except RecursionError:
                print('stuck')
                quit()  


