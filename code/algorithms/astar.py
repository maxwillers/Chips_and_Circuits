
# data structure that handles elements in order from a high to a low assigned priority
import copy
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
            for coordinate in path:
                if self.chip.grid[coordinate[0]][coordinate[1]][coordinate[2]] != -1:
                    self.chip.grid[coordinate[0]][coordinate[1]][coordinate[2]] += 1

            net = Net(path)
            start_gate.connections.append(end_gate.id)
            end_gate.connections.append(start_gate.id)
            self.chip.nets.append(net)
    
    def search(self, start_gate, end_gate):
        
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

        #print(pq.empty())
        while not pq.empty():
            
            location = pq.get()
            if location == (1, 6, 0):
                print("cheeeeeck")

            choose, gates = self.chip.available_neighbors(location)
            
          
            if end_coordinates in gates:

                #print(end_coordinates)
                came_from[end_coordinates] = location
                break

            for option in choose:
                new_cost = costs_so_far[location] + 1 + self.chip.cost(location, option)
                if (sx, sy, sz) == (1, 5, 0) and end_coordinates == (4, 4, 0) and option == (1, 6, 0): 
                    print(f"Option: {option}, cost: {new_cost}")
                if option not in costs_so_far or new_cost < costs_so_far[option]:
                    costs_so_far[option] = new_cost
                    priority = new_cost + self.heuristic(option, end_coordinates)
                    #if (sx, sy, sz) == (1, 5, 0) and end_coordinates == (4, 4, 0) and option == (1, 6, 0): 
                        #print(f"priority 1, 6, 0: {priority}")
                        #print(pq.queue)
                    pq.put(option, priority)
                    #print(pq.queue)
                    came_from[option] = location
        
        if pq.empty():
            came_from[end_coordinates] = location
        self.chip.weights.clear()
        return came_from, (sx, sy, sz), end_coordinates
        #return self.search(start_gate, end_gate)
    
    # def undo_connection(self, start_co, end_co):
    #     """Removes the path made from the grid an removes net from chip"""
    #     for net in self.chip.nets:
    #         if net.path[0] == (start_co[0], start_co[1], 0) and net.path[-1] == (end_co[0], end_co[1], 0):
    #             for i in range(1, len(net.path), 1):
    #                 x,y,z = net.path[i]
    #                 self.chip.grid[x][y][z] -= 1
                
    #             self.chip.nets.remove(net)
                    
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

