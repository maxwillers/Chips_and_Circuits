"""
sorting.py
This file contains functions that can sort the netlist:
- manhatan_dis_sort : sorts the list based on their manhatan distance
- union_sort: 
- random_sort: randomly sorts the netlist 
"""

import random
import math


def dist(p0,p1):
        """Calculates the distance between two points"""
        return math.sqrt((p1[0]-p0[0])**2+(p1[1]-p0[1])**2)
    
def manhatan_dis_sort(connections):
    """Sorts the netlist based on the distance between the gates"""
    connections_new =[]
    for connection in connections:
        start, end = connection
        connections_new.append({'start_gate': start, 'end_gate': end, 'start_co': [start.x, start.y], 'end_co':[end.x, end.y]})
    connections = sorted(connections_new, key=lambda p:dist(p['start_co'],p['end_co']))

    return connections


def random(connections):
    """Create a random connections list by swapping connections"""
    for _ in range(len(connections)*2):
        # Make two indexes
        index_1 = 0
        index_2 = 0

        # Give them a random value and make sure these values are not the same
        while index_1 == index_2:
            index_1 = random.randrange(0, len(connections))
            index_2 = random.randrange(0, len(connections))

        # Swap nets in the connections list
        tmp = connections[index_1]
        connections[index_1] = connections[index_2]
        connections[index_2] = tmp

    return connections
