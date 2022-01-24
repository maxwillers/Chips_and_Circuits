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
        self.create_netlist(chip)
        
    def create_netlist(self, chip):
        """Go over all connection that need to be made and ensure they are made"""
        self.new_chip = copy.deepcopy(chip)
        for i in range (len(self.chip.netlist[0])):
            self.add_connection(self.chip.gates[self.chip.netlist[0][i]-1], self.chip.gates[self.chip.netlist[1][i] -1]) 

    def add_connection(self, start_gate, end_gate):
        """Make the connection between two gates first changing the x coordinates then the y coordinates"""
        start_x = start_gate.x
        end_x = end_gate.x

        start_y = start_gate.y
        end_y = end_gate.y

        x = start_x
        y = start_y
        z = 0
        path = [(x,y,z)]
        no_option = []

        while (end_x, end_y , 0) not in self.chip.available_neighbours((x,y,z))[1]:
            neighbors = self.chip.available_neighbours((x,y,z))[0]
            best_neighbors = []
            available_neigbors = []
          
            for neighbor in neighbors:
                if neighbor not in no_option:
                    available_neigbors.append(neighbor)
                    x_neighbor, y_neighbor, z_neigbor = neighbor
                    if abs(end_x - x_neighbor) < abs(end_x - x) or abs(end_y - y_neighbor) < abs(end_y - y) or z_neigbor < z:
                        best_neighbors.append(neighbor)
                
            if len(best_neighbors) != 0:
                x,y,z = random.choice(best_neighbors)
                path.append((x,y,z))
                self.chip.grid[x][y][z] += 1
            elif len(available_neigbors) != 0:
                x,y,z = random.choice(available_neigbors)
                path.append((x,y,z))
                self.chip.grid[x][y][z] += 1
            else:
                if len(path) > 1:
                    self.chip.grid[x][y][z] -= 1
                    no_option.append(path.pop())
                    x,y,z = path[-1]


        x,y,z = end_x, end_y, 0
        path.append((x,y,z))
        net = Net(path)
        start_gate.connections.append(end_gate.id)
        end_gate.connections.append(start_gate.id)
        self.chip.nets.append(net)
