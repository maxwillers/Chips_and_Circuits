"""
hillclimber.py
This file contains the class Hillclimber that implements the hillclimber algorithm.
The hillclimber algorithm does not stand on its own; it is meant to be applied to any of the other algorithms as an optional addition.
"""

import ast
import copy
from hashlib import new
from tracemalloc import start
from matplotlib.pyplot import flag
from scipy import rand

from code.algorithms.astar import Astar
from . import randomise
import random
from ..classes.chips import Chip
from ..classes.net import Net
<<<<<<< HEAD


class Hillclimber:

    def __init__(self, astar_chip):
        self.astar_chip = copy.deepcopy(astar_chip)
        self.score = astar_chip.calculate_value()
        self.flag = False
        for iteration in range(2000):
            print(f"Iteration {iteration}/2000, current value: {self.score}")
            new_astar_chip = copy.deepcopy(self.astar_chip)
            self.reconfigure_astar_chip(new_astar_chip)
            self.check_solution(new_astar_chip)
            if self.flag == True:
                return False

        # self.astar_chip = new_astar_chip

    def reconfigure_astar_chip(self, new_astar_chip):
        # print(len(new_astar_chip.connections))
        connection_set = []
        while len(connection_set) < len(new_astar_chip.connections):
            random_connection = random.choice(new_astar_chip.connections)
            if random_connection not in connection_set:
                connection_set.append(random_connection)
                # print(connection_set)
                self.undo_connection(
                    new_astar_chip,
                    random_connection["start_co"],
                    random_connection["end_co"],
                )
                path = randomise.random_path(
                    new_astar_chip,
                    random_connection["start_gate"],
                    random_connection["end_gate"],
                )
                if path == False:
                    try:
                        path = randomise.random_path(
                            new_astar_chip,
                            random_connection["start_gate"],
                            random_connection["end_gate"],
                        )
                    except RecursionError:
                        self.flag = True
                        return
                self.create_new_connection(new_astar_chip, path)

            # new_astar_chip.connections.remove(random_connection)

        self.undo_connection(
            new_astar_chip,
            new_astar_chip.connections[0]["start_co"],
            new_astar_chip.connections[0]["end_co"],
        )
        path = randomise.random_path(
            new_astar_chip,
            new_astar_chip.connections[0]["start_gate"],
            new_astar_chip.connections[0]["end_gate"],
        )
        if path == False:
            try:
                path = randomise.random_path(
                    new_astar_chip,
                    random_connection["start_gate"],
                    random_connection["end_gate"],
                )
            except RecursionError:
                self.flag = True
                return
        self.create_new_connection(new_astar_chip, path)
        # new_astar_chip.connections.remove(new_astar_chip.connections[0])

    def check_solution(self, new_astar_chip):
        new_score = new_astar_chip.calculate_value()
        old_score = self.score
        if new_score < 1000:
            print(new_score)
        # print(new_astar_chip.calculate_intersections())
=======
from . import helpers_path
class Hillclimber():

    def __init__(self, chip): 
        self.astar_chip = copy.deepcopy(chip)
        self.score = chip.chip.calculate_value()
        
        for iteration in range(100):
            print(f'Iteration {iteration}/2000, current value: {self.score}')
            new_chip = copy.deepcopy(self.astar_chip)
            self.reconfigure_chip(new_chip)
            self.check_solution(new_chip)
            

    def reconfigure_chip(self, new_chip):
        #print(len(new_chip.connections))
        flag = True
        connection_list = []
        #while len(connection_list) < len(new_chip.chip.connections):
        random_connection = random.choice(new_chip.chip.connections)
        if random_connection not in connection_list:
            connection_list.append(random_connection)
            helpers_path.undo_connection(new_chip.chip, random_connection['start_co'], random_connection['end_co']) 
            if isinstance(new_chip, Astar) == True:
                came_from, start, end = new_chip.search(random_connection['start_gate'], random_connection['end_gate'], flag)
                path = new_chip.create_path(came_from, start, end)
                helpers_path.path_to_chip(path, new_chip.chip, random_connection['start_gate'], random_connection['end_gate'])
                #return new_chip

    def check_solution(self, new_chip):
        new_score = new_chip.chip.calculate_value()        
        old_score = self.score
        print(new_score)
        print(old_score)
>>>>>>> 8b45c5a01cad21f4ec3437f7c69a73d84dd72155
        if new_score <= old_score:
            self.astar_chip = new_chip
            self.score = new_score
<<<<<<< HEAD

    def undo_connection(self, new_astar_chip, start_co, end_co):
        """Removes the path made from the grid an removes net from chip"""
        for net in new_astar_chip.nets:
            if net.path[0] == (start_co[0], start_co[1], 0) and net.path[-1] == (
                end_co[0],
                end_co[1],
                0,
            ):
                for i in range(1, len(net.path), 1):
                    x, y, z = net.path[i]

                    if new_astar_chip.grid[x][y][z] != -1:
                        new_astar_chip.grid[x][y][z].remove((net.path[i - 1]))
                        new_astar_chip.grid[x][y][z].remove((net.path[i + 1]))

                # print(len(new_astar_chip.nets))
                new_astar_chip.nets.remove(net)

    def create_new_connection(self, new_astar_chip, path):
        for i in range(len(path)):
            x, y, z = path[i]
            if new_astar_chip.grid[x][y][z] != -1:
                if new_astar_chip.grid[x][y][z] == 0:
                    new_astar_chip.grid[x][y][z] = [(path[i - 1]), (path[i + 1])]
                else:
                    new_astar_chip.grid[x][y][z] = new_astar_chip.grid[x][y][z] + [
                        (path[i - 1]),
                        (path[i + 1]),
                    ]
        net = Net(path)
        new_astar_chip.nets.append(net)
=======
>>>>>>> 8b45c5a01cad21f4ec3437f7c69a73d84dd72155
