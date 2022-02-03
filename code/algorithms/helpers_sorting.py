"""
helpers_sorting.py
This file contains functions that can sort the netlist:
- manhattan_dis_sort : sorts the list based on their manhatan distance
- random_sort: randomly sorts the netlist

"""

import random
import math


def dist(p0, p1):
    """Calculates the distance between two points"""
    return math.sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)


def manhattan_dis_sort(connected_gates):
    """Sorts the netlist based on the distance between the gates"""
    connected_gates_new = []

    # Add connections to connections list
    for connection in connected_gates:
        start, end = connection
        connected_gates_new.append(
            {
                "start_gate": start,
                "end_gate": end,
                "start_co": [start.x, start.y],
                "end_co": [end.x, end.y],
            }
        )

    # Sort list based on their coordinates
    connected_gates = sorted(
        connected_gates_new, key=lambda p: dist(p["start_co"], p["end_co"])
    )

    return connected_gates


def random_sort(connected_gates):
    """Create a random conected_gates list by swapping gate connections that need to be made"""
    for _ in range(len(connected_gates) * 2):

        # Make two indices
        index_1 = 0
        index_2 = 0

        # Give them a random value and make sure these values are not the same
        while index_1 == index_2:
            index_1 = random.randrange(0, len(connected_gates))
            index_2 = random.randrange(0, len(connected_gates))

        # Swap nets in the connected_gates list
        tmp = connected_gates[index_1]
        connected_gates[index_1] = connected_gates[index_2]
        connected_gates[index_2] = tmp

        # Format the connected_gates list properly
        connected_gates_new = []
        for connection in connected_gates:
            start, end = connection
            connected_gates_new.append(
                {
                    "start_gate": start,
                    "end_gate": end,
                    "start_co": [start.x, start.y],
                    "end_co": [end.x, end.y],
                }
            )

    return connected_gates_new


def create_netlist(chip, sorting):
    """Create a list of the gate connections which are then sorted"""

    # Make a list of the gate connections to be made
    for i in range(len(chip.netlist[0])):
        chip.connected_gates.append(
            (chip.gates[chip.netlist[0][i] - 1], chip.gates[chip.netlist[1][i] - 1])
        )

    # Sort the netlist based on the wanted sort
    if sorting == "manhattan":
        chip.connected_gates = manhattan_dis_sort(chip.connected_gates)
    elif sorting == "random":
        chip.connected_gates = random_sort(chip.connected_gates)

    return chip
