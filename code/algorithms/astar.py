
# data structure that handles elements in order from a high to a low assigned priority
import copy
from enum import Flag
from hashlib import new
from os import path
from code.algorithms.sorting import random, manhatan_dis_sort
import numpy 
import heapq
from matplotlib.pyplot import flag
from code.classes.net import Net
#from queue import PriorityQueue
import random

class PriorityQueue:
    """
    class which creates a priority queu
    source: https://www.redblobgames.com/pathfinding/a-star/implementation.html"""

    def __init__(self):
        self.coordinates = []
    
    def empty(self):
        return not self.coordinates

    def put(self, coordinate, priority):
        heapq.heappush(self.coordinates, (priority, coordinate))

    def get(self):
        return heapq.heappop(self.coordinates)[1]

class Astar():
    """Base class that stores all the required components for a funcioning A* algorithm"""
 
    def __init__(self, chip):
        self.chip = copy.deepcopy(chip)
        self.create_netlist()
        

 
 
    def create_netlist(self):
        """Go over all the connections that need to be made and ensure that they are made"""
        connections =[]
        for i in range (len(self.chip.netlist[0])):
            connections.append((self.chip.gates[self.chip.netlist[0][i]-1], self.chip.gates[self.chip.netlist[1][i] -1])) 
        
        # Sort the netlist from closest connection to farthest away
        connections = manhatan_dis_sort(connections)
            #print(self.search(start_gate, end_gate))
        for connection in connections:
            start_gate = connection['start_gate']
            end_gate = connection['end_gate']

            # Find a path between two gates
            came_from, start, end = self.search(start_gate, end_gate)
            path = self.create_path(came_from, start, end)
            for i in range(len(path)):
                x, y, z = path[i]
                if self.chip.grid[x][y][z] == 0:
                    self.chip.grid[x][y][z] = ((path[i - 1]), (path[i + 1]))
                elif self.chip.grid[x][y][z] != -1 and self.chip.grid[x][y][z] != 0:
                    self.chip.grid[x][y][z] = ((path[i - 1]), (path[i + 1]))
                    self.chip.intersections += len(self.chip.grid[x][y][z]) / 2
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
            choose.extend(intersections)

            for gate in gates:
                if gate == end_coordinates:
                    choose.append(gate)

            if location == end_coordinates:
                break
            
          
            for option in choose:
                #extra_costs = self.chip.cost(location, option)
                new_cost = costs_so_far[location] + self.chip.cost(option)
                
                if option not in costs_so_far or new_cost < costs_so_far[option]:
                    costs_so_far[option] = new_cost
                    #print(self.heuristic(option, end_coordinates))                    
                    priority = new_cost  + self.heuristic(option, end_coordinates) 
                
                    pq.put(option, priority)
                    came_from[option] = location
                                    
        if pq.empty():
            came_from[end_coordinates] = location        
            print("false")
      
        return came_from, (sx, sy, sz), end_coordinates
                   
    def heuristic(self, neighbor, end_gate):
            """Calculates the distance with the Manhattan metric and returns the distance between two gates"""
            """Constitutes the h in the formula f(n) = g(n) + h(n)"""
            a = numpy.array(neighbor)
            b = numpy.array(end_gate)
            return numpy.linalg.norm(a-b)

    def create_path(self, came_from, start, end):
        position = end
        path = []
        while position != start:
            path.append(position)
           
            position = came_from[position]
        path.append(start)
        path.reverse()
        return path
 
 
    # def intersections_search(self, start, end):
