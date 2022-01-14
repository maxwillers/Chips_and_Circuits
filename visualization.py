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


def visualization_3d(chip):
    """ visualizing the 3d chips"""
    # Create 3d graph
    fig=plt.figure()
    ax=fig.add_subplot(111,projection='3d')
    ax.set_zlim(0,chip.height)
    ax.set_ylim(0,chip.length)
    ax.set_xlim(0,chip.width)

    # Visualize nets on chip
    for i in range(len(chip.nets)):
        ax.plot(*zip(*chip.nets[i].path), '-')
    
    # Visualize the gates on chip
    ax.plot(chip.gates[0], chip.gates[1], 'rs', markersize = 10)

    plt.grid()
    plt.show()
   