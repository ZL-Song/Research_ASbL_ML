# Make the numpy array for the edge features.
# Normalization.
# Zilin Song, 19 Jan 2022
# 

import numpy 

if __name__ == '__main__':
    d1_edge_dists = numpy.load('./rawds/ges_imi.d1.edge_dist.npy')
    d2_edge_dists = numpy.load('./rawds/ges_imi.d2.edge_dist.npy')


    d1_min_dist = numpy.min(d1_edge_dists, axis=0)
    d2_min_dist = numpy.min(d2_edge_dists, axis=0)

    d1_dif_dist = numpy.max(d1_edge_dists, axis=0) - d1_min_dist
    d2_dif_dist = numpy.max(d2_edge_dists, axis=0) - d2_min_dist

    d1_edge_dists_norm = numpy.ones(d1_edge_dists.shape)
    for i in range(d1_edge_dists.shape[0]):
        d1_edge_dists_norm[i] = (d1_edge_dists[i] - d1_min_dist) / d1_dif_dist

    d2_edge_dists_norm = numpy.ones(d2_edge_dists.shape)
    for i in range(d2_edge_dists.shape[0]):
        d2_edge_dists_norm[i] = (d2_edge_dists[i] - d2_min_dist) / d2_dif_dist
    
    numpy.save('./rawds/ges_imi.d1.edge_attr.npy', d1_edge_dists_norm)
    numpy.save('./rawds/ges_imi.d2.edge_attr.npy', d2_edge_dists_norm)