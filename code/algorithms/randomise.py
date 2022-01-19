"""
This file contains the Random class which implements a random algorithm for finding paths between chips.
"""

from calendar import c
import random
import copy
from tracemalloc import start
from code.classes import chips
from code.classes.chips import Chip
from code.classes.net import Net


class Random:

    def __init__(self, chip):
        self.chip = copy.deepcopy(chip)
        self.create_netlist()
        

    def create_netlist(self):
        """Go over all connection that need to be made and ensure they are made"""

        # Iterate over the netlist
        for i in range(len(self.chip.netlist[0])):
            print(i)
            self.random_path(self.chip.gates[self.chip.netlist[0][i]-1], self.chip.gates[self.chip.netlist[1][i] -1])


    def random_path(self, start_gate, end_gate):
        """Assign each net with a randomized path"""

        lines = [] 
           
        sx = start_gate.x
        sy = start_gate.y
        sz = 0

        current_coordinates = (sx, sy, sz)

        ex = end_gate.x
        ey = end_gate.y 
        ez = 0

        end_coordinates = (ex, ey, ez)

        # While the connection has not been made, make random choices for a new line  
        while current_coordinates != end_coordinates:

            # If there are neighbour points available, make a random choice between these neighbouring points
            choose, gates = self.chip.available_neighbours(current_coordinates)
            
            # Iterate over the possible neighbouring gates
            for end in gates:

                # If the current coordinates match the end gate coordinate, create the net
                if end == end_coordinates:
                    print(f"check {current_coordinates}, {end_coordinates}") 
                    net = Net(lines)
                    start_gate.connections.append(end_gate.id)
                    end_gate.connections.append(start_gate.id)
                    self.chip.nets.append(net)
                    return
                    
            # If there are neighbours available, pick one randomly
            if choose: 
                new_line = random.choice(choose)

                # Keep track of the lines which have been laid
                lines.append(new_line)

                # Keep track of the current position
                current_coordinates = new_line

                self.chip.grid[current_coordinates[0]][current_coordinates[1]][current_coordinates[2]] += 1

            # If there are no neighbours available, run the function again
            if not choose:
                
                # Delete the lines which have been laid in order to start over
                for coordinate in lines:
                    self.chip.grid[coordinate[0]][coordinate[1]][coordinate[2]] = 0

                # to do: set limit
                self.random_path(start_gate, end_gate)


