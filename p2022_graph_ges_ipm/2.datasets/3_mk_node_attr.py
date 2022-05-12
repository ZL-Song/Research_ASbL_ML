# Make the numpy array for the node level features.
# Zilin Song, 19 Jan 2022
# 
import numpy

def mk_node_attr(node_chrgs):
    """Make node feature attributes"""
    node_labels  = numpy.load('./rawds/label_nodes.npy').tolist()
    
    all_path_features = []

    for ipath in range(npath):
        one_path_features = []

        for inode in range(len(node_chrgs[ipath])):
            chrg = node_chrgs[ipath][inode]
            node_features = []

            if   node_labels[inode].split('.')[-1][0] == 'H':
                node_features.extend([chrg, 0, 0, 0])
            
            elif node_labels[inode].split('.')[-1][0] == 'C':
                node_features.extend([0, chrg, 0, 0])
            
            elif node_labels[inode].split('.')[-1][0] == 'N':
                node_features.extend([0, 0, chrg, 0])
            
            elif node_labels[inode].split('.')[-1][0] == 'O':
                node_features.extend([0, 0, 0, chrg])

            one_path_features.append(node_features)

        all_path_features.append(one_path_features)

    return all_path_features

if __name__ == '__main__':
    
    d1_node_chrgs = numpy.load('./rawds/ges_imi.d1.node_nbo.npy').tolist()
    d2_node_chrgs = numpy.load('./rawds/ges_imi.d2.node_nbo.npy').tolist()

    npath = 500

    d1_ds = numpy.asarray(mk_node_attr(d1_node_chrgs))
    d2_ds = numpy.asarray(mk_node_attr(d2_node_chrgs))

    print(d1_ds.shape)
    print(d2_ds.shape)

    numpy.save('./rawds/ges_imi.d1.node_attr.npy', d1_ds)
    numpy.save('./rawds/ges_imi.d2.node_attr.npy', d2_ds)