"""
greedy.py
This file contains the class greedy class which implements a greedy alogrithm for finding paths
This greedy algorithm can both be iterative, which means it will remove random paths if it cannot find a sollution or not
"""
import copy
from code.algorithms.helpers_path import path_to_chip, undo_connection
import random
from code.algorithms.helpers_sorting import create_netlist


class Greedy:
    """The Greedy class that assigns the best possible value to each node one by one"""

    def __init__(self, chip, sorting, it=False):
        self.chip = copy.deepcopy(chip)
        self.connections = []
        self.connection_made = []
        self.it = it
        self.run(sorting)

    def get_next_connection(self):
        """Gets the next coordinates for the next connection"""
        return self.connections.pop(0)

    def add_connection(self, start_gate, end_gate):
        """Make the connection between two gates first changing the x-coordinate then the y-coordinate"""

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

        # While the endgate is not reached go find a next step
        while (end_x, end_y, 0) not in self.chip.available_neighbors((x, y, z))[1]:
            if len(path) < 350 and len(no_option) < 500:
                neighbors = self.chip.available_neighbors((x, y, z))[0]
                best_neighbors = []
                medium_neighbors = []
                available_neigbors = []
                for neighbor in neighbors:

                    # Check if any of the neighbors are no longer an option (lead to dead end) and remove those
                    if neighbor not in no_option and neighbor not in path:
                        available_neigbors.append(neighbor)
                        x_neighbor, y_neighbor, z_neigbor = neighbor

                        # Check if the available neighbors are in the right direction or not
                        if (
                            abs(end_x - x_neighbor) < abs(end_x - x)
                            or abs(end_y - y_neighbor) < abs(end_y - y)
                            or z_neigbor < z
                        ):
                            best_neighbors.append(neighbor)
                        elif z_neigbor > z:
                            medium_neighbors.append

                # If there are neighbors in the right direction go there
                if len(best_neighbors) != 0:
                    x, y, z = random.choice(best_neighbors)
                    path.append((x, y, z))

                elif len(medium_neighbors) != 0:
                    x, y, z = random.choice(best_neighbors)
                    path.append((x, y, z))

                # Otherwise go to any of the available neighbors
                elif len(available_neigbors) != 0:
                    x, y, z = random.choice(available_neigbors)
                    path.append((x, y, z))

                # If there are no available neighbors check if an intersection can be made
                else:
                    if len(self.chip.available_neighbors((x, y, z))[2]) > 0:
                        available_intersections = []

                        # Check if intersection is in no option
                        for intersection in self.chip.available_neighbors((x, y, z))[2]:
                            if intersection not in no_option:
                                available_intersections.append(intersection)

                        # Make intersection if there are any available
                        if len(available_intersections) > 0:
                            x, y, z = random.choice(available_intersections)
                            path.append((x, y, z))
                        else:
                            return False

                    # If there are no available neighbors go back a step and make the current position no longer an option
                    else:
                        if len(path) > 1:
                            no_option.append(path.pop())
                            x, y, z = path[-1]
                        else:
                            return False
            else:
                return False

        # If end gate is found put that in the path list
        x, y, z = end_x, end_y, 0
        path.append((x, y, z))

        self.chip = path_to_chip(path, self.chip, start_gate, end_gate)
        return True

    def run(self, sorting):
        """Runs the greedy model"""

        # Create the properly sorted netlistt
        self.chip = create_netlist(self.chip, sorting)

        # Copy the connections list so it can be popped
        self.connections = copy.deepcopy(self.chip.connections)
        steps = 0

        # Go past every connection that needs to be made
        while len(self.connections) > 0:

            # Make sure the algorithm does not get stuck in iterations by using a maximum steps
            if steps < 5000:
                steps += 1

                # Get next connection
                connection = self.get_next_connection()
                start_gate, end_gate = connection

                # If connection succesfully made add to connection made list
                if self.add_connection(start_gate, end_gate):
                    self.connection_made.append(connection)

                # Otherwise add this connection to connection list again
                elif self.it is True:
                    while not self.add_connection(start_gate, end_gate):
                        steps += 1
                        if steps < 5000:

                            # If other connections were made choose one randomly and redo the connection
                            if len(self.connection_made) > 1:
                                remove_connection = self.connection_made.pop(
                                    random.randint(0, (len(self.connection_made) - 1))
                                )
                                self.connections.append(remove_connection)
                                remove_start, remove_end = remove_connection
                                self.chip = undo_connection(
                                    self.chip,
                                    [remove_start.x, remove_start.y],
                                    [remove_end.x, remove_end.y],
                                )
                                self.add_connection(start_gate, end_gate)

                            # Otherwise if no other connections are made choose another connection randomly to be done
                            elif len(self.connections) > 1:
                                connection = self.connections.pop(
                                    random.randint(0, len(self.connections) - 1)
                                )
                            else:
                                return False

                        # Stop algorithm if too many steps have been taken
                        else:
                            return False
                else:
                    return False

        # Update chip connections
        self.chip.connections = self.connection_made
