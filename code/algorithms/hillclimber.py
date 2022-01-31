import copy
from .randomise import Random
import random

class Hillclimber():

    def __init__(self, chip):
        self.chip = copy.deepcopy(chip)
        for iteration in range(2000):
            self.reconfigure_chip()
            #self.check_solution()
    
    def reconfigure_chip(self):
        all_connections = self.chip.connections
        while len(self.chip.connections) > 1:
            random_connection = random.choice(all_connections)
            Random.random_path(random_connection[0], random_connection[1])
            all_connections.remove(random_connection)
        Random.random_path(all_connections[0][0], all_connections[0][1])
    
    #def check_solution()
