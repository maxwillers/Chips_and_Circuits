"""
Chips.py
This file contains the class Chip, which forms a chip with gates on it
"""

from code.classes.gate import Gate
import pandas as pd


class Chip:
    """Class for creating chip"""

    def __init__(self, width, length, netlist, gate_coordinates):
        self.width = width
        self.length = length
        self.height = 7
        self.gates = []
        self.nets = []
        self.gate_coordinates = gate_coordinates
        self.netlist = [netlist["chip_a"].tolist(), netlist["chip_b"].tolist()]
        self.connected_gates = []
        self.grid = [
            [[0 for _ in range(self.height + 1)] for _ in range(self.length + 1)]
            for _ in range(self.width + 1)
        ]
        self.add_gates()

    def add_gates(self):
        """create gates with id and connections"""
        id_gates = self.gate_coordinates["chip"].tolist()
        x_gates = self.gate_coordinates["x"].tolist()
        y_gates = self.gate_coordinates["y"].tolist()

        for i in range(len(id_gates)):
            gate = Gate(id_gates[i], x_gates[i], y_gates[i])

            # Set the gate value to -1
            x = gate.x
            y = gate.y
            z = 0
            self.grid[x][y][z] = -1
            self.gates.append(gate)

    def available_neighbors(self, coordinates):
        """Checks available neighbours for each position"""
        good_neighbors = []
        gate_neighbors = []
        intersect_neighbors = []

        x, y, z = coordinates

        # Check for each neighbour (point on the grid directly next to the current position) if they exist and are available
        for i in range(-1, 2, 2):

            # Check if the x-coordinates stay in the grid
            if x + i >= 0 and x + i <= self.width:

                # If the location on the grid is free, it is a option or a so-called "good neighbour"
                if self.grid[x + i][y][z] == 0:
                    good_neighbors.append((x + i, y, z))

                # If the location on the grid is a gate, it might be the endpoint
                elif self.grid[x + i][y][z] == -1:
                    if self.grid[x][y][z] == 0 or self.grid[x][y][z] == -1:
                        gate_neighbors.append((x + i, y, z))
                    elif (x + i, y, z) not in self.grid[x][y][z]:
                        gate_neighbors.append((x + i, y, z))

                # Else it might be an intersection option
                else:
                    wires = self.grid[x + i][y][z]
                    if coordinates not in wires:
                        intersect_neighbors.append((x + i, y, z))

            if y + i >= 0 and y + i <= self.length:
                if self.grid[x][y + i][z] == 0:
                    good_neighbors.append((x, y + i, z))
                elif self.grid[x][y + i][z] == -1:
                    gate_neighbors.append((x, y + i, z))
                else:
                    wires = self.grid[x][y + i][z]
                    if coordinates not in wires:
                        intersect_neighbors.append((x, y + i, z))

            # Check for neighbors with varying z-coordinates
            if z + i >= 0 and z + i <= self.height:
                if self.grid[x][y][z + i] == 0:
                    good_neighbors.append((x, y, z + i))
                elif self.grid[x][y][z + i] == -1:
                    gate_neighbors.append((x, y, z + i))
                else:
                    wires = self.grid[x][y][z + i]
                    if coordinates not in wires:
                        intersect_neighbors.append((x, y, z + i))

        # Return a list of tuples of all possible neighbours
        return good_neighbors, gate_neighbors, intersect_neighbors

    def is_solution(self):
        """Returns True if all gates in netlist are connected"""
        for connection in self.connected_gates:
            start_gate = connection["start_gate"]
            end_gate = connection["end_gate"]

            if end_gate.id not in start_gate.connections:
                return False
        return True

    def calculate_intersections(self):
        """Calculate how many intersections the chip has"""
        intersections = 0

        # For every grid point, check the number of coordinates
        for x in range(self.width + 1):
            for y in range(self.length + 1):
                for z in range(self.height + 1):

                    # If more than two coordinates are found at a point, it is an intersection
                    if self.grid[x][y][z] != 0 and self.grid[x][y][z] != -1:
                        if len(self.grid[x][y][z]) == 4:
                            intersections += 1
                        elif len(self.grid[x][y][z]) > 4:
                            intersections += len(self.grid[x][y][z]) - 4

        return intersections

    def calculate_value(self):
        """Returns the cost of placing the wires"""
        value = 0
        for net in self.nets:
            value += len(net.path) - 1
        value = value + (300 * self.calculate_intersections())

        return value

    def df_output(self):
        """Returns the output in a dataframe"""
        wires = []
        nets = []

        # Make a list of paths
        for net in self.nets:
            wires.append(str(net.path).replace(" ", ""))

        # Make a list of gate ID's that form a connection with each other
        for connection in self.connected_gates:
            start_gate = connection["start_gate"]
            end_gate = connection["end_gate"]
            nets.append(f"({start_gate.id},{end_gate.id})")

        return pd.DataFrame(data={"net": nets, "wires": wires})

    def cost(self, neighbor, flag):
        """Returns costs for the next step (used in astar algorithm)"""
        gates = self.available_neighbors(neighbor)[1]

        # If hillclimber is used on the A* algorithm, then don't take the gates into account
        if len(gates) > 0 and flag is False:
            return 1 + 10 * len(gates) + 300 * self.intersection(neighbor)

        # Otherwise do take them into account
        else:
            return 1 + 300 * self.intersection(neighbor)

    def intersection(self, neighbor):
        """Returns amount of intersections for a single grid point"""
        intersections = 0
        if (
            self.grid[neighbor[0]][neighbor[1]][neighbor[2]] != 0
            and self.grid[neighbor[0]][neighbor[1]][neighbor[2]] != -1
        ):
            intersections += 1
        return intersections
