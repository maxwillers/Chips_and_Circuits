import pandas as pd 
import matplotlib.pyplot as plt 


class Grid:
    """Class for creating grid"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid = [[None for _ in range(self.x)] for _ in range(self.y)]

class Gate:
    """Class for creating gates"""

    # include height later 
    def __init__(self, id, x, y):
        self.id = id 
        self.x = x 
        self.y = y 

class Net: 
    """Class for creating nets"""

    def __init__(self, start, end):
        self.start = start 
        self.end = end
        self.path = []




