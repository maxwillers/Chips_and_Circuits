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


## Technologies
Project is created with:
* Python version: 3.9
* Matplotlib library version: 3.4


## Files
The code exists of several folders:
- **code**: contains three important folders, namely:
    - algorithms: the random, greedy and A* algoritms are stored here
    - classes: the Chip, Net and Gate classes are kept here
    - visualization: contains files for a 3D visualization using matplotlib
    - README.md: an extra readme file that elaborates on the files contained in the folders mentioned above
- **gate_netlist**: contains this case's provided chips and their netlists
- main.py: to run the code


## Code examples
* To generate a plot of chip_0 and netlist_1 using the randomise algorithm, use:
`python3 main.py gates_netlists/chip_0/netlist_1.csv gates_netlists/chip_0/print_0.csv plots/plot.png random`
* To generate a plot of chip_1 and netlist_4 using the greedy algorithm, use:
`python3 main.py gates_netlists/chip_0/netlist_3.csv gates_netlists/chip_0/print_0.csv plots/plot.png greedy ` 
* To generate a plot of chip_2 and netlist_7 using the A* algorithm, use:
`python3 main.py gates_netlists/chip_2/netlist_8.csv gates_netlists/chip_2/print_2.csv plots/plot.png astar ` 