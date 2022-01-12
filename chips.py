"""
chips.py
This file contains the class Chip which forms a chip with gates on them
"""


class Chip:
    """Class for creating chip"""

    def __init__(self, netlist, gate_coordinates):
        # self.x = x
        # self.y = y
        #self.grid = [[None for _ in range(self.x)] for _ in range(self.y)]
        self.gates= [gate_coordinates['x'].tolist(), gate_coordinates['y'].tolist()]
       
