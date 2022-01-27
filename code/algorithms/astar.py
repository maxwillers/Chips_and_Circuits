
# data structure that handles elements in order from a high to a low assigned priority
import copy
from enum import Flag
from hashlib import new
from os import path
from code.classes.net import Net
from queue import PriorityQueue

class Astar():
    """Base class that stores all the required components for a funcioning A* algorithm"""

    def __init__(self, chip):
        self.chip = copy.deepcopy(chip)
        self.create_netlist()


    def create_netlist(self):
        """Go over all the connections that need to be made and ensure that they are made"""
        for i in range(len(self.chip.netlist[0])):
            start_gate = self.chip.gates[self.chip.netlist[0][i]-1]
            end_gate = self.chip.gates[self.chip.netlist[1][i]-1]
            #print(self.search(start_gate, end_gate))
            came_from, start, end = self.search(start_gate, end_gate)
            path = self.create_path(came_from, start, end)
            for i in range(len(path)):
                x, y, z = path[i]
                if self.chip.grid[x][y][z] != -1:
                    self.chip.grid[x][y][z] = ((path[i - 1]), (path[i + 1]))

            net = Net(path)
            start_gate.connections.append(end_gate.id)
            end_gate.connections.append(start_gate.id)
            self.chip.nets.append(net)
    
    def search(self, start_gate, end_gate):
        
        flag = False

        # Set start coordinates
        sx = start_gate.x
        sy = start_gate.y
        sz = 0

        # Set end coordinates
        ex = end_gate.x
        ey = end_gate.y 
        ez = 0

        end_coordinates = (ex, ey, ez)

        # Set present coordinates and put them in path
        current_coordinates = (sx, sy, sz)
        
        pq = PriorityQueue()
        pq.put(current_coordinates, 0)
        costs_so_far = {}
        came_from = {}
        costs_so_far[(sx, sy, sz)] = 0
        came_from[(sx, sy, sz)] = None

        print(f"start: {current_coordinates}, end: {end_coordinates}")

        while not pq.empty():
            
            location = pq.get()

            choose, gates, intersections = self.chip.available_neighbors(location)
            
            if end_coordinates in gates:
                came_from[end_coordinates] = location
                break


            for option in choose:
                #extra_costs = self.chip.cost(location, option)
                new_cost = costs_so_far[location] + 1

              
                if option not in costs_so_far or new_cost < costs_so_far[option]:
                    costs_so_far[option] = new_cost
                    priority = new_cost + self.heuristic(option, end_coordinates)
                        
                    pq.put(option, priority)
                    came_from[option] = location
                

        # if pq.empty():
        #     came_from[end_coordinates] = location
        self.chip.weights.clear()
        return came_from, (sx, sy, sz), end_coordinates
                    
    def heuristic(self, neighbor, end_gate):
            """Calculates the distance with the Manhattan metric and returns the distance between two gates"""
            """Constitutes the h in the formula f(n) = g(n) + h(n)"""
            sx, sy, sz = neighbor
            ex, ey, ez = end_gate
            return abs(sx - ex) + abs(sy - ey) + abs(sz - ez)

    def create_path(self, came_from, start, end):
        position = end
        path = []
        while position != start:
            path.append(position)
            
            position = came_from[position]
        path.append(start)
        path.reverse()
        return path

