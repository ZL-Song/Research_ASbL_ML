# Extract atomic charges as numpy arrays. 
# Zilin Song, 05 Dec 2021
# 

import iomisc, numpy

if __name__ == '__main__':
    d1_chrg, d1_chrg_labels = iomisc.loadchrg('d1')
    d2_chrg, d2_chrg_labels = iomisc.loadchrg('d2')

    node_labels = numpy.load('./rawds/label_nodes.npy')

    d1_node_indices = []
    for node in node_labels:
        i = numpy.where(d1_chrg_labels == node)[0] # numpy.where returns an array
        d1_node_indices.append(i)

    d2_node_indices = []
    for node in node_labels:
        i = numpy.where(d2_chrg_labels == node)[0] # numpy.where returns an array
        d2_node_indices.append(i)

    d1_node_indices = numpy.squeeze(numpy.asarray(d1_node_indices))
    d2_node_indices = numpy.squeeze(numpy.asarray(d2_node_indices))

    # Should be the same.
    print(d1_node_indices)
    print(d2_node_indices)

    npath = 500
    nrep  = 36

    d1_node_chrgs = []
    d2_node_chrgs = []

    for ipath in range(npath):
        d1_path_chrg = d1_chrg[ipath]
        d2_path_chrg = d2_chrg[ipath]

        # Take only the reactant.
        d1_rep_chrg = d1_path_chrg[0]
        d2_rep_chrg = d2_path_chrg[0]
        
        d1_node_chrgs.append(d1_rep_chrg[d1_node_indices])
        d2_node_chrgs.append(d2_rep_chrg[d2_node_indices])
        
    d1_node_chrgs = numpy.asarray(d1_node_chrgs)
    d2_node_chrgs = numpy.asarray(d2_node_chrgs)

    numpy.save('./rawds/ges_imi.d1.node_nbo.npy', d1_node_chrgs)
    numpy.save('./rawds/ges_imi.d2.node_nbo.npy', d2_node_chrgs)