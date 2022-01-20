# A* simple pseudocode
# Open list; the set nodes to be evaluated
# CLosed list; set of nodes already evaluated
# add the start node to OPENSSL_VERSION

# loop
#     current = node in Open list met de laagste f_cost (g+h)
#     remove current node from open list
#     add to close list

#     if current node = target node (path found)
#         return

#     for eacht neighbour of the current node
#         if neighbour not traversable or neighbour is in close_old_connections  
#             skip to next neighbour

#         if new path to neighbour is shorter (a, b, s example filmpje) or neighbour not in open
#             set f cost of neighbour
#             set parent of neighbour to current node (keeping track for retracing later on)
#             if neighbour is not in open
#                 add neighbour to open
#  we will be exited out of the loop when current == end node 

# als 2 neighbours zelfde f score, moet je algoritme eerste die pakken die als laatste ge add is
# algoritme niet stoppen voor de laatste stap; dus ookal is ht eindpunt al in "zicht", alsnog doorgaan met de loop, pas stoppen als de end == cuurent

# de open list is children a.k.a. possibilities; possible paths

# 