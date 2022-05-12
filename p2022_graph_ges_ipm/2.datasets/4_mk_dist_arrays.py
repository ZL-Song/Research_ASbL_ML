# Extract interatomic distances from pathway geometries as NumPy arrays. 
# Zilin Song, 05 Dec 2021
# 

import selection, iomisc, numpy, multiprocessing, sys

def extract_one_replica(mda_universe, repid, bondlabel_list):
    """Extract the interatomic distances between the specified bonding pairs."""
    
    dist_row = []

    for bondlabel in bondlabel_list:
        atomlabel_i = bondlabel.split(':')[0]
        atomlabel_j = bondlabel.split(':')[1]

        atom_i = mda_universe.select_atoms(f"segid Q{repid} and resname {atomlabel_i.split('.')[0]} " \
                                           f"               and   resid {atomlabel_i.split('.')[1]} " \
                                           f"               and    name {atomlabel_i.split('.')[2]} " )
        atom_j = mda_universe.select_atoms(f"segid Q{repid} and resname {atomlabel_j.split('.')[0]} " \
                                           f"               and   resid {atomlabel_j.split('.')[1]} " \
                                           f"               and    name {atomlabel_j.split('.')[2]} " )

        # Sanity check. 
        if atom_i.n_atoms != 1 or atom_j.n_atoms != 1: raise ValueError(f"Bad selection on reactive bonds: {bondlabel}")

        # d = selection.invert_dist(atom_i[0], atom_j[0])
        # d = selection.invariant_dist(atom_i[0], atom_j[0])
        d = selection.dist(atom_i[0], atom_j[0])
        
        dist_row.append(d)

    return dist_row

def extract_all(sysname, label_array, npath=500, nrep=1):
    """Extract all chemical bonds on all replicas."""
    bondlabel_list = numpy.load(f"{label_array}")

    dist_mat = []

    for ipath in range(1, npath+1):
        u = iomisc.loadpath(sysname, ipath)

        for irep in range(1, nrep+1):
            print(f"Extracting: ges_imi.{sysname}.path{ipath}.rep{irep}...", flush=True)
            dist_row = extract_one_replica(u, irep, bondlabel_list)
            dist_mat.append(dist_row)
    
    return dist_mat

if __name__ == '__main__':
    label_array = "./rawds/label_edges.npy"
    
    with multiprocessing.Pool(processes=2) as pool:
        # Async multiprocessing.
        d1res = pool.apply_async(extract_all, args=['d1', label_array])
        d2res = pool.apply_async(extract_all, args=['d2', label_array])
        
        d1_dist_mat = d1res.get()
        d2_dist_mat = d2res.get()

    print(numpy.asarray(d1_dist_mat).shape)
    print(numpy.asarray(d2_dist_mat).shape)
    
    numpy.save(f"./rawds/ges_imi.d1.edge_dist.npy", d1_dist_mat)
    numpy.save(f"./rawds/ges_imi.d2.edge_dist.npy", d2_dist_mat)
