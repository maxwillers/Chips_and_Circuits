import random
import copy
from tracemalloc import start
from code.classes import chips
from code.classes.chips import Chip


class Random:

    def __init__(self, chip):
        self.chip = copy.deepcopy(chip)
        self.create_netlist()
        

    def create_netlist(self):
        """Go over all connection that need to be made and ensure they are made"""
        # iterate over netlist
        for i in range(len(self.chip.netlist[0])):
            print(i)
            self.random_path(self.chip.gates[self.chip.netlist[0][i]-1], self.chip.gates[self.chip.netlist[1][i] -1])


    def random_path(self, start_gate, end_gate):
        """
        Assign each net with a randomized path
        """

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
            
            for end in gates:
                if end == end_coordinates:
                    print(f"check {current_coordinates}, {end_coordinates}") 
                    for coordinate in lines:
                        self.chip.grid[coordinate[0]][coordinate[1]][coordinate[2]] += 1
                    current_coordinates = end
                    return
                    
            # if there are neighbours available pick one randomly
            if choose: 
                new_line = random.choice(choose)

                # keep track of the lines which have been laid 
                lines.append(new_line)

                # change current position 
                current_coordinates = new_line
                
            # if there are no neighbours available run function again
            if not choose:
                # to do: set limit
                self.random_path(start_gate, end_gate)


