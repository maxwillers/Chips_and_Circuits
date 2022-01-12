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
    plt.plot(chip.gates[0],chip.gates[1], 'ro')

    plt.plot([1, 2, 3, 4, 5, 6, 6, 5, 4, 4, 5, 6],[5, 5, 5, 5, 5, 5, 4, 4, 4, 3, 2, 2], 'k-')
    plt.grid()
    plt.show()


