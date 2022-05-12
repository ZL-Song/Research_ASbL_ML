# Extract interatomic distances from pathway geometries as NumPy arrays. 
# Zilin Song, 05 Dec 2021
# 

import iomisc, numpy, multiprocessing

def extract_one_replica(mda_universe, repid):
    """Extract the interatomic distances between the specified bonding pairs."""
    
    dat_row = []
    

    atom_n4 = mda_universe.select_atoms(f"segid Q{repid} and resname IMI " \
                                       f"                and   resid 286 " \
                                       f"                and    name  N4 " )
    atom_h4 = mda_universe.select_atoms(f"segid Q{repid} and resname SER " \
                                       f"                and   resid  64 " \
                                       f"                and    name HG1 " )
    atom_o7 = mda_universe.select_atoms(f"segid Q{repid} and resname IMI " \
                                       f"                and   resid 286 " \
                                       f"                and    name  O7 " )
    atom_og = mda_universe.select_atoms(f"segid Q{repid} and resname SER " \
                                       f"                and   resid  64 " \
                                       f"                and    name  OG " )

    # Sanity check.
    assert atom_n4.n_atoms==1
    assert atom_h4.n_atoms==1
    assert atom_o7.n_atoms==1
    assert atom_og.n_atoms==1

    coor_n4 = atom_n4.center_of_geometry()
    coor_h4 = atom_h4.center_of_geometry()
    coor_o7 = atom_o7.center_of_geometry()
    coor_og = atom_og.center_of_geometry()

    n4h4 = coor_n4 - coor_h4
    o7h4 = coor_o7 - coor_h4
    ogh4 = coor_og - coor_h4
    
    # calc acceptor...H dist
    # print(n4h4, coor_n4, coor_h4)
    dist_o7h4 = numpy.linalg.norm(o7h4)
    dist_ogh4 = numpy.linalg.norm(ogh4)

    # calc donor-H...accopter angle
    angl_n4h4o7 = numpy.rad2deg(numpy.arccos(numpy.dot(n4h4, o7h4)/(numpy.linalg.norm(n4h4)*numpy.linalg.norm(o7h4))))
    angl_n4h4og = numpy.rad2deg(numpy.arccos(numpy.dot(n4h4, ogh4)/(numpy.linalg.norm(n4h4)*numpy.linalg.norm(ogh4))))

    dat_row = [dist_o7h4, dist_ogh4, angl_n4h4o7, angl_n4h4og]
    print(dat_row)
    return dat_row

def extract_all(sysname, npath=500, nrep=36):
    """Extract all chemical bonds on all replicas."""

    dat_mat = []


    for ipath in range(1, npath+1):
        u = iomisc.loadpath(sysname, ipath)
        dat_path = []
        for irep in range(1, nrep+1):
            print(f"Extracting: ges_imi.{sysname}.path{ipath}.rep{irep}...", flush=True)
            dat_row = extract_one_replica(u, irep)
            dat_path.append(dat_row)
        
        dat_mat.append(dat_path)
    
    return dat_mat

if __name__ == '__main__':
    dat_mat = extract_all('d2')
    numpy.save("d2_n4_hbonds.npy", dat_mat)