"""
greedy_2.py
This file contains the class greedy class which implements a greedy alogrithm for finding paths
This greedy algorithm based on Manhattan distance.
"""
import copy
from code.classes.net import Net
import random
<<<<<<< HEAD
from code.algorithms.helpers import random_sort
=======
import math
from code.algorithms.helpers_sorting import manhattan_dis_sort, random_sort
>>>>>>> 8b45c5a01cad21f4ec3437f7c69a73d84dd72155


class Greedy_random:
    """
    The Greedy class that assigns the best possible value to each node one by one.
    """

    def __init__(self, chip):
        self.chip = copy.deepcopy(chip)
        self.connections = []
        self.connection_made = []
        self.run()
        self.succesfull = False


    def get_next_connection(self):
        """Gets the next coordinates for the next connection"""
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
        path = [(x, y, z)]

        # Make a list with coordinates that are not an option anymore, as they lead to a dead end
        no_option = []

        # While the end gate is not reached go find a next step
        while (end_x, end_y, 0) not in self.chip.available_neighbors((x, y, z))[1]:
            if len(path) < 200 and len(no_option) < 400:
                neighbors = self.chip.available_neighbors((x, y, z))[0]
                best_neighbors = []
                medium_neighbors = []
                available_neigbors = []
                for neighbor in neighbors:

                    # Check if any of the neighbors are no longer an option (lead to dead end) and remove those
                    if neighbor not in no_option and neighbor not in path:
                        available_neigbors.append(neighbor)
                        x_neighbor, y_neighbor, z_neigbor = neighbor

                        # Check if the available neighbors are located in the right direction or not
                        if (
                            abs(end_x - x_neighbor) < abs(end_x - x)
                            or abs(end_y - y_neighbor) < abs(end_y - y)
                            or z_neigbor < z
                        ):
                            best_neighbors.append(neighbor)
                        elif z_neigbor > z:
                            medium_neighbors.append

                # If there are neighbors to the right, go there
                if len(best_neighbors) != 0:
                    x, y, z = random.choice(best_neighbors)
                    path.append((x, y, z))

                elif len(medium_neighbors) != 0:
                    x, y, z = random.choice(best_neighbors)
                    path.append((x, y, z))

                # Otherwise, go to any of the available neighbors
                elif len(available_neigbors) != 0:
                    x, y, z = random.choice(available_neigbors)
                    path.append((x, y, z))

                # If there are no available neighbors, go back a step and set the current position to no longer being an option
                else:
                    if len(self.chip.available_neighbors((x, y, z))[2]) > 0:
                        available_intersections = []
                        for intersection in self.chip.available_neighbors((x, y, z))[2]:
                            if intersection not in no_option:
                                available_intersections.append(intersection)
                        if len(available_intersections) > 0:
                            x, y, z = random.choice(available_intersections)
                            path.append((x, y, z))
                        else:
                            return False
                    else:
                        if len(path) > 1:
                            no_option.append(path.pop())
                            x, y, z = path[-1]
                        else:
                            return False
            else:
                return False

        # If the end gate is found, create a net and adjust the connections in start and end gate
        x, y, z = end_x, end_y, 0
        path.append((x, y, z))

        # Fill path in grid with tuples where path comes from and goes to
        for i in range(len(path)):
            x, y, z = path[i]
            if self.chip.grid[x][y][z] != -1:
                if self.chip.grid[x][y][z] == 0:
                    self.chip.grid[x][y][z] = [(path[i - 1]), (path[i + 1])]
                else:
                    self.chip.grid[x][y][z].append((path[i - 1]))
                    self.chip.grid[x][y][z].append((path[i + 1]))

        # If the end gate is found, create a net and adjust the connections in start and end gate
        net = Net(path)
        self.chip.nets.append(net)
        start_gate.connections.append(end_gate.id)
        end_gate.connections.append(start_gate.id)
        return True


    def run(self):
        """Runs the greedy model"""
        for i in range(len(self.chip.netlist[0])):
            self.chip.connections.append(
                (
                    self.chip.gates[self.chip.netlist[0][i] - 1],
                    self.chip.gates[self.chip.netlist[1][i] - 1],
                )
            )

        # Sort the netlist from closest connection to the connection the farthest away
        self.chip.connections = random_sort(self.chip.connections)

        self.connections = copy.deepcopy(self.chip.connections)
        steps = 0

        # Go past every connection
        while len(self.connections) > 0:

            # uitleg 1000 stappen????
            if steps < 1000:
                steps += 1
                print(steps)
                connection = self.get_next_connection()

                # If connection succesfully made add to the connection list
                if not self.add_connection(
                    connection["start_gate"], connection["end_gate"]
                ):
                    print("fail")
                    return False
            else:
                return False

        # Checks if a succesful connection has been found, laten staan????/   waar staat dit, moet "succesful" zijn
        self.succesfull = True
        print("succes")

        print("succes")
