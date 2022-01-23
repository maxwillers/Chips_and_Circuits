"""
greedy_2.py
This file contains the class greedy class which implements a greedy alogrithm for finding paths
This greedy algorithm based on Manhattan distance.
"""
import copy
from code.classes.net import Net
import random

class Greedy_random:
    """
    The Greedy class that assigns the best possible value to each node one by one.
    """

    def __init__(self, chip):
        self.chip = copy.deepcopy(chip)
        self.create_netlist()
        
    def create_netlist(self):
        """Go over all connection that need to be made and ensure they are made"""
        for i in range (len(self.chip.netlist[0])):
            self.add_connection(self.chip.gates[self.chip.netlist[0][i]-1], self.chip.gates[self.chip.netlist[1][i] -1]) 

    def add_connection(self, start_gate, end_gate):
        """Make the connection between two gates first changing the x coordinates then the y coordinates"""
        path = []
        start_x = start_gate.x
        end_x = end_gate.x

        start_y = start_gate.y
        end_y = end_gate.y

        x = start_x
        y = start_y
        z = 0

        while x != end_x and y != end_y and z != 0:
            neighbors = self.chip.available_neighbors((x,y,z))
            best_neighbors = []
            medium_neighbors = []
            for neighbor in neighbors:
                x_neighbor, y_neighbor, z_neigbor = neighbor
                if abs(end_x - x_neighbor) < abs(end_x - x) or abs(end_y - y_neighbor) < abs(end_y - y):
                    best_neighbors.append(neighbor)
                elif z_neigbor < z:
                    medium_neighbors.append(neighbor)
            
            if len(best_neighbors) != 0:
                x,y,z = random.choice(best_neighbors)[0]
            elif len(medium_neighbors) != 0:
                x,y,z = medium_neighbors[0]
            else:
                x,y,z = random.choice(neighbor)[0]

            path.append((x,y,z))
            self.chip.grid[x][y][z] += 1
        
        # Create net
        net = Net(path)
        start_gate.connections.append(end_gate.id)
        end_gate.connections.append(start_gate.id)
        self.chip.nets.append(net)

