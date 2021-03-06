"""
main.py
Created By: Madelief Verburg, Max Willers en Nikki van der Woord
Created Date: 02/02/22
Course: Programmeertheorie of the Minor Programmeren
This file contains the function main of the assignment Chips and Circuits
"""

import pandas as pd
import argparse
from code.classes.chips import Chip
from code.visualization.visualization import visualization_3d
from code.algorithms import randomise
from code.algorithms.greedy import Greedy
from code.algorithms.astar import Astar
from code.algorithms.hillclimber import Hillclimber
import time


def main(
    netlist_file,
    gate_coordinates,
    output_png,
    algorithm,
    sorting,
    n_batch,
    output_batch_file,
):

    # Make lists of the gates located on the chip and of the nets
    netlist = pd.read_csv(netlist_file)
    gate_coordinates = pd.read_csv(gate_coordinates)

    # Set the width and height of the grid
    grid_width = gate_coordinates["x"].max() + 1
    grid_length = gate_coordinates["y"].max() + 1

    # Create a chip with gates
    chip = Chip(grid_width, grid_length, netlist, gate_coordinates)
    all_score = []
    all_output = []
    best_chip = []
    time_taken = []

    # Run the requested algoritms the requested amount of times
    for _ in range(int(n_batch)):
        start_time = time.time()
        if algorithm == "astar":
            run_chip = Astar(chip, sorting)
        elif algorithm == "astar_hill":
            run_chip = Astar(chip, sorting)
            hill = Hillclimber(run_chip)
            run_chip = hill.astar_chip
        elif algorithm == "greedy_it":
            run_chip = Greedy(chip, sorting, it=True)
        elif algorithm == "greedy_non_it":
            run_chip = Greedy(chip, sorting, it=False)
        elif algorithm == "random":
            run_chip = randomise.run_random(chip, sorting)
        end_time = time.time()

        # Append results to correct lists
        if algorithm != "random" and run_chip.chip.is_solution() is True:

            # Create output dataframe and append to list
            all_score.append(run_chip.chip.calculate_value())
            output = run_chip.chip.df_output()
            score = {
                "net": netlist_file.split("gates_netlists/")[1]
                .replace("/", "_")
                .replace("netlist", "net")
                .split(".csv")[0],
                "wires": run_chip.chip.calculate_value(),
            }
            output = output.append(score, ignore_index=True)
            all_output.append(output)

            # Append chip and time to specific list
            best_chip.append(
                {
                    "score": run_chip.chip.calculate_value(),
                    "time_run": end_time - start_time,
                    "chip": run_chip.chip,
                    "output": output,
                }
            )
            time_taken.append(end_time - start_time)

        # If random function gives correct solution append to list
        elif algorithm == "random" and run_chip.is_solution() is True:

            # Create output dataframe and append to list
            all_score.append(run_chip.calculate_value())
            output = run_chip.df_output()
            score = {
                "net": netlist_file.split("gates_netlists/")[1]
                .replace("/", "_")
                .replace("netlist", "net")
                .split(".csv")[0],
                "wires": run_chip.calculate_value(),
            }
            output = output.append(score, ignore_index=True)
            all_output.append(output)

            # Append chip and time to specific list
            best_chip.append(
                {
                    "score": run_chip.calculate_value(),
                    "time_run": end_time - start_time,
                    "chip": run_chip,
                    "output": output,
                }
            )
            time_taken.append(end_time - start_time)

        # If run did not give solution note down fail in the list
        else:
            all_output.append("fail")
            all_score.append("fail")

            # Still append time taken
            time_taken.append(end_time - start_time)

    # Create a big dataframe file with all information in it
    batch_run = pd.DataFrame(
        data={"score": all_score, "output": all_output, "time": time_taken}
    )
    batch_run.to_csv(output_batch_file, index=False)

    # Visualize the best solution and make output
    best = sorted(best_chip, key=lambda d: d["score"])
    if len(best) > 0:
        visualization_3d(best[0]["chip"], output_png)
        best[0]["output"].to_csv("output.csv", index=False)
    else:
        print("Sorry no sollution was found")
        return False


if __name__ == "__main__":

    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="make chip circuit")

    # Adding arguments
    parser.add_argument("netlist_file", help="input file (csv)")
    parser.add_argument("gate_coordinates", help="input print file (csv)")
    parser.add_argument("output_png", help="output file (png)")
    parser.add_argument("output_batch_file", help="name of output batchrun file(csv)")
    parser.add_argument("algorithm", help="algorithm you want to use")
    parser.add_argument("sorting", help="sorting algorithm to be used")
    parser.add_argument("n_batch", help="number of times batch is ran")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(
        args.netlist_file,
        args.gate_coordinates,
        args.output_png,
        args.algorithm,
        args.sorting,
        args.n_batch,
        args.output_batch_file,
    )
