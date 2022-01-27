
# Chips and Circuits
### Nikki van der Woord, Max Willers & Madelief Verburg
------------------------------------------------------

# Introduction

This is code for the project 'Chips and Circuits' of the minor computer programming from the UvA.

It attempts to find the most sufficient way to wire a chip. The chip contains several gates with their own coordinates. These gates have to be connected with eachother as is stated in the netlist. The goal is to do this so the costst are the lowest.

The cost are calculated as follows:
    total cost = units of wire + 300 * intersections

Hereby the **units of wire** is every coordinate the wire passes and the **intersections** are when two wires cross the same coordinate.

However there are some restrictions:
-  **collision** are not allowed
    - collisions happen when two units run allong the same path
- The path cannot go past the chip
    - the chip grid is the size of the outer gate coordinates + 1. so it starts at 0 and ends at max x value +1 and max y value +1. The height is 7. 


# Files

The code exists of several folders:
- **code***: contains all important code
    - algorithms: contains all algorithms for a sollution
    - classes: contains all classes for this case
    - visualization: contains files for visualization
- **gate_netlist**: contains the available chips and their netlsit
- main.py: to run the code