"""
astar.py
This file contains the A* ("astar") class and creates solutions using the A* algorithm.
The heurstic used in this algorithm is based on Manhattan distance.
"""
import copy
from code.algorithms.helpers_sorting import create_netlist
from code.algorithms.helpers_net import create_net_on_chip
import heapq


class PriorityQueue:
    """
    Creates a priority queue
    Source: https://www.redblobgames.com/pathfinding/a-star/implementation.html
    """

    def __init__(self):
        self.coordinates = []

    def empty(self):
        return not self.coordinates

    def put(self, coordinate, priority):
        heapq.heappush(self.coordinates, (priority, coordinate))

    def get(self):
        return heapq.heappop(self.coordinates)[1]


class Astar:
    """Base class that stores all the required components for a funcioning A* algorithm"""

    def __init__(self, chip, sorting):
        self.chip = copy.deepcopy(chip)
        self.run(sorting)

    def run(self, sorting):
        """Goes over all the gate connections that need to be made and ensures that they are made"""

        # Create the properly sorted netlistt
        self.chip = create_netlist(self.chip, sorting)

        # Flag = False is used to take account with the gates, so they do not get closed in
        flag = False

        # Go over every connection and make that connection
        for connection in self.chip.connected_gates:
            start_gate = connection['start_gate']
            end_gate = connection['end_gate']

            # Find a path between two gates
            came_from, start, end = self.search(start_gate, end_gate, flag)
            path = self.create_path(came_from, start, end)

            # Append path to chip
            self.chip = create_net_on_chip(path, self.chip, start_gate, end_gate)

    def search(self, start_gate, end_gate, flag):
        """
        Finds the best paths for a net using the A* algorithm
        Source of inspiration: https://www.redblobgames.com/pathfinding/a-star/implementation.html
        """

        # Set start coordinates
        sx = start_gate.x
        sy = start_gate.y
        sz = 0

        # Set end coordinates
        ex = end_gate.x
        ey = end_gate.y
        ez = 0
        end_coordinates = (ex, ey, ez)

        # Set present coordinates and put them in a priority queue
        current_coordinates = (sx, sy, sz)
        pq = PriorityQueue()
        pq.put(current_coordinates, 0)

        # Keep track of the costs of the path thus far and the position the path just came from
        costs_so_far = {}
        came_from = {}
        costs_so_far[(sx, sy, sz)] = 0
        came_from[(sx, sy, sz)] = None

        # Continue the algorithm as long as the priority queue is not empty yet
        while not pq.empty():

            # Select the best location
            location = pq.get()
            choose, gates, intersections = self.chip.available_neighbors(location)
            choose.extend(intersections)

            # If the correct end gate is found in the gate list, add it to the possible options
            for gate in gates:
                if gate == end_coordinates:
                    choose.append(gate)

            # Connection was found
            if location == end_coordinates:
                break

            # Iterate over every possible option; each possible move to make
            for option in choose:

                # Update the costs
                new_cost = costs_so_far[location] + self.chip.cost(option, flag)

                # Check if an option has not appeared before or if the newly found path is a better (cheaper) one
                if option not in costs_so_far or new_cost < costs_so_far[option]:

                    # Update the queues
                    costs_so_far[option] = new_cost
                    priority = new_cost + self.manhattan_heuristic(
                        option, end_coordinates, flag
                    )

                    pq.put(option, priority)

                    # Update the path with the newly found better option
                    came_from[option] = location

        return came_from, (sx, sy, sz), end_coordinates

    def manhattan_heuristic(self, neighbor, end_gate, flag):
        """
        Calculates the distance with the Manhattan metric and returns the distance between two gates
        Constitutes the h in the formula f(n) = g(n) + h(n)
        """

        # Set coordinates neighbor and end_gate
        nx, ny, nz = neighbor
        ex, ey, ez = end_gate

        # If needed take in account the gates(do not come to close)
        if flag is False:
            return abs(nx - ex) + abs(ny - ey)
        else:
            return abs(nx - ex) + abs(ny - ey) + abs(nz - ez)

    def create_path(self, came_from, start, end):
        """Creates a path for a certain net"""

        position = end
        path = []

        # Backtrack the path to get the best A* approved option
        while position != start:
            path.append(position)
            try:
                position = came_from[position]
            except KeyError:
                return False

        path.append(start)

        # Reverse path so start coordinates are at the beginning
        path.reverse()

        return path
