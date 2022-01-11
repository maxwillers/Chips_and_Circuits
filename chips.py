import grid
import sys
import pandas as pd
import argparse

def main(netlist_file, print_file):
    netlist = pd.read_csv(netlist_file)
    print_grid = pd.read_csv(print_file)
    print(netlist)
    print(print_grid)


if __name__ == "__main__":

    
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="make chip circuit")

    # Adding arguments
    parser.add_argument("netlist_file", help="input file (csv)")
    parser.add_argument("print_file", help="input print file (csv)")
   
    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.netlist_file, args.print_file) 
    

