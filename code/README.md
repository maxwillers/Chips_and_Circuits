### The "code" folder contains three important folders, namely "algorithms", "classes" and "visualization". This README is written to serve as an elaboration on the files contained in these three maps and their functions.

## Algorithms
* astar.py
- The A* ("astar") algorithm is based on the Dijkstra algorithm, which is also known as the "shortest-path-finder".  Whereas the Dijkstra algorithm chooses the paths by solely looking at the costs and selecting the lowest one, the A* algorithm also incorporates a certain heuristic in its calculations.  The heuristic that was chosen here is based on the so-called "Manhattan distance" or "Manhattan metric".  
- An important feature of the A* algorithm is that it works with a priority queue.  Here all possible options for the path are stored and the lowest costs are given the highest priority. Inspiration for our priority queue was taken from [www.redblobgames.com](https://www.redblobgames.com/pathfinding/a-star/implementation.html).

* greedy_breakthrough
* greedy_itt
* helpers.py 
* hillclimber.py
* randomise.py

## Classes 
* chips.py
* gate.py
* net.py

## Visualization
* visualization.py
- This file contains functions for both a 2D as a 3D visualization of the chips.  However, as the 3D visualization is what is actually needed for solving this case, the visualization_3d function is what is called in main.py.  The need to switch to a 2D representation should not arise and is therefore only accessable through manually changing the visualization_3d function call to the visualization function in main.