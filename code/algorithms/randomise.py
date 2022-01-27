"""
This file contains the Random class which implements a random algorithm for finding paths between chips.
"""
import sys 
from calendar import c
import random
import copy
from tracemalloc import start

import jinja2
from code.classes import chips
from code.classes.chips import Chip
from code.classes.net import Net

#sys.setrecursionlimit(5000)

class Random:

    def __init__(self, chip):
        self.chip = copy.deepcopy(chip)
        self.create_netlist()
        

    def create_netlist(self):
        """Go over all connection that need to be made and ensure they are made"""
        

        # Iterate over the netlist
        for i in range(len(self.chip.netlist[0])):
            print(f"chip {i + 1}: {self.random_path(self.chip.gates[self.chip.netlist[0][i]-1], self.chip.gates[self.chip.netlist[1][i] -1])}")
                
        
    
    def random_path(self, start_gate, end_gate):
        """
        Assign each net with a randomized path
        """
        flag = False

        path = [] 
           
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
            
            
            # iterate over possible neighbour gates
            for end in gates:

                # If the current coordinates match the end gate coordinate, check if the coordinates are unique
                if end == end_coordinates:
                    
                    # if the coordinates are unique, create net
                    if len(path) == len(set(path)):
                        path.append(end)
                        for i in range(len(path)):
                            x, y, z = path[i]
                            if self.chip.grid[x][y][z] != -1:
                                self.chip.grid[x][y][z] = ((path[i - 1]), (path[i + 1]))
                            
                        net = Net(path)
                        start_gate.connections.append(end_gate.id)
                        end_gate.connections.append(start_gate.id)
                        self.chip.nets.append(net)
                        for i in range(len(path)):
                            x, y, z = path[i]
                            print(self.chip.grid[x][y][z])
                        return print(f"double check {current_coordinates}, {end_coordinates}") 
                    
                    # if coordinates are not unique, delete the coordinates and start over
                    else:
                        path.clear()
                        try:
                            return self.random_path(start_gate, end_gate)
                        except RecursionError:
                            print("stuck")
                            quit() 
    

            # if there are neighbours available pick one randomly
            if choose: 
            
                new_line = random.choice(choose)

                # Keep track of the lines which have been laid
                path.append(new_line)

                # Keep track of the current position
                current_coordinates = new_line

                flag == False

            # If there are no neighbours available, run the function again
            elif len(choose) == 0 and len(intersections) > 0 and flag == False:
                new_line = random.choice(intersections)

                path.append(new_line)

                current_coordinates = new_line
                print('whaaat')

                flag = True


            else:
                # if possible try again to find a connection
                try:
                    return self.random_path(start_gate, end_gate)

                # if a recursion error is occurring quit the program
                except RecursionError:
                    print('stuck')
                    quit()     
