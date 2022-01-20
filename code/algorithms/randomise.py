from calendar import c
import random
import copy
from tracemalloc import start

import jinja2
from code.classes import chips
from code.classes.chips import Chip
from code.classes.net import Net


class Random:

    def __init__(self, chip):
        self.chip = copy.deepcopy(chip)
        self.create_netlist()
        

    def create_netlist(self):
        """Go over all connection that need to be made and ensure they are made"""
        # iterate over netlist
        for i in range(len(self.chip.netlist[0])):
            self.random_path(self.chip.gates[self.chip.netlist[0][i]-1], self.chip.gates[self.chip.netlist[1][i] -1])
            print(i)


    def random_path(self, start_gate, end_gate):
        """
        Assign each net with a randomized path
        """
        flag = True

        lines = [] 
           
        sx = start_gate.x
        sy = start_gate.y
        sz = 0

        current_coordinates = (sx, sy, sz)

        ex = end_gate.x
        ey = end_gate.y 
        ez = 0

        end_coordinates = (ex, ey, ez)

        # while the connection has not been made, make random choices for a new line  
        while current_coordinates != end_coordinates:

            # if there are neighbour points available make a random choice 
            choose, gates = self.chip.available_neighbours(current_coordinates)
            
            
            # iterate over possible neighbour gates
            for end in gates:

                # if coordinates match end gate coordinate, create net
                if end == end_coordinates:
                    #print(f"check {current_coordinates}, {end_coordinates}") 
                    
                    if len(lines) == len(set(lines)):
                        for coordinate in lines:
                            self.chip.grid[coordinate[0]][coordinate[1]][coordinate[2]] += 1
                        net = Net(lines)
                        start_gate.connections.append(end_gate.id)
                        end_gate.connections.append(start_gate.id)
                        self.chip.nets.append(net)
                        flag = False
                        #print(f"double check {current_coordinates}, {end_coordinates}") 
                        
                        

                    else:

                        lines.clear
                        return self.random_path(start_gate, end_gate)
            
            if flag == False:
                break
            # if there are neighbours available pick one randomly
            if choose: 
            
                new_line = random.choice(choose)

                # keep track of the lines which have been laid 
                lines.append(new_line)

                # change current position 
                current_coordinates = new_line

                #self.chip.grid[current_coordinates[0]][current_coordinates[1]][current_coordinates[2]] += 1

            # if there are no neighbours available run function again
            if not choose:
                
                # delete the lines which have been laid
                
                
                # to do: set limit
                return self.random_path(start_gate, end_gate)
        
        
        return print(f"double check {current_coordinates}, {end_coordinates}") 
    #==
                


    #def retry(self, start_gate, end_gate):
