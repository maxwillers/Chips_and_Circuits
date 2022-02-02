### The "code" folder contains three important folders, namely "algorithms", "classes" and "visualization". This README is written to serve as an elaboration on the files contained in these three maps and on their functions.

## Algorithms
- **astar.py:**
- The A* ("astar") algorithm is based on the Dijkstra algorithm, which is also known as the "shortest-path-finder" algorithm.  Whereas the Dijkstra algorithm chooses the paths by solely looking at the costs and selecting the lowest one, the A* algorithm also incorporates a certain heuristic in its calculations.  The heuristic that was chosen here is based on the so-called "Manhattan distance" or "Manhattan metric".  
- An important feature of the A* algorithm is that it works with a priority queue.  Here all possible options for the path are stored and the lowest costs are given the highest priority. Working from lowest to highest multiple possible paths are explored.  The queue is updated once a cheaper route has been found and along the way the data structure keeps track of the direction the net came from.  When the entire queue is worked through, the path, is backtracked and the best found solution is returned.  Inspiration for our priority queue was taken from [www.redblobgames.com](https://www.redblobgames.com/pathfinding/a-star/implementation.html).

- **greedy_itt**
- The greedy algorithm is designed to make the best choices possible locally, meaning for each step along the way.  To implement this, a distinction has been made between types of so-called neighbours, meaning the neighbouring points on the grid.  A neighbouring point is classified as a "best_neighbours" if the coordinates are closer to the end gate coordinates.  They are seen as "medium_neighbours" if they are closer to the end gate but on a higher level, so with a higher z-coordinate.  If there are no options which meet either of these conditions, the path will select one of the other possible neighbours randomly. 
- In this greedy algorithm the netlists are sorted from shortest to longest distance between the two gates, using the Manhattan metric to do so.
- SNAP NIET HELEMAAL ADD CONNECTION EN UNDO CONNECTION

- **greedy_random**


- **hillclimber.py**
- This file contains the hillclimber class.
- The hillclimber can be applied to either of the other algorithms.  The selected algorithm is then taken as a starting point and hillclimber will run n amount of times.  If one of the runs turns up a better solution (so with lower total costs), the previous solution will be swapped for this improved one. *WAT TE DOEN IN COMMAND LINE?*

- **randomise.py**
- The run_random function is the main function used to generate a semi-random solution to the case.
- This function is more of a semi-random algorithm, seeing as a complete random algorithm has a too extremely low chance of generating a succesful solution (one that connects all the gates as is stated in the netlist).  The nets are forced to connect with their end gate is these coordinates can be found among the available neighbours.
- The available_neighbours function called here can be found in chips.py
- The nets in the netlist are sorted in run_random using the manhattan_dis_sort function which can be found in helpers.py.
- The random_path function is called in run_random and serves to generate random paths for the nets.
- This algorithm uses recursion and call itself when a succesful solution could not be generated.  The recursion limit is set at 5000 and the program will quit if a recursion error occurs.


## Classes 
- **chips.py:**
- Contains the Chip class which is used to create a grid.
- Adds the gates to the chip using the add_gates function.
- The good_neighbours function that determines which directions a path can take from a certain position.  This function is called in the
astar.py, greedy_2.py, greedy_itt.py and randomise.py files.
- The is_solution function return True if all the gates are succesfully connected as the netlist prescribes. 
- The calculate_intersections is needed in order to calculate the costs of the nets, seeing as an intersection adds 300 to total.
- The calculate_value function uses the calculated intersections to determine the total cost. This function is called in main.py. 
- Also contained here is the df_output function which for each net returns a list of the coordinates that net's wire crosses.
- The cost function is called in astar.py and is an essential component of the Dijkstra and therefore A* algorithm.

- **gate.py:**
- Contains the Gate class in which the gate ID, the corresponding coordinates and a list of gates to which it should be connected with.

- **net.py:**
- Contains the Net class which is used to create a "path" or "net" between tho gates.


## Visualization
- **visualization.py:**
- This file contains functions for both a 2D as a 3D visualization of the chips.  However, as the 3D visualization is what is actually needed for solving this case, the visualization_3d function is what is called in main.py.  The need to switch to a 2D representation should not arise and is therefore not made easily accessable.  It can be seen that the two functions are fairly similar; adding the third dimension is the main difference.  The vizualization function therefore only remains in this file to show the process of how the 3D visualization came to be.
- For the visualizations the matplotlib library was used. 