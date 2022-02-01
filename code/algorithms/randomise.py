"""
randomise.py

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

def run_random(chip):
    """Go over all connection that need to be made and ensure they are made"""

    chip = copy.deepcopy(chip)

    # Iterate over the netlist
    for i in range(len(chip.netlist[0])):
        chip.connections.append((chip.gates[chip.netlist[0][i]-1], chip.gates[chip.netlist[1][i] -1])) 
    
    # Rearange list so the shortest distances will be first
    chip.connections = manhatan_dis_sort(chip.connections)

    # Go over every connection to be made an make a connection       
    for connection in chip.connections:
        start_gate = connection['start_gate']
        end_gate = connection['end_gate']

        path = random_path(chip, start_gate, end_gate)

        # Change values in grid to the coordinates every grid point connects to
        for i in range(len(path)):
            x, y, z = path[i]
            if chip.grid[x][y][z] != -1: 
                if chip.grid[x][y][z] == 0:
                    chip.grid[x][y][z] = [(path[i - 1]), (path[i + 1])]
                else:
                    chip.grid[x][y][z] = chip.grid[x][y][z] + [(path[i - 1]), (path[i + 1])]
        
        # Add path to net and add connections to gates
        net = Net(path) 
        start_gate.connections.append(end_gate.id)
        end_gate.connections.append(start_gate.id)
        chip.nets.append(net)

    return chip

def random_path(chip, start_gate, end_gate):
    """
    Assign each net with a randomized path
    """
    path = [] 
    set_path = set(path)
    counter = 0
    sx = start_gate[0]
    sy = start_gate[1]
    sz = 0

    current_coordinates = (sx, sy, sz)

    ex = end_gate[0]
    ey = end_gate [1]
    ez = 0

    end_coordinates = (ex, ey, ez)

    path.append(current_coordinates)

    # While the connection has not been made, make random choices for a new line  
    while current_coordinates != end_coordinates:

        # If there are neighbour points available, make a random choice between these neighbouring points
        choose, gates, intersections = chip.available_neighbors(current_coordinates)
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
                print(counter)
                try:
                    return random_path(chip, start_gate, end_gate)

                # if a recursion error is occurring quit the program
                except RecursionError:
                    print('stuck')
                    quit()     
            else:
                counter += 1

        else:

            # if possible try again to find a connection
            try:
                return random_path(chip, start_gate, end_gate)

            # if a recursion error is occurring quit the program
            except RecursionError:
                print('stuck')
                quit()  


