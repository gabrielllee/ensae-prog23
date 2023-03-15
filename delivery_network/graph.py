class Graph:
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.list_of_neighbours = []
        self.list_of_edges = []
        self.max_power = 0
    

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1
        self.list_of_edges.append((node1,node2,power_min))
    


    def get_path_with_power(self, src, dest, power):
        ancetres = self.bfs(src, dest, power) #ancetres est encore le dicitonnaire qui a comme clé un noeud et comme valeur 
        #celui par lequel on a pu parvenir à ce noeud.
        parcours = []
        #on crée une liste parcours qui nous donnera le parcours entre les deux noeuds choisis en respectant toujours la puissance 
        #exigée.
        a = dest #on renomme dest en a pour faciliter la suite.
        if a not in ancetres:
            return None
            #s'il n'y a pas de graphe connexe avec la puissance exigée, on retourne none.
        while a != src:
            #On met cette condition car on part de l'arrivée de notre bfs, donc on remonte point par point jusqu'à arriver à 
            #notre point de départ.
            parcours.append(a)
            a = ancetres[a]
            #on rajoute le sommet a à notre liste de noeuds parcourus et on définit "le nouveau" a comme étant son ancêtre pour
            #rebrousser chemin.
        parcours.append(src)
        #on doit ajouter l'origine a la main parce que notre boucle while s'arrête dès lors que a prend la valeur du noeud de départ
        #et ne le rajoute donc pas dans la liste.
        parcours.reverse()
        return parcours


    def dfs(self, node, visites, composantes, power=1000000000):  
    #on a rajouté une condition de puissance afin de pouvoir conditionner les chemins possible dans la question 
    #traitant de la puissance minimale à avoir pour un trajet. On met une valeur très importante par défaut pour 
    #éviter qu'il n'ampute des trajectoires possibles sur des graphes
        visites.append(node) 
    #on prend un point à partir duquel on veut commencer notre dfs et on l'ajoute à la liste 
    #visites qui conservera tous les noeuds déjà visités
        composantes.append(node)
    #la liste composantes n'est ici pas indispensable mais sera utile pour la question qui suit 
        for i in self.graph[node]: 
            if i[0] not in visites and power >= i[1]: 
                self.dfs(i[0], visites, composantes, power=power) 
                #ici est la recursion de la fonction. On lui demande de s'appliquer elle-même à chaque noeud qui n'est pas 
                #encore présent dans la liste "visites". On rajoute également une condition sur la puissance lorsque cela est nécessaire. 
        return visites
                
