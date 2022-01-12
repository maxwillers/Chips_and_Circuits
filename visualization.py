"""
Visualization.py
This file contains the code for a 2D visualization
"""

import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np
from mpl_toolkits.mplot3d import Axes3D



def visualization(chip):
    """ visualizing the chips"""  

    # Visualize nets on chip
    for i in range(len(chip.nets)):
        plt.plot(*zip(*chip.nets[i].path), '-')
    
    # Visualize the gates on chip
    plt.plot(chip.gates[0], chip.gates[1], 'rs', markersize = 10)
  
    plt.grid()
    plt.show()


