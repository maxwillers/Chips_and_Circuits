"""This file contains the class with all gates"""

class Gate: 
    """Class for creating gates"""

    def __init__(self, gate_id, x, y):
        self.id = gate_id
        self.x = x
        self.y = y
        self.connections = []