#et on applique à nouveau la fonction pour qu elle visite tous les voisins des voisins etc...   

    def connected_components(self) :
        visites = []
        gde_liste = []
        #on crée une grande liste qui sera une liste de liste de tous les noeuds reliés. C'es-à-dire que chaque liste 
        #présente dans la liste soit un graphe connexe avec tous les noeuds qu'elle contient. 
        for i in self.graph:
            if i not in visites:
                composantes=[]
                #on a donc ici la liste de compostantes qui se reset à chaque itération tandis que la liste de visites
                #reste inchangé. 
                #Comme on parcours chaque noeud et que visites garde en mémoire tous les noeuds qui ont été visités,
                #on a donc une nouvelle liste qui se crée qu'à condition qu'il n'y ait aucuun noeud dans une précédente liste.
                self.dfs(i, visites, composantes)
                gde_liste.append(composantes)
        return gde_liste
        
    def bfs(self, beg, dest, power=-1):
        ancetres = {}
        #le dictionnaire ancetres est le dicitonnaire qui permet d'avoir le lien entre chaque sommet, c'est-à-dire que la clé est le 
        #sommet en question et sa valeur est le noeud par lequel on est arrivés. 
        queue = []
        visited = set()
        #on fait un set pour les noeuds visités pour éviter d'avoir des boucles étant donné que le set ne gardera
        #qu'une fois chaque noeud. 
        queue.append(beg)
        while len(queue) > 0:
            n = queue.pop()
            #le while est conditionné par la longueur de la queue du fait de l'utilisation de pop. Comme on a une queue on supprime le 
            #dernier élément de cette liste pour chercher les autres sommets. 
            for v in self.graph[n]:
                if v[0] not in visited and power >= v[1]:
                    #on garde la condition dans les visites pour ne pas faire de boucle et on rajoute celle sur la puissance pour coller
                    #aux conditions de base. De la sorte, on considère qu'il n'y a pas d'arêtes si la puissance de celle-ci
                    #est supérieure à la puissance donnée comme paramètre. 
                    queue.append(v[0])
                    #on rajoute tous les voisins du noeud en question à la liste de queue pour avoir tous les chemins
                    ancetres[v[0]] = n
                    #on définit la valeur comme le noeur à partir duquel on est arrivés.
                    visited.add(v[0])
                    #et on le rajoute au set des visites comme pour éviter les boucles.
        return ancetres


    def BS(self, liste, power):
        #code de BS "de base" utilisé pour avoir une idée de comment coder le binary search de min_power
        haut = len(liste)-1
        bas = 0
        mid = 0
        while bas <= haut:
            mid = (haut+bas)//2
            if liste[mid] < power:
                bas = mid+1
            elif liste[mid] > power:
                haut = mid-1
            elif liste[mid] == power:
                return mid
        return -1 #si on arrive la c est que l element etait po dans la liste

    def power_nodes(self, node1, node2): #fonction un peu inutile utilisée à des fins d'entraînement
        liste = self.graph[node1]
        for i in liste:
            if i[1] == node2:
                power = i[3]
        return power
    



    def min_power(self, src, dest):
        debut = 1
        fin = self.max_power
        if dest not in self.dfs(src, [], []):
            return None, None
        #si les deux noeuds en question ne sont pas sur un graphe connexe, on retourne none car il n'y a pas de chemins possible. 
        while debut != fin: 
            #on fait une recherche binaire. 
            #Pour être tout à fait honnête, la condition sur le while est un peu désuète étant donné qu'on fait un break
            #avant que cette condition puisse se remplir mais c'est la solution qui a le mieux marché sur plusieurs tests : 
            #network.1 et network.2, lentement mais sûrement.
            mid = ((debut+fin)//2)
            actu=self.dfs(src, [], [], power=mid)
            #on actualise à chaque itération le graphe des sommets formant un graphe connexe et permettant un chemin. 
            if dest in actu:
                fin = mid
            #si le sommet qu'on veut atteindre est dans le graphe fait à partir de la médiane des puissances
            #on redéfinit la "borne sup" comme étant l'ancien milieu pour retrécir notre champ de recherche.
            elif dest not in actu:
                debut=mid
            #on procède pareillement mais avec la plus petite puissance dans le cas contraire.
            if fin-debut == 1 :
                break
            #Comme on ne prend pas comme valeurs de power les puissances présentes dans le graphe mais simplement 
            #les entiers situés entre la plus grande puissance et la plus petite, 
            #la condition pour sortir de la boucle while est que la différence entre les deux extrêmes soit égale à un. 
            #Ainsi, cela signifierait que ce sont deux entiers qui se suivent et on doit donc nécessairement prendre 
            #"fin" car début serait trop petit. 
        minus=fin
        return self.get_path_with_power(src, dest, minus), minus
        #en testant cette fonction sur le network.2 avec comme noeuds 1 et 12, voici le résultat obtenu :
        # ([1, 2, 4, 12], 52761). C'est assez long mais il parvient au résultat sans trop de soucis. 

    def connected_components_set(self):
        return set(map(frozenset, self.connected_components()))
    

def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    g: Graph
        An object of the class Graph with the graph from file_name.
    """
    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())
        g = Graph(range(1, n+1))
        for _ in range(m):
            edge = list(map(int, file.readline().split()))
            if len(edge) == 3:
                node1, node2, power_min = edge
                g.add_edge(node1, node2, power_min) # will add dist=1 by default
            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)
            else:
                raise Exception("Format incorrect")
    return g


class Union_Find():

    def __init__(self):
        self.rank = -1
        self.parent = -1

    def make_set(self):
        self.parent = self
        self.rank = 0
    
    def find(self):
        while self != self.parent:
            self = self.parent
        return self

# A function that merges two sets of x and y,
# in this case the sets being connected components of nodes    
    def union(self, y):
        root_x = self.find()
        root_y = y.find()    
        if root_x == root_y :
            return 
        if root_x.rank > root_y.rank:
            root_y.parent = root_x
        else:
            root_x.parent = root_y
            if root_x.rank == root_y.rank:
                root_y.rank = root_y.rank + 1


def kruskal(input_graph):
    """
    Gives the minimum spanning tree (MST) of an input graph using Kruskal's algorithm
    We use the union-find method to detect cycles as suggested in S. Dasgupta et al. (2006)
    Path compression allows to bring complexity down to O(|V|): 
    See below time-complexity comparisons with BFS/DFS
    (This algorithm works adequately on one graph at a time)
    """
    MST = Graph()
    MST.nb_edges = input_graph.nb_nodes - 1
    """
    Preuve (Q.11): Un graphe connexe non orienté est un arbre ssi il a |sommets|-1 arêtes

    """
    # Sorting edges in a nondecreasing order of their power: 
    # the spanning tree produced by iteration will then necessarily be a MST
    input_graph.graph = sorted(input_graph.list_of_edges, key=lambda item: item[2])
    # we use an index (p) to go through these edges in an increasing order of power
    p = 0
    nodes = {}
    for node in input_graph.nodes:
        nodes[node] = Union_Find()
        nodes[node].make_set()
    # When our MST in progress will have |V|-1 edges, it will be complete (see above, Q. 11)
    e = 0
    while e < len(input_graph.nodes)-1:
        # we consider the edge with the smallest power each time
        n1, n2, power = input_graph.graph[p]
        p = p+1
        # if adding the edge doesn't create a cycle, we add it to our MST in progress
        if nodes[n1].find() != nodes[n2].find():
            MST.add_edge(n1, n2, power)
            e = e+1
            # and we take into account that the nodes are now connected
            nodes[n1].union(nodes[n2])
    return MST


def min_power_kruskal_V1(input_graph, src, dest):
    """
    New version of the min_power function, 
    Gives the path with the minimum power between two given nodes
    A twist to bring complexity down and time performance up:
    - preprocessing with the kruskal algorithm
    The complexity is then lowered to O(|V|)
    """
    # Step n° 1: Preprocessing
    MST = kruskal(input_graph)
    #Step n° 2: running min_power on the generated MST
    path, power = min_power(MST, src, dest)
    return path, power



def min_power_kruskal_V2(input_graph, src, dest, power):
    """
    New version of the min_power function, 
    Gives the path with the minimum power between two given nodes
    Two twists bring complexity down and time performance up:
    - preprocessing with the kruskal algorithm
    - lowest common ancestor (LCA) search instead of DFS to find paths before power-sorting them
    This allows to bring complexity down to O(|log(V)|)
    """
    # Step n° 1: Preprocessing
    MST = kruskal(input_graph)
    # Step n°2: Lowest common ancestor
    list_of_parents = kruskal.parents
    ancestors = []
    #We build the list of all ancestors of the start node
    current_node = origin
    while list_of_parents[current_node-1] != current_node:
        ancestors.append(current_node)
        current_node = list_of_parents[current_node-1]
    ancestors.append(current_node)
    #To find the path, we find the lowest common ancestor of the two nodes.
    lca = destination
    while lca not in ancestors:
        lca = list_of_parents[lca-1]

    #The path is simple : starting node -> lca -> ending node
    ascending_path  = []
    descending_path = []
    current_node = origin
    while current_node != lca:
        ascending_path.append(current_node)
        current_node = list_of_parents[current_node-1]
    ascending_path.append(lca)

    current_node = destination
    while current_node != lca:
        descending_path.append(current_node)
        current_node = list_of_parents[current_node-1]
    #Now the path regardless of power is found.
    #To find the power, we collect all powers in that path, and identify the minimum
    path = ascending_path + descending_path[::-1]
    power = input_graph.max_power
    for index in range(len(path)-1):
        origin, destination = path[index], path[index+1]
        destination_index = input_graph.list_of_neighbours[origin-1].index(destination)
        power = min(power, input_graph.graph[origin][destination_index][1])

    # Step n° 3: Filtering by power to get the lowest



    return path, min_power

g = graph_from_file("/home/onyxia/work/ensae-prog23/input/network.2.in")
print(g.min_power(1, 12))
