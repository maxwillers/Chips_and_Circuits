"""
greedy_itt.py
This file contains the class greedy class which implements a greedy alogrithm for finding paths
This greedy algorithm is based on Manhattan distance.
"""
import copy
from code.classes.net import Net
import random
from code.algorithms.helpers import manhattan_dis_sort


class Greedy_itt:
    """The Greedy class that assigns the best possible value to each node one by one"""
    def __init__(self, chip):
        self.chip = copy.deepcopy(chip)
        self.connections = []
        self.connection_made = []
        self.run()


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
        # flake error redefinition of unused path!!!!!!!!!!!!!!!!!!!!!!!
        path = [(x, y, z)]

        # Make a list with coordinates that are not an option anymore, as they lead to a dead end
        no_option = []

        # While the endgate is not reached go find a next step
        while (end_x, end_y, 0) not in self.chip.available_neighbors((x, y, z))[1]:

            # hier comment????/ 200 en 400
            if len(path) < 200 and len(no_option) < 400:
                neighbors = self.chip.available_neighbors((x, y, z))[0]
                best_neighbors = []
                medium_neighbors = []
                available_neigbors = []
                for neighbor in neighbors:

                    # Check if any of the neighbors are no longer an option(lead to dead end) and remove those
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

                # If there are no available neighbors go back a step and make the current position no longer an option
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

        # If the end gate is found make the net and adjust connections in start and end gate ??????
        x, y, z = end_x, end_y, 0
        path.append((x, y, z))

        # Fill path in grid with tuples where path comes from and goes to ????
        for i in range(len(path)):
            x, y, z = path[i]
            if self.chip.grid[x][y][z] != -1:
                if self.chip.grid[x][y][z] == 0:
                    self.chip.grid[x][y][z] = [(path[i - 1]), (path[i + 1])]
                else:
                    self.chip.grid[x][y][z].append((path[i - 1]))
                    self.chip.grid[x][y][z].append((path[i + 1]))

        # If end gate is found make net and adjust connecitons in start and end gate
        net = Net(path)
        self.chip.nets.append(net)
        start_gate.connections.append(end_gate.id)
        end_gate.connections.append(start_gate.id)
        return True


    def undo_connection(self, start_co, end_co):
        """Removes the path made from the grid an removes net from chip"""
        for net in self.chip.nets:
            if net.path[0] == (start_co[0], start_co[1], 0) and net.path[-1] == (
                end_co[0],
                end_co[1],
                0,
            ):
                for i in range(1, len(net.path) - 1, 1):
                    x, y, z = net.path[i]
                    new_tuples = []
                    old_tuples = [(net.path[i - 1]), (net.path[i + 1])]
                    current_tuples = self.chip.grid[x][y][z]
                    if len(current_tuples) == 2:
                        self.chip.grid[x][y][z] = 0
                    else:
                        for coordinate in current_tuples:
                            if coordinate not in old_tuples:
                                new_tuples.append(coordinate)

                    self.chip.grid[x][y][z] = new_tuples

                self.chip.nets.remove(net)


    def run(self):
        """Runs the greedy model"""
        for i in range(len(self.chip.netlist[0])):
            self.chip.connections.append(
                (
                    self.chip.gates[self.chip.netlist[0][i] - 1],
                    self.chip.gates[self.chip.netlist[1][i] - 1],
                )
            )

        # Sort the netlist from closest connection to farthest away
        self.chip.connections = manhattan_dis_sort(self.chip.connections)

        self.connections = copy.deepcopy(self.chip.connections)
        steps = 0

        # Go past every connection
        while len(self.connections) > 0:
            if steps < 1000:
                steps += 1
                connection = self.get_next_connection()

                # If connection succesfully made add to connection made list
                if self.add_connection(
                    connection["start_gate"], connection["end_gate"]
                ):
                    self.connection_made.append(connection)

                # Otherwise add this connection to connection list again
                else:
                    while not self.add_connection(
                        connection["start_gate"], connection["end_gate"]
                    ):
                        steps += 1
                        if steps < 1000:

                            # If other connections were made choose to redo that one with a randomly chosen one
                            if len(self.connection_made) > 1:
                                weg_connection = self.connection_made.pop(
                                    random.randint(0, (len(self.connection_made) - 1))
                                )
                                self.connections.append(weg_connection)
                                self.undo_connection(
                                    weg_connection["start_co"], weg_connection["end_co"]
                                )
                                self.add_connection(
                                    connection["start_gate"], connection["end_gate"]
                                )

                            # Otherwise choose another connection randomly to be done
                            elif len(self.connections) > 1:
                                connection = self.connections.pop(
                                    random.randint(0, len(self.connections) - 1)
                                )
                            else:
                                return False

                        # Fail if too many steps have past; the path has gotten too long
                        else:
                            print("fail")
                            return False
