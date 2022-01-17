import random
import copy


def firstCoordinatePositive():
    """
    Continues the net path by adding 1 to the first coordinate
    """
    pass


def firstCoordinateNegative():
    """
    Continues the net path by subtracting 1 from the first coordinate
    """
    pass


def secondCoordinatePositive():
    """
    Continues the net path by adding 1 to the second coordinate
    """
    pass


def secondCoordinateNegative():
    """
    Continues the net path by subtracting 1 from the second coordinate
    """
    pass


def thirdCoordinatePositive():
    """
    Continues the net path by adding 1 to the third coordinate
    """
    pass


def thirdCoordinateNegative():
    """
    Continues the net path by subtracting 1 from the third coordinate
    """
    pass


# convert the tuple containing the coordinates to a list to make it mutable
# dus gaat erom: verander eerste coordinaat met + of - 1 / verander tweede coordinaat met dat of derde
# convert it back to a tuple and put it in a list of tuples, only if the move is possible in this particular instance
# randomly choose one of the functions from the list and run it
# save the new coordinates as the new starting point and save all the coordinates in a list; so one list per net 


def random_path(graph, start_coordinate, end_coordinate):
    """
    Assign each net with a randomized path
    """
    # Generate a random path for each net in the netlist
    # for net in netlist:
        # while start_coordinate != end_coordinate:

    # Create a list of tuples containing all the possible options for a particular position on the grid

    choose = (firstCoordinatePositive, firstCoordinateNegative, secondCoordinatePositive, secondCoordinateNegative, thirdCoordinatePositive, thirdCoordinateNegative) 
    random.choice(choose)() 
 





def random_reassignment(graph, possibilities):
    """
    Algorithm that reallocates the taken paths until each net is valid.
    CAUTION: may run indefinitely.
    """
    new_graph = copy.deepcopy(graph)

    # Randomly assign a value to each of the nodes
    random_path(new_graph, possibilities)

    # Find nodes that are "violations" and have neighbours with same value
    violating_nodes = new_graph.get_violations()

    # While we have violations
    while len(violating_nodes):
        # Reconfigure violations randomly
        random_reconfigure_nodes(new_graph, violating_nodes, possibilities)

        # Find nodes that are violations
        violating_nodes = new_graph.get_violations()

    return new_graph