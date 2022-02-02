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
        if new_score <= old_score:
            self.astar_chip = new_chip
            self.score = new_score
