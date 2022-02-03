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
    - collisions happen when two units run allong the same grid segment
- The path cannot go past the chip
    - the chip grid is the size of the outer gate coordinates + 1. so it starts at 0 and ends at max x value +1 and max y value +1. The chip always has a height of 7.
- The path cannot go through gates. 
--------------------------------------------------
## Requirements

Project is created with:
* Python version: 3.9.1
* Matplotlib library version: 3.4.3
* Pandas version: 1.3.4

To succesfully run this code a few packages need to be installed, which are noted in requirements.txt. This packages can be downloaded using pip:

```
pip3 install -r requirements.txt
```
--------------------------------------------------
## Run 
- To run the model, run ``main.py`` with command in this directory. e.g.

```
    $ python3 main.py netlist_file *print_file* *output_png* *output_batch_file* *algorithm* *sorting* *times_batch_run*
```
- commands that need to be added
    - **netlist_file**: find the netlist files in the *gates_netlist* map
    - **print_file**: find the print files in the *gates_netlist* map
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
## Output

When running this model you will receive the following output:
- A visualization of the run with the lowest score 
- An output.csv file including the gates id's, the nets and score. This is the output of the run with the lowest score
- A batchrun file with score, output (same as in the output file) and time of each run

---------------------------------------------------
## Files
The code exists of several folders:
- **code**: contains three important folders, namely:
    - algorithms: the random, greedy and A* algoritms are stored here
    - classes: the Chip, Net and Gate classes are kept here
    - visualization: contains files for a 3D visualization using matplotlib
    - README.md: an extra readme file that elaborates on the files contained in the folders mentioned above
- **gate_netlist**: contains this case's provided chips and their netlists
- main.py: to run the code

--------------------------------------------------
## State space

In order to calculate the state space of this problem we first have to understand all the options there are. Every step we do there could be a maximum of 5 choices: front, left, right, up, down. Every grid point a choice needs to be made. The order in which the choices are made does matter and repition of the choices is possible. Therefore the state space is n^r. Where n = the amount of choices and r the amount of choices to be made.

However in our 3d structure not every grid point has 5 options therefore the state space is smaller. On the outer sides of the 3d structure there are only 2, 3 or 4 options. So to properly calculate the state space we have to take these corners and sides into account.

This will lead to the formulas:
	- r = 8 with n= 2 
	-  r = (4l + 4b +4h - 24) with n = 3 
	-  r= ((h-2) * (b + l -4) + (l-2) * (h-2)) * 2 with n= 4 
	-  r = (l -2) * (b-2) * (h-2)  with n =5

Leading to a total formula:
2^8 * 3^((4l + 4w +4h - 24)) * 4^(((h-2) * (w + l -4) + (l-2) * (h-2)) * 2 ) *  5 ^ ((l -2) * (w-2) * (h-2)) 

So if we calculate this for a grid of length = 6, with =7, height = 7 
    - 2^8 * 3^56 * 4^130 * 5^100 = 2,0 * 10^177



