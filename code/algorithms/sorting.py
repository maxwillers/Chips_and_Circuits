"""
sorting.py
This file contains functions that can sort the netlist:
- manhatan_dis_sort : sorts the list based on their manhatan distance
- union_sort: 
- random_sort: randomly sorts the netlist 
"""

import random
import math


def dist(p0,p1):
        """Calculates the distance between two points"""
        return math.sqrt((p1[0]-p0[0])**2+(p1[1]-p0[1])**2)
    
def manhatan_dis_sort(connections):
    """Sorts the netlist based on the distance between the gates"""
    connections_new =[]
    for connection in connections:
        start, end = connection
        connections_new.append({'start_gate': start, 'end_gate': end, 'start_co': [start.x, start.y], 'end_co':[end.x, end.y]})
    connections = sorted(connections_new, key=lambda p:self.dist(p['start_co'],p['end_co']))

    return connections


def union_sort(connections):
    """Sorts the netlist based on the location of the gates (from outside to inside)"""
     netlistVersion2 = deepcopy(netList)
        # lege derde versie van te definiëren netlist opgeslagen
        netlistVersion3 = []
        # lengte netlist berekend
        k = len(netList)

        # de breedte van het eerste veld is 17 (tellend vanaf 0)
        width = 17
        # de hoogte van het eerste veld is 12 (tellend vanaf 0)
        height = 12

        # helftbreedte en hoogte worden berekend om het bord te scheiden
        halfWidth = width / 2
        halfHeight = height / 2

        # itereren over lengte netlist
        for j in range(0, k):
            # het minimum worddt op een hoog getal gezet
            minimum = 1000
            # numbernetlist wordt 0
            numberNetList = 0

            # itereren over lengte netlist min j
            for i in range(0, k - j):
                # de eerste factor van wire opslaan in listelement1
                listElement1 = netlistVersion2[i][0]
                # de tweede factor van wire opslaan in listelement2
                listElement2 = netlistVersion2[i][1]

                # check of de x-waarde in de eerste helft valt
                if (gate[listElement1].x <= halfWidth):
                    x1Value = gate[listElement1].x
                else:
                    # anders wordt de waarde breedte minus x-element
                    x1Value = width - gate[listElement1].x

                if (gate[listElement1].y <= halfHeight):
                    y1value = gate[listElement1].y
                else:
                    y1value = height - gate[listElement1].y

                # de waarde van de eerste gate is het
                # minimum van de x1- en y1waarde
                value1 = min(x1Value, y1value)

                if (gate[listElement2].x <= halfWidth):
                    x2Value = gate[listElement2].x
                else:
                    x2Value = width - gate[listElement2].x

                if (gate[listElement2].y <= halfHeight):
                    y2Value = gate[listElement2].y
                else:
                    y2Value = height - gate[listElement2].y

                # de waarde van de tweede gate is het
                # minimum van de x2- en y2waarde
                value2 = min(x2Value, y2Value)

                sum = value1 + value2

                # als de som kleiner is dan het minimum
                if (sum < minimum):
                    minimum = sum
                    numberNetList = i

            # zet zojuist bepaalde netlistelement in netlistVersion3
            netlistVersion3.append(netlistVersion2[numberNetList])
            # haalde aangewezen element uit netlistVersion2
            netlistVersion2.pop(numberNetList)
        # return nieuwe netlist
        return netlistVersion3