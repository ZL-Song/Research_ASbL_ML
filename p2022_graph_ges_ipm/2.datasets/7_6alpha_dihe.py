# Extract chemcial distance array from pathway geometries. 
# Zilin Song, 05 Dec 2021
# 

import selection, iomisc, numpy, multiprocessing, sys

def extract_one_replica(mda_universe, repid):
    """Extract the interatomic distances between the specified bonding pairs."""
    
    atom_C7C6C6aO6a  = mda_universe.select_atoms(f"(segid Q{repid} and resname IMI and resid 286 and name  C7)") + \
                       mda_universe.select_atoms(f"(segid Q{repid} and resname IMI and resid 286 and name  C6)") + \
                       mda_universe.select_atoms(f"(segid Q{repid} and resname IMI and resid 286 and name C15)") + \
                       mda_universe.select_atoms(f"(segid Q{repid} and resname IMI and resid 286 and name O15)")
    assert atom_C7C6C6aO6a.n_atoms==4

    dihe = selection.dihedral(atom_C7C6C6aO6a)

    return dihe

def extract_all(sysname, npath=500, nrep=1):

    dihe_mat = []

    for ipath in range(1, npath+1):
        u = iomisc.loadpath(sysname, ipath)

        for irep in range(1, nrep+1):
            print(f"Extracting: ges_imi.{sysname}.path{ipath}.rep{irep}...", flush=True)
            dist_row = extract_one_replica(u, irep)
            dihe_mat.append(dist_row)
    
    return dihe_mat


if __name__ == '__main__':
    
    with multiprocessing.Pool(processes=2) as pool:
        # Async multiprocessing.
        d1res = pool.apply_async(extract_all, args=['d1'])
        d2res = pool.apply_async(extract_all, args=['d2'])
        
        d1_dihe_mat = d1res.get()
        d2_dihe_mat = d2res.get()

    print(numpy.asarray(d1_dihe_mat).shape)
    print(numpy.asarray(d2_dihe_mat).shape)
    
    numpy.save(f"./rawds/ges_imi.d1.ccco_dihe.npy", d1_dihe_mat)
    numpy.save(f"./rawds/ges_imi.d2.ccco_dihe.npy", d2_dihe_mat)
