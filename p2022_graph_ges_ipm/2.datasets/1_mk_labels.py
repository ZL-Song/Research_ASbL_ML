# Make the graph - nodes and edges. 
# Zilin Song, 13 Jan 2022
# 

from json.tool import main
import numpy

def find_nodelabels():
    """Find all labels of nodes."""
    nodes = []
    edges = []

    with open("./edge.log", 'r') as infile:
        for line in infile:
            atom0 = line.split()[0]
            atom1 = line.split()[1]

            if not (atom0 in nodes):
                nodes.append(atom0)
            
            if not (atom1 in nodes):
                nodes.append(atom1)
            
    return numpy.asarray(nodes)

def find_edgelabels():
    """Find all indices of edges"""
    node_labels = find_nodelabels()
    edge_labels = []

    edge_node0  = []
    edge_node1  = []

    with open("./edge.log", 'r') as infile:

        for line in infile:
            atom0 = line.split()[0]
            atom1 = line.split()[1]
            
            node0 = numpy.argwhere(node_labels==atom0)
            node1 = numpy.argwhere(node_labels==atom1)
            
            # Note: append both for undirected edges. 
            edge_node0.append(node0)
            edge_node0.append(node1)
            edge_node1.append(node1)
            edge_node1.append(node0)
            
            if f"{atom0}:{atom1}" in edge_labels or f"{atom1}:{atom0}" in edge_labels:
                print(f"Repeated edge spec: {atom0}:{atom1}")
            edge_labels.append(f"{atom0}:{atom1}")
            edge_labels.append(f"{atom1}:{atom0}") 

    return numpy.squeeze(numpy.asarray([edge_node0, edge_node1])), numpy.asarray(edge_labels)

if __name__ == '__main__':
    node_labels  = find_nodelabels()
    edge_indices, edge_labels = find_edgelabels()

    print(node_labels)
    print(node_labels.shape)
    print(edge_labels)
    print(edge_labels.shape)
    print(edge_indices)
    print(edge_indices.shape)

    numpy.save(f"./rawds/label_nodes.npy", node_labels)
    numpy.save(f"./rawds/label_edges.npy", edge_labels)
    numpy.save(f"./rawds/indices_edges.npy", edge_indices)

    # Note that node indices at 21 is the Ser70 HG1 atom.
