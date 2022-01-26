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
            self.add_connection(self.chip.gates[self.chip.netlist[0][i]-1], self.chip.gates[self.chip.netlist[1][i] -1], self.new_chip) 

    def add_connection(self, start_gate, end_gate, new_chip):
        """Make the connection between two gates first changing the x coordinates then the y coordinates"""
        # Set start coordinates
        start_x = start_gate.x
        end_x = end_gate.x

        # Set end coordinates
        start_y = start_gate.y
        end_y = end_gate.y

        # Set present coordinates and put them in path
        x = start_x
        y = start_y
        z = 0
        path = [(x,y,z)]

        # Make a list with coordinates that are not an option anymore, as they lead to a dead end
        no_option = []

        # While the endgate is not reached go find a next step
        while (end_x, end_y , 0) not in self.chip.available_neighbours((x,y,z))[1]:
            neighbors = self.chip.available_neighbours((x,y,z))[0]
            best_neighbors = []
            available_neigbors = []
          
            for neighbor in neighbors:

                # Check if any of the neighbors are no longer an option(lead to dead end) and remove those
                if neighbor not in no_option:
                    available_neigbors.append(neighbor)
                    x_neighbor, y_neighbor, z_neigbor = neighbor

                    # Check if the available neighbors are in the right direction or not
                    if abs(end_x - x_neighbor) < abs(end_x - x) or abs(end_y - y_neighbor) < abs(end_y - y) or z_neigbor < z:
                        best_neighbors.append(neighbor)


            # If there are neighbors in the right direction go there    
            if len(best_neighbors) != 0:
                x,y,z = random.choice(best_neighbors)
                path.append((x,y,z))
                self.chip.grid[x][y][z] += 1

            # Otherwise go to any of the available neighbors
            elif len(available_neigbors) != 0:
                x,y,z = random.choice(available_neigbors)
                path.append((x,y,z))
                self.chip.grid[x][y][z] += 1

            # If there are no available neighbors go back a step and make the current position no longer an option
            else:
                if len(path) > 1:
                    self.chip.grid[x][y][z] -= 1
                    no_option.append(path.pop())
                    x,y,z = path[-1]
                else:
                    return self.create_netlist(self.chip)


        # If end gate is found make net and adjust connecitons in start and end gate
        x,y,z = end_x, end_y, 0
        path.append((x,y,z))
        net = Net(path)
        self.chip.nets.append(net)
        start_gate.connections.append(end_gate.id)
        end_gate.connections.append(start_gate.id)
        