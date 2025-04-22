
# NetDecom Documentation

## Overview
NetDecom is a Python package for advanced graph analysis, providing algorithms for convex subgraph extraction and recursive decomposition of both undirected graphs (UGs) and directed acyclic graphs (DAGs). Built on NetworkX, it offers efficient implementations of three core functionalities.

## Installation

```pycon
>>> pip install NetDecom
```

## Core Functionalities

### 1. Convex Hull Identification in Undirected Graphs
Finds the minimal convex subgraph containing a given node set R:

```pycon
>>> import NetDecom as nd
>>> import networkx as nx
>>> G = nx.Graph([(1, 2), (2, 3), (3, 4)])
>>> nd.IPA(G, [1, 3])  # Inducing Path Absorbing Algorithm
>>> nd.CMSA(G, [1, 3])  # Close Minimal Separator Absorbing Algorithm
```

### 2. Recursive Graph Decomposition
Decomposes graphs into maximal prime subgraphs using MCS ordering:

```pycon
>>> MCS = [1, 2, 3, 4]  # Maximum Clique Sequence
>>> nd.Decom_CMSA((G, MCS))  # CMSA-based decomposition
>>> nd.Decom_IPA((G, MCS))  # IPA-based decomposition
```

### 3. Directed Convex Hull Identification in Directed Acyclic Graphs
Finds the minimal d-convex subgraph containing a given node set R:

```pycon
>>> G = nx.DiGraph([(1, 2), (2, 3), (3, 4)])
>>> nd.CMDSA(G, [1, 3])  # Close Minimal D-Separator Absorbing Algorithm
```

### 4. Random Graph Generation
Generates random connected graphs, including UGs and DAGs, with specified parameters for node count and edge probability.

#### `generator_connected_ug(n, p)`
#### `generate_connected_dag(n, p, max_parents=3)`
#### Parameters:
- `n` (int): The number of nodes in the graph.
- `p` (float): The probability of adding an edge between any pair of nodes (for UG) or from a parent node to a child node (for DAG). The value should be between 0 and 1.
- `max_parents` (int, optional): The maximum number of parent nodes for each node in the DAG. Defaults to 3.

#### Returns:
- A connected graph (`networkx.Graph` for UG or `networkx.DiGraph` for DAG).

#### Example:

```pycon
>>> ug = nd.generator_connected_ug(10, 0.3)  # Generate a connected UG with 10 nodes and edge probability 0.3
>>> dag = nd.generate_connected_dag(10, 0.3, max_parents=3)  # Generate a connected DAG with 10 nodes, edge probability 0.3, and maximum parents 3
```

### 5. Load Example Graphs

#### `get_example(file_name)`
Reads the specified example file from the library and returns the corresponding undirected NetworkX graph object.

#### Parameters:
- `file_name` (str): The name of the example file to be read. The following example files are available:
    - `Animal-Network.txt`
    - `as20000102.txt`
    - `bio-CE-GN.txt`
    - `bio-CE-GT.txt`
    - `bio-DR-CX.txt`
    - `CA-CondMat.txt`
    - `CA-HepTh.txt`
    - `DD6.txt`
    - `Email-Enron.txt`
    - `mammalia-voles-rob-trapping-22.txt`
    - `rec-amazon.txt`
    - `rec-eachmovie.txt`
    - `rec-movielens-tag-movies-10m.txt`
    - `rec-movielens-user-movies-10m.txt`
    - `rec-movielens.txt`
    - `rec-yelp-user-business.txt`

#### Returns:
- A NetworkX UG object corresponding to the specified example file.

#### Example:

```pycon
>>> G = nd.get_example("Email-Enron.txt")  # Load the Enron email network as an UG


## Notes
- All input graphs must be NetworkX Graph/DiGraph objects.
- MCS ordering should follow graph topology.
- DAG decomposition features are under development.
