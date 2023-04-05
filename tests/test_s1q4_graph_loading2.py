import sys 
sys.path.append("delivery_network")

from graph import Graph, graph_from_file

import unittest   # The test framework

def test_s1q4_graph_loading ():
    "test pour la question 4 sur le fichier network.04.in"
    g=graph_from_file('network.04.in')
    dist=int(g.graph [1][0][2])

    return (dist==6 or dist==89)
    # car le noeud 1 est relié à 2 avec une puissance de 89,
    # et à 4 avec une puissance de 6.


if __name__ == '__main__':
    unittest.main()