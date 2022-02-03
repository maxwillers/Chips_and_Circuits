"""
randomise.py
This file contains the Random class which implements a random algorithm for finding paths between chips.
"""

import sys
import random
import copy
from code.algorithms.helpers_sorting import create_netlist
from code.algorithms.helpers_net import create_net_on_chip

sys.setrecursionlimit(5000)


def run_random(chip, sorting):
    """Go over all connections that need to be made and ensure they are made"""

    random_chip = copy.deepcopy(chip)

    # Create the properly sorted netlist
    random_chip = create_netlist(random_chip, sorting)

    # Go over every connection to be made an make a connection
    for connection in random_chip.connected_gates:
        start_gate = connection['start_gate']
        end_gate = connection['end_gate']

        path = random_path(random_chip, start_gate, end_gate)
        if path is False:
            break

        random_chip = create_net_on_chip(path, random_chip, start_gate, end_gate)

    # If all paths are made return chip
    return random_chip


def random_path(random_chip, start_gate, end_gate):
    """Assign each net with a randomized path"""
    path = []
    set_path = set(path)
    counter = 0

    # Set start coordinates
    sx = start_gate.x
    sy = start_gate.y
    sz = 0

    current_coordinates = (sx, sy, sz)

    # Set end coordinates
    ex = end_gate.x
    ey = end_gate.y
    ez = 0

    end_coordinates = (ex, ey, ez)

    path.append(current_coordinates)

    # While the connection has not been made, make random choices for a new line
    while current_coordinates != end_coordinates:

        # If there are neighbour points available, make a random choice between these neighbouring points
        choose, gates, intersections = random_chip.available_neighbors(
            current_coordinates
        )
        choose.extend(intersections)

        # Iterate over possible neighbour gates
        for end in gates:

            # If the current coordinates match the end gate coordinate, check if the coordinates are unique
            if end == end_coordinates:
                path.append(end)
                return path

        # If there are neighbours available pick one randomly
        if choose:
            new_line = random.choice(choose)

            # If a coordinate is already in the path it cannot be added again
            if new_line not in set_path:
                path.append(new_line)
                set_path.add(new_line)
                current_coordinates = new_line

            # If algorithm gets stuck return it
            elif counter == 1000:
                try:
                    return random_path(random_chip, start_gate, end_gate)

                # If a recursion error is occurring return that path could not be made
                except RecursionError:
                    return False
            else:
                counter += 1

        else:

            # If possible try again to find a connection
            try:
                return random_path(random_chip, start_gate, end_gate)

            # If a recursion error is occurring return that path could not be made
            except RecursionError:
                return False
