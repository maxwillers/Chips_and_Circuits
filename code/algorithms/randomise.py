"""
randomise.py

This file contains the Random class which implements a random algorithm for finding paths between chips.
"""
import sys
from calendar import c
import random
import copy
from tracemalloc import start
from code.algorithms.helpers_sorting import manhattan_dis_sort, random_sort, create_netlist
from code.algorithms.helpers_path import path_to_chip
from code.classes.chips import Chip
from code.classes.net import Net

sys.setrecursionlimit(5000)


def run_random(chip, sorting):
    """Go over all connection that need to be made and ensure they are made"""

    flag = False
    random_chip = copy.deepcopy(chip)

    # Create the properly sorted netlistt
    random_chip = create_netlist(random_chip, sorting)
    print(random_chip.connections)

    # Go over every connection to be made an make a connection       
    for connection in random_chip.connections:
        start_gate, end_gate= connection
        # end_gate = connection['end_gate']

        path = random_path(random_chip, start_gate, end_gate)
        if path == False:
            flag = True
            break
        
        random_chip = path_to_chip(path, random_chip, start_gate, end_gate)

    if flag == False:
        return random_chip
    else:
        return False

def random_path(random_chip, start_gate, end_gate):
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
        choose, gates, intersections = random_chip.available_neighbors(current_coordinates)
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
                    return random_path(random_chip, start_gate, end_gate)

                # if a recursion error is occurring quit the program
                except RecursionError:
                    return False
            else:
                counter += 1

        else:

            # if possible try again to find a connection
            try:
                return random_path(random_chip, start_gate, end_gate)

            # if a recursion error is occurring quit the program
            except RecursionError:
                return False
