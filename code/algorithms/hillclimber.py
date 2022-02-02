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

class Hillclimber():

    def __init__(self, chip): 
        self.chip = copy.deepcopy(chip)
        self.score = chip.chip.calculate_value()
        

        for iteration in range(100):
            print(f'Iteration {iteration}/2000, current value: {self.score}')
            new_chip = copy.deepcopy(self.chip)
            new_chip = self.reconfigure_chip(new_chip)
            self.check_solution(new_chip)
            #self.chip = new_chip


    def reconfigure_chip(self, new_chip):
        #print(len(new_chip.connections))
        flag = True
        connection_list = []
        #while len(connection_list) < len(new_chip.chip.connections):
        random_connection = random.choice(new_chip.chip.connections)
        if random_connection not in connection_list:
            connection_list.append(random_connection)
            self.undo_connection(new_chip, random_connection['start_co'], random_connection['end_co']) 
            if isinstance(new_chip, Astar) == True:
                came_from, start, end = new_chip.search(random_connection['start_gate'], random_connection['end_gate'], flag)
                path = new_chip.create_path(came_from, start, end)
                self.create_new_connection(new_chip, path)
                return new_chip
         
        # self.undo_connection(new_chip, new_chip.chip.connections[0]['start_co'], new_chip.chip.connections[0]['end_co'])
        # if isinstance(new_chip, Astar) == True:
        #     came_from, start, end = new_chip.search(new_chip.chip.connections[0]['start_gate'], new_chip.chip.connections[0]['end_gate'], flag)
        #     path = new_chip.create_path(came_from, start, end)
        #     self.create_new_connection(new_chip, path)
        # else: 
        #     print("madremia")


    def check_solution(self, new_chip):
        new_score = new_chip.chip.calculate_value()        
        old_score = self.score
        print(new_score)
        print(old_score)
        if new_score <= old_score:
            self.chip = new_chip
            self.score = new_score

    def undo_connection(self, new_chip, start_co, end_co):
        """Removes the path made from the grid an removes net from chip"""
        for net in new_chip.chip.nets:
            if net.path[0] == (start_co[0], start_co[1], 0) and net.path[-1] == (end_co[0], end_co[1], 0):
                for i in range(len(net.path)):
                    x,y,z = net.path[i]
                    
                    if new_chip.chip.grid[x][y][z] != -1:
                        new_chip.chip.grid[x][y][z].remove((net.path[i - 1]))
                        new_chip.chip.grid[x][y][z].remove((net.path[i + 1]))
                    
                        
                #print(len(new_chip.nets))        
                new_chip.chip.nets.remove(net)

                

    def create_new_connection(self, new_chip, path):
        for i in range(len(path)):
            x, y, z = path[i]
            print(new_chip.chip.grid[x][y][z])
            if new_chip.chip.grid[x][y][z] != -1:
                if new_chip.chip.grid[x][y][z] == 0:
                    new_chip.chip.grid[x][y][z] = [(path[i - 1]), (path[i + 1])]
                else:
                    new_chip.chip.grid[x][y][z] = new_chip.chip.grid[x][y][z] + [(path[i - 1]), (path[i + 1])]
        net = Net(path)
        new_chip.chip.nets.append(net)
