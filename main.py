# Created By: Madelief Verburg, Max Willers en Nikki van der Woord
# Created Date: 02/01/22
# Course: Programmeertheorie of the Minor Programmeren
"""
This file contains the function main of the assignment Chips and Circuits
"""

import pandas as pd
import argparse
from code.classes.chips import Chip
from code.visualization.visualization import visualization_3d
from code.algorithms.greedy import Greedy
from code.algorithms.randomise import Random
from code.algorithms.greedy_2 import Greedy_random
from code.algorithms.astar import Astar



def main(netlist_file, gate_coordinates, output_png):

    scores = []
    total = 0
    i = 0
    # Make lists of the gates located on the chip and of the connections that are to be made between gates
    netlist = pd.read_csv(netlist_file)
    gate_coordinates = pd.read_csv(gate_coordinates)

    # Set the width and height of the grid
    grid_width = gate_coordinates['x'].max() + 1
    grid_length = gate_coordinates['y'].max() + 1

    # Create a chip with gates
    chip = Chip(grid_width, grid_length, netlist, gate_coordinates)
    # score =[]
    # for _ in range(10):
    #     greedy = Greedy_random(chip)
    #     if greedy:
    #         score.append(greedy.chip.calculate_value())
    # score.sort()
    # print(score)
    # print(f"max:{score[-1]}, min: {score[0]}, avarage:{mean(score)}")
    # print(f"sollutions:{len(scores)}")
    
    astar = Astar(chip)
    # # Make a dataframe
   
    
    # Make a dataframe
    #output = astar.chip.df_output()

    #score = {'net': netlist_file.split("gates_netlists/")[1].replace("/", "_").split(".csv")[0], 'wires': astar.chip.calculate_value()}
    #output = output.append(score, ignore_index=True)
    #print(output)
    #output.to_csv('output.csv', index=False)
    
    # Visualize the chip
    visualization_3d(astar.chip, output_png)


if __name__ == "__main__":

    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="make chip circuit")

    # Adding arguments
    parser.add_argument("netlist_file", help="input file (csv)")
    parser.add_argument("gate_coordinates", help="input print file (csv)")
    parser.add_argument("output_png", help = "output file (png)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.netlist_file, args.gate_coordinates, args.output_png)
