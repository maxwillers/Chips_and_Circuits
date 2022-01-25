"""
greedy_2.py
This file contains the class greedy class which implements a greedy alogrithm for finding paths
This greedy algorithm based on Manhattan distance.
"""
import copy
from code.classes.net import Net
import random
import math

class Greedy_random:
    """
    The Greedy class that assigns the best possible value to each node one by one.
    """

    def __init__(self, chip):
        self.chip = copy.deepcopy(chip)
        self.connections = []
        self.connection_made = []
        self.run()
        
    
    def dist(self, p0,p1):
        """Calculates the distance between two points"""
        return math.sqrt((p1[0]-p0[0])**2+(p1[1]-p0[1])**2)
    
    def sort_netslist(self):
        """Sorts the netlist based on the distance between the gates"""
        connections_new =[]
        for connection in self.connections:
            start, end = connection
            connections_new.append({'start_gate': start, 'end_gate': end, 'start_co': [start.x, start.y], 'end_co':[end.x, end.y]})
        self.connections = sorted(connections_new, key=lambda p:self.dist(p['start_co'],p['end_co']))


    def get_next_connection(self):
        """Gets the next coordinates for the next connection """
        return self.connections.pop(0)

    def add_connection(self, start_gate, end_gate):
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
                    return False

        
        # If end gate is found make net and adjust connecitons in start and end gate
        x,y,z = end_x, end_y, 0
        path.append((x,y,z))
        net = Net(path)
        self.chip.nets.append(net)
        start_gate.connections.append(end_gate.id)
        end_gate.connections.append(start_gate.id)
        return True

    def undo_connection(self, start_co, end_co):
        """Removes the path made from the grid an removes net from chip"""
        for net in self.chip.nets:
            if net.path[0] == (start_co[0], start_co[1], 0) and net.path[-1] == (end_co[0], end_co[1], 0):
                for i in range(1, len(net.path), 1):
                    x,y,z = net.path[i]
                    self.chip.grid[x][y][z] -= 1
                
                self.chip.nets.remove(net)

            

    def run(self):
        """Runs the greedy model"""

        self.backup_chip = copy.deepcopy(self.chip)

        # Add netlist
        for i in range (len(self.chip.netlist[0])):
            self.connections.append((self.chip.gates[self.chip.netlist[0][i]-1], self.chip.gates[self.chip.netlist[1][i] -1])) 
        
        # Sort the netlist from closest connection to farthest away
        self.sort_netslist()
        steps = 0

        # Go past every connection
        while len(self.connections) > 0:
            if steps < 1000:
                steps +=1
                connection = self.get_next_connection()

                # If connection succesfully made add to connection made list
                if self.add_connection(connection['start_gate'], connection['end_gate']):
                    self.connection_made.append(connection)
                
                # Otherwise add this connection to connection list again
                else: 
                    while not self.add_connection(connection['start_gate'], connection['end_gate']):
                        steps +=1 
                        if steps < 1000: 
                            self.connections.append(connection)

                            # If other connections were made choose one randomly and redo that one
                            if len(self.connection_made) > 0:
                                connection = self.connection_made.pop(random.randint(0,(len(self.connection_made) -1)))
                                self.undo_connection(connection['start_co'],connection['end_co'])
                                self.add_connection(connection['start_gate'], connection['end_gate'])

                            # Otherwise choose another connection randomly to be done
                            else:
                                connection = self.connections.pop(random.randint(0, len(self.connections)-1))
                        
                        # Fail if to many steps have past
                        else:
                            print("fail")
                            return False
            else: 
                print("fail")
                # self.__init__(self.backup_chip)
                return False

        print("succes")
        return True
                
                
                
        
    
        
        


        

        
