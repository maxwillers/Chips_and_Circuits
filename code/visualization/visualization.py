"""
This file contains the code for both a 2D and a 3D visualization
"""

import matplotlib.pyplot as plt


def visualization(chip):
    """ Visualizes the chips in 2D"""

    # Visualize the nets on the chip
    for i in range(len(chip.nets)):
        plt.plot(*zip(*chip.nets[i].path), '-')

    # Visualize the gates on the chip
    gates_y = []
    gates_x = []
    for i in range(len(chip.gates)):
        gates_y.append(chip.gates[i].y)
        gates_x.append(chip.gates[i].x)

    # Plot the grid
    plt.plot(gates_x, gates_y, 'rs', markersize=10)
    plt.grid()
    plt.show()


def visualization_3d(chip, output_png):
    """ Visualizes the grid in 3D"""

    # Create a 3D graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_zlim(0, chip.height)
    ax.set_ylim(0, chip.length)
    ax.set_xlim(0, chip.width)

    # Visualize the nets on the chip
    for i in range(len(chip.nets)):
        ax.plot(*zip(*chip.nets[i].path), '-')

    # Visualize the gates on the chip
    gates_y = []
    gates_x = []
    for i in range(len(chip.gates)):
        gates_y.append(chip.gates[i].y)
        gates_x.append(chip.gates[i].x)
    ax.plot(gates_x, gates_y, 'rs', markersize=8)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    # Add the total wire cost a particular instance's nets
    ax.set_title(f'Total wire cost: {chip.calculate_value()}', fontsize=10, fontweight='normal')
    

    # Plot the grid
    plt.grid()
    plt.show()
    plt.savefig(output_png)
