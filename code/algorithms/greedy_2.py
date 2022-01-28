"""
greedy_2.py
This file contains the class greedy class which implements a greedy alogrithm for finding paths
This greedy algorithm based on Manhattan distance.
"""
import copy
from statistics import median
from code.classes.net import Net
import random
import math
from code.algorithms.sorting import manhatan_dis_sort, random_sort

class Greedy_random:
    """
    The Greedy class that assigns the best possible value to each node one by one.
    """

    def __init__(self, chip):
        self.chip = copy.deepcopy(chip)
        self.connections = []
        self.connection_made = []
        self.run()

    def get_next_connection(self):
        """Gets the next coordinates for the next connection """
        return self.connections.pop(0)

    def add_connection(self, start_gate, end_gate):
        """Make the connection between two gates first changing the x coordinates then the y coordinates"""
        print(start_gate.id, end_gate.id)
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
        intersection = False
        i = 0

        # While the endgate is not reached go find a next step
        while (end_x, end_y , 0) not in self.chip.available_neighbors((x,y,z))[1]:
            i+=1
            neighbors = self.chip.available_neighbors((x,y,z))[0]
            best_neighbors = []
            medium_neighbors = []
            available_neigbors = [] 
            if i > 50000:
                return False
          
            for neighbor in neighbors:

                # Check if any of the neighbors are no longer an option(lead to dead end) and remove those
                if neighbor not in no_option:
                    available_neigbors.append(neighbor)
                    x_neighbor, y_neighbor, z_neigbor = neighbor

                    # Check if the available neighbors are in the right direction or not
                    if abs(end_x - x_neighbor) < abs(end_x - x) or abs(end_y - y_neighbor) < abs(end_y - y) or z_neigbor < z:
                        best_neighbors.append(neighbor)
                    
                    elif z_neigbor > z:
                        medium_neighbors.append
                    

            # If there are neighbors in the right direction go there    
            if len(best_neighbors) != 0:
                x,y,z = random.choice(best_neighbors)
                path.append((x,y,z))
                intersection = False
            
            elif len(medium_neighbors) != 0:
                x,y,z = random.choice(best_neighbors)
                path.append((x,y,z))
                intersection = False

            # Otherwise go to any of the available neighbors
            elif len(available_neigbors) != 0:
                x,y,z = random.choice(available_neigbors)
                path.append((x,y,z))
                intersection = False
                
            # If there are no available neighbors go back a step and make the current position no longer an option
            else:
                print("intersections")
                print(self.chip.available_neighbors((x,y,z))[2])
                if len(self.chip.available_neighbors((x,y,z))[2]) != 0:         
                    x,y,z = random.choice(self.chip.available_neighbors((x,y,z))[2])
                    path.append((x,y,z))
                    intersection = True
                
                elif intersection == True:
                    intersection_possibilities = []
                    for intersection_possibility in random.choice(self.chip.available_neighbors((x,y,z))[2]):
                        if intersection_possibility not in self.chip.grid[x][y][z]:
                            intersection_possibilities.append(intersection_possibility)
                    if len(intersection_possibility) > 0:
                        x,y,z = random.choice(intersection_possibilities)
                        path.append((x,y,z))
                    else:
                        print("stapje terug")
                        if len(path) > 1:
                            self.chip.grid[x][y][z].remove((path[-1], 0))
                            no_option.append(path.pop())
                            x,y,z = path[-1]
                        else:
                            print("fail")
                            return False
        
                else:
                    print("stapje terug")
                    if len(path) > 1:
                        self.chip.grid[x][y][z] = 0
                        no_option.append(path.pop())
                        x,y,z = path[-1]
                    else:
                        return False
                
        # If end gate is found make net and adjust connecitons in start and end gate
        x,y,z = end_x, end_y, 0
        path.append((x,y,z))

        # Fill path in grid with tuples where path comes from and goes to
        for i in range (len(path)):
            x, y, z = path[i]
            if self.chip.grid[x][y][z] != -1:
                self.chip.grid[x][y][z] = ((path[i - 1]), (path[i + 1]))

        # If end gate is found make net and adjust connecitons in start and end gate
        net = Net(path)
        self.chip.nets.append(net)
        start_gate.connections.append(end_gate.id)
        end_gate.connections.append(start_gate.id)
        

            
    def run(self):
        """Runs the greedy model"""

        self.backup_chip = copy.deepcopy(self.chip)
        
        # Sort the netlist from closest connection to farthest away
        self.connections = random_sort(self.chip.netlist)
        connections_new =[]
        for i in range(len(self.connections)):
            start, end = self.chip.gates[self.connections[0][i]-1], self.chip.gates[self.connections[1][i]-1]
            connections_new.append({'start_gate': start, 'end_gate': end, 'start_co': [start.x, start.y], 'end_co':[end.x, end.y]})
        self.connections = connections_new

        # Go past every connection
        while len(self.connections) > 0:
            connection = self.get_next_connection()

            self.add_connection(connection['start_gate'], connection['end_gate'])
            
            
            
        print("succes")
                
                
                
        
    
        
        


        

        
