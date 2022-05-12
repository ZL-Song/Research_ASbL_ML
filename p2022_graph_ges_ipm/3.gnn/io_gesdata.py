# Create graph dataset.
# Zilin Song, 19 Jan 2022
#

import numpy

# ---------------------------------------------------------------------------------

def random_split():
    """Generate data indices for training/validation splits."""

    rng = numpy.random.default_rng()

    idx_all   = numpy.arange(500)

    idx_train = rng.choice(idx_all, size=425, replace=False)
    idx_other = numpy.delete(idx_all, idx_train)

    i_valid   = rng.choice(numpy.arange(75), size=75, replace=False)
    idx_valid = numpy.take(idx_other, i_valid)

    print("\n", r"  Training entries:", "\n", idx_train)
    print("\n", r"Validation entries:", "\n", idx_valid)
    print(numpy.intersect1d(idx_train, idx_valid))
    print("\n=========")
    return idx_train, idx_valid

def make_split():
    """Make and save the indices for data splits."""

    d1_train, d1_valid = random_split()
    d2_train, d2_valid = random_split()

    numpy.save("./data_split/idx_d1_train.npy", d1_train)
    numpy.save("./data_split/idx_d1_valid.npy", d1_valid)
    numpy.save("./data_split/idx_d2_train.npy", d2_train)
    numpy.save("./data_split/idx_d2_valid.npy", d2_valid)

# ---------------------------------------------------------------------------------

import torch
from torch_geometric.data import Data

def make_gesdata():
    r"""Prepare the GES/IMI data for graph representation."""
    _basedir    = f"/users/zilins/scratch/6.proj_ges_imi/2.datasets/rawds"

    # ---
    # Node attr.
    _d1_node_chrg_dir = f"{_basedir}/ges_imi.d1.node_attr.npy"
    _d2_node_chrg_dir = f"{_basedir}/ges_imi.d2.node_attr.npy"
    _nodelabeldir     = f"{_basedir}/label_nodes.npy"

    d1_node_attr = numpy.load(_d1_node_chrg_dir)[:, :-2, :] # Remove node S70-Hg, IMI-N4
    d2_node_attr = numpy.load(_d2_node_chrg_dir)
    node_attr_label = numpy.load(_nodelabeldir)
    # print(d1_node_attr[0])
    # print(node_chrg_label)

    # ---
    # Edge attr.
    _d1_edge_attr_dir = f"{_basedir}/ges_imi.d1.edge_attr.npy"
    _d2_edge_attr_dir = f"{_basedir}/ges_imi.d2.edge_attr.npy"
    _edgelabeldir = f"{_basedir}/label_edges.npy"
    d1_edge_attr = numpy.load(_d1_edge_attr_dir)[:, :-6] # Remove edges concerning S70-Hg, IMI-N4
    d2_edge_attr = numpy.load(_d2_edge_attr_dir)
    edge_attr_label = numpy.load(_edgelabeldir)
    # print(d1_edge_attr.shape)
    # print(edge_attr_label)

    # ---
    # Edge connectivities.
    _edge_index_dir = f"{_basedir}/indices_edges.npy"
    d1_edge_index = numpy.load(_edge_index_dir)[:, :-6] # Remove edges concerning S70-Hg, IMI-N4
    d2_edge_index = numpy.load(_edge_index_dir)
    # print(d1_edge_index)
    # print(d2_edge_index)

    # ---
    # Pathway barriers.
    _d1_barrier_dir = f"{_basedir}/ges_imi.d1.barrier.npy"
    _d2_barrier_dir = f"{_basedir}/ges_imi.d2.barrier.npy"
    d1_barrier = numpy.load(_d1_barrier_dir)
    d2_barrier = numpy.load(_d2_barrier_dir)
    # print(barrier.shape)
    # print(d1_barrier.shape)

    # ---
    # Extend dimension if there are only one feature present.
    d1_node_attr = numpy.expand_dims(d1_node_attr, axis=2) if d1_node_attr.ndim == 2 else d1_node_attr
    d1_edge_attr = numpy.expand_dims(d1_edge_attr, axis=2) if d1_edge_attr.ndim == 2 else d1_edge_attr
    d1_barrier   = numpy.expand_dims(d1_barrier,   axis=1) if   d1_barrier.ndim == 1 else d1_barrier
    d2_node_attr = numpy.expand_dims(d2_node_attr, axis=2) if d2_node_attr.ndim == 2 else d2_node_attr
    d2_edge_attr = numpy.expand_dims(d2_edge_attr, axis=2) if d2_edge_attr.ndim == 2 else d2_edge_attr
    d2_barrier   = numpy.expand_dims(d2_barrier,   axis=1) if   d2_barrier.ndim == 1 else d2_barrier

    # print(d1_edge_attr.shape)
    # print(d1_edge_attr.shape)

    # ---
    # unify data type to numpy.float32 so that pytorch will not complain upon tensor conversion
    d1_node_attr = d1_node_attr.astype(numpy.float32)
    d1_edge_attr = d1_edge_attr.astype(numpy.float32)
    d1_barrier   =   d1_barrier.astype(numpy.float32)
    d2_node_attr = d2_node_attr.astype(numpy.float32)
    d2_edge_attr = d2_edge_attr.astype(numpy.float32)
    d2_barrier   =   d2_barrier.astype(numpy.float32)

    # print(f"d1_node_attr.shape = {d1_node_attr.shape}")
    # print(f"d1_edge_attr.shape = {d1_edge_attr.shape}")
    # print(f"d1_barrier.shape   = {d1_barrier.shape}")
    # print(f"d2_node_attr.shape = {d2_node_attr.shape}")
    # print(f"d2_edge_attr.shape = {d2_edge_attr.shape}")
    # print(f"d2_barrier.shape   = {d2_barrier.shape}")

    # for i in range(node_attr_label.shape[0]):
    #     print(node_attr_label[i])
    
    # print(node_attr_label)
    # print(edge_attr_label)

    # ---
    # Create list of graph data.
    d1_data_list = []

    for i in range(500):  # Add all d1 data.
        d = Data(x         =torch.from_numpy(d1_node_attr[i]),
                 edge_index=torch.from_numpy(d1_edge_index),
                 edge_attr =torch.from_numpy(d1_edge_attr[i]),
                 y         =torch.from_numpy(d1_barrier[i])
        )
        d1_data_list.append(d)

    d2_data_list = []

    for i in range(500):  # Add all d2 data.
        d = Data(x         =torch.from_numpy(d2_node_attr[i]),
                 edge_index=torch.from_numpy(d2_edge_index),
                 edge_attr =torch.from_numpy(d2_edge_attr[i]),
                 y         =torch.from_numpy(d2_barrier[i])
        )
        d2_data_list.append(d)

    return d1_data_list, d2_data_list

def load_ges_data(split=True):
    """Load and return the splitted data."""
    idx_d1_train = numpy.load("./data_split/idx_d1_train.npy").tolist()
    idx_d1_valid = numpy.load("./data_split/idx_d1_valid.npy").tolist()
    idx_d2_train = numpy.load("./data_split/idx_d2_train.npy").tolist()
    idx_d2_valid = numpy.load("./data_split/idx_d2_valid.npy").tolist()

    d1, d2 = make_gesdata()

    if split == True:

        train = []
        valid = []

        for id in idx_d1_train:
            train.append(d1[id])

        for id in idx_d2_train:
            train.append(d2[id])

        for id in idx_d1_valid:
            valid.append(d1[id])
        
        for id in idx_d2_valid:
            valid.append(d2[id])
            
        return train, valid
    
    else:
        
        return d1, d2
    

if __name__ == '__main__':
    make_gesdata()
