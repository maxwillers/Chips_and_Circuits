# Created By: Madelief Verburg, Max Willers en Nikki van der Woord
# Created Date: 02/01/22
# Course: Programmeertheorie of the Minor Programmeren
"""
This file contains the function main of the assignment Chips and Circuits
"""

import pandas as pd
import argparse
from code.algorithms import hillclimber
from code.classes.chips import Chip
from code.visualization.visualization import visualization_3d
from code.algorithms.greedy import Greedy
from code.algorithms import randomise 
from code.algorithms.greedy_2 import Greedy_random
from code.algorithms.greedy_itt import Greedy_itt
from code.algorithms.astar import Astar
from code.algorithms.hillclimber import Hillclimber


def main(netlist_file, gate_coordinates, output_png, algorithm):

    # Make lists of the gates located on the chip and of the connections that are to be made between gates
    netlist = pd.read_csv(netlist_file)
    gate_coordinates = pd.read_csv(gate_coordinates)

    # Set the width and height of the grid
    grid_width = gate_coordinates['x'].max() + 1
    grid_length = gate_coordinates['y'].max() + 1

    # Create a chip with gates
    chip = Chip(grid_width, grid_length, netlist, gate_coordinates)
    all_output = []
    score_2 = []
    for _ in range(1):
        if algorithm == 'astar':
            run_chip = Astar(chip)
        elif algorithm == 'greedy':
            run_chip = Greedy_itt(chip)
        elif algorithm == 'random':
            run_chip = randomise.create_netlist(chip)
        
        if run_chip == True:
            score_2.append(run_chip.chip.calculate_value())
    
    print(score_2)
    # print(statistics.mean(score_2))
        

    output = run_chip.chip.df_output()
    score = {'net': netlist_file.split("gates_netlists/")[1].replace("/", "_").replace("netlist", "net").split(".csv")[0], 'wires': run_chip.chip.calculate_value()}
    output = output.append(score, ignore_index=True)
        # all_output.append(output)  
    
    # Make a dataframe
    output.to_csv('output.csv', index=False)
    
    # Visualize the chip
    visualization_3d(run_chip.chip, output_png)

    hill = Hillclimber(run_chip)

    visualization_3d(run_chip.chip, 'out2.png')

if __name__ == "__main__":

    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="make chip circuit")

    # Adding arguments
    parser.add_argument("netlist_file", help="input file (csv)")
    parser.add_argument("gate_coordinates", help="input print file (csv)")
    parser.add_argument("output_png", help = "output file (png)")
    parser.add_argument("algorithm", help = "algorithm you want to use")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.netlist_file, args.gate_coordinates, args.output_png, args.algorithm)
