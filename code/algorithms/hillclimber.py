import copy
from hashlib import new
from . import randomise
import random
from ..classes.chips import Chip

class Hillclimber():

    def __init__(self, astar_chip):
        self.astar_chip = copy.deepcopy(astar_chip)
        self.score = astar_chip.chip.calculate_value()
        for iteration in range(2000):
            print(f'Iteration {iteration}/{2000}, current value: {self.score}')
            new_astar_chip = copy.deepcopy(self.astar_chip)
            self.reconfigure_astar_chip()
            self.check_solution(new_astar_chip)
    
    def reconfigure_astar_chip(self):
        all_connections = self.astar_chip.connections
        while len(self.astar_chip.connections) > 1:
            random_connection = random.choice(all_connections)
            randomise.random_path(random_connection[0], random_connection[1])
            all_connections.remove(random_connection)
        randomise.random_path(all_connections[0][0], all_connections[0][1])
    
    
    def check_solution(self, new_astar_chip):
        new_score = new_astar_chip.chip.calculate_value()
        old_score = self.score
        if new_score <= old_score:
            self.astar_chip = new_astar_chip
            self.score = new_score

