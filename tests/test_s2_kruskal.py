# This will work if ran from the root folder.
import sys 
sys.path.append("delivery_network")

from graph import graph_from_file, kruskal
import unittest   # The test framework

def test_kruskal ():
    """
    On crée un graphe G avec une boucle grâce à addd_edge
    On le teste avec Kruskal qui doit rendre le même graphe sans la dernière arête. On le nomme K
    """
    G=Graph([k for k in range (1,4)]) 
    K=Graph([k for k in range (1,4)])
    for k in range(1,4) :
        G.add_edge(k, k+1, k)
        test.add_edge(k,k+1,k)
    G.add_edge(4, 1, 4)
    print (test_kruskal)

    return (G.kruskal().graph==K.graph)

if __name__ == '__main__':
    unittest.main()