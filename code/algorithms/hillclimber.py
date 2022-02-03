"""
hillclimber.py
This file contains the class Hillclimber that implements the hillclimber algorithm.
The hillclimber algorithm does not stand on its own; it is meant to be applied to the astar algorithm as an optional addition.
"""

import copy
import random
from code.algorithms.helpers_net import create_net_on_chip, undo_net


class Hillclimber:
    def __init__(self, chip):
        self.astar_chip = copy.deepcopy(chip)
        self.score = chip.chip.calculate_value()

        # Iterate 2000 times to find the local best solution
        for _ in range(2000):
            new_chip = copy.deepcopy(self.astar_chip)
            self.reconfigure_chip(new_chip)
            self.check_solution(new_chip)

    def reconfigure_chip(self, new_chip):
        """Reconfigures chip, by rearranging a randomly chosen connection"""
        flag = True
        connection_list = []
        for _ in range(2):
            random_connection = random.choice(new_chip.chip.connected_gates)

            # Check if connection has been chosen before otherwise undo connection
            if random_connection not in connection_list:
                connection_list.append(random_connection)
                undo_net(
                    new_chip.chip,
                    random_connection["start_co"],
                    random_connection["end_co"],
                )

                # Create new path and append it to chip
                came_from, start, end = new_chip.search(
                    random_connection["start_gate"], random_connection["end_gate"], flag
                )
                path = new_chip.create_path(came_from, start, end)
                create_net_on_chip(
                    path,
                    new_chip.chip,
                    random_connection["start_gate"],
                    random_connection["end_gate"],
                )
                new_chip.chip.connected_gates.remove(random_connection)
                new_chip.chip.connected_gates.append(random_connection)

    def check_solution(self, new_chip):
        """Check if new solution is better than the old solution"""
        new_score = new_chip.chip.calculate_value()
        old_score = self.score

        if new_score <= old_score:
            self.astar_chip = new_chip
            self.score = new_score
