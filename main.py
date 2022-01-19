"""
main.py
This file contains the function main of the assignment Chips and Circuits
"""

import pandas as pd
import argparse
from code.classes.chips import Chip
from code.visualization.visualization import visualization, visualization_3d
from code.algorithms.randomise import Random


def main(netlist_file, gate_coordinates):
    # Make lilst of gates on chip and connections to be made between gates
    netlist = pd.read_csv(netlist_file)
    gate_coordinates = pd.read_csv(gate_coordinates)

    # Get width and height of chip 
    grid_width = gate_coordinates['x'].max() + 1
    grid_length = gate_coordinates['y'].max() + 1

    # Create chip with gates 
    chip = Chip(grid_width, grid_length, netlist, gate_coordinates)

    random = Random(chip)


    # Visualize the chip
    visualization_3d(random.chip)
   

if __name__ == "__main__":

    
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="make chip circuit")

    # Adding arguments
    parser.add_argument("netlist_file", help="input file (csv)")
    parser.add_argument("gate_coordinates", help="input print file (csv)")
   
    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.netlist_file, args.gate_coordinates) 
    


