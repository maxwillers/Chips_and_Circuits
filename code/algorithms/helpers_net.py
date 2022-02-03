"""
helpers_net.py

This file contains functions that can be used in the algorithms that help with paths
- create_net_on_chip: adds the path to the grid to make it a net
- undo_net: removes net from chip
"""
from code.classes.net import Net


def create_net_on_chip(path, chip, start_gate, end_gate):
    """Adds path to grid and the net to chip"""

    # Fill grid with coordinates of both the previous and following coordinate of the path
    for i in range(len(path)):
        x, y, z = path[i]
        if chip.grid[x][y][z] != -1:
            if chip.grid[x][y][z] == 0:
                chip.grid[x][y][z] = [(path[i - 1]), (path[i + 1])]
            else:
                chip.grid[x][y][z] += [(path[i - 1]), (path[i + 1])]

    # If end gate is found make net and adjust connected_gates in start and end gate
    net = Net(path)
    chip.nets.append(net)
    start_gate.connections.append(end_gate.id)
    end_gate.connections.append(start_gate.id)

    return chip


def undo_net(chip, start_co, end_co):
    """Removes the path made from the grid an removes net from chip"""

    # Go over every path in the chip to see which has the same start and end gate
    for net in chip.nets:
        if net.path[0] == (start_co[0], start_co[1], 0) and net.path[-1] == (
            end_co[0],
            end_co[1],
            0,
        ):

            # Go over every coordinate in the path (except start and end coordinate)
            for i in range(1, len(net.path) - 1, 1):
                x, y, z = net.path[i]
                new_tuples = []
                old_tuples = [(net.path[i - 1]), (net.path[i + 1])]
                current_tuples = chip.grid[x][y][z]

                # Filter out the coordinates that need to be removed
                if current_tuples == 0 or len(current_tuples) < 3:
                    chip.grid[x][y][z] = 0
                else:
                    for coordinate in current_tuples:
                        if coordinate not in old_tuples:
                            new_tuples.append(coordinate)

                    # Give the grid the correct coordinates(with the path removed)
                    chip.grid[x][y][z] = new_tuples

            # Remove net from chip
            chip.nets.remove(net)
            return chip
