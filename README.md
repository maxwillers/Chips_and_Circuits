# Chips and Circuits
### A program containing various algoritms used to solve the Chips and Circuits problem case
##### By Madelief Verburg, Max Willers & Nikki van der Woord
------------------------------------------------------

## Introduction
This program has been created for the 'Chips and Circuits' project for the Programming Theory course, which is part of the UvA's Programming minor.

It attempts to find the most sufficient way to wire a chip. A chip contains several gates, each with their own coordinates. These gates need to be connected with each other through nets. Which gates should be connected with which gate is stated in a given netlist. The goal of this program is to be able to generate solutions in which the gates are connected according to the netlist in the most optimized way as is possible. The aim is to find solutions while keeping the total costs of the placed nets as low as possible.

The total cost are calculated as follows:
    total cost = units of wire + 300 * intersections

Hereby the **units of wire** is every coordinate the wire passes and an **intersections** occurs when two wires cross the same coordinate. This formula goes to show that finding the shorest paths for all the nets is not the issue to be taken in to consideration, and that intersections should be avoided as much as possible, as these amp up the cost drastically. 

Furthermore, there are some restrictions regarding laying down the nets:
-  **Collision** is not allowed
    - collisions happen when two units run allong the same path
- The path cannot go past the chip
    - the chip grid is the size of the outer gate coordinates + 1. so it starts at 0 and ends at max x value +1 and max y value +1. The chip always has a height of 7.

--------------------------------------------------
## Run 
- To run the model, run ``main.py`` with command in this directory. e.g.

```
    $ python3 main.py *netlist_file* *print_file* *output_png* *output_batch_file* *algorithm* *sorting* *times_batch_run*
```
- commands that need to be added
    - **netlist_file**: find the netlist files in the *gates_netlist* map
    - **print_file output_png**: find the print files in the *gates_netlist* map
    - **output_png** : the name of the visualization output
    - **output_batch_file** : the name of the batch_run csv output
    - **algorithm sorting**: the algorithm that will be ran
        - algorithm options:
            - astar   : astar algorithm
            - astar_hill  : astar algorithm with hillclimber
            - greedy_it  : itterative greedy algorithm
            - greedy_non_it   : non-itterative greedy algorithm
            - random  : random algorith
    - **sorting**: the sorting algorithm that will be ran
        - sorting options:
            - manhattan  : sorts from lowest distance to highest
            - random   : randomly sorts
    - **times_batch_run**: the amount of times a algorithm will be ran in the batch run


### example 
running netlist 4 with astar_hill algorithm with manhattan sort a 100 times:
```
    $ python3 main.py gates_netlists/chip_1/netlist_4.csv gates_netlists/chip_1/print_1.csv plot.png batch_run.csv astar_hill manhattan 100
```

---------------------------------------------------

## Technologies
Project is created with:
* Python version: 3.9
* Matplotlib library version: 3.4

--------------------------------------------------
## Files
The code exists of several folders:
- **code**: contains three important folders, namely:
    - algorithms: the random, greedy and A* algoritms are stored here
    - classes: the Chip, Net and Gate classes are kept here
    - visualization: contains files for a 3D visualization using matplotlib
    - README.md: an extra readme file that elaborates on the files contained in the folders mentioned above
- **gate_netlist**: contains this case's provided chips and their netlists
- main.py: to run the code

