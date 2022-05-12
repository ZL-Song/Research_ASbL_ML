# Extract hydrogen bonds from pathway geometries. 
# Hydrogen bonds are noted by donor/acceptor distances. 
# Zilin Song, 06 Dec 2021
# 

import iomisc, selection, numpy, multiprocessing
from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis as HBA

def _is_hbond(donor, hydrogen, acceptor):
    """Check if Hydrogen bonded using the default mdanalysis.HBA metric."""
    dh_dist   = selection.dist(donor, hydrogen)
    da_dist   = selection.dist(donor, acceptor)
    dha_angle = selection.angle(donor, hydrogen, acceptor)
    if dh_dist <= 1.2 and da_dist <= 3.0 and dha_angle >= 110:
        if dha_angle >= 150:
            print(f"####Found dha_angle >150 match: {donor} - {acceptor}")
        return True
    else:
        return False

def find_hbonds(mda_universe, repid):
    """Find all possible hydrogen bonded HEAVY atom pairs.
    Note for HBA.results:
    hba.hbonds=[    
        [<frame>, <donor index (0-based)>, 
        <hydrogen index (0-based)>,
        <acceptor index (0-based)>,
        <distance>, <angle>], [...]
    ]"""
    heavy_atoms    = selection.select_heavy_atoms(mda_universe, repid, return_selstr=True)
    hydrogen_atoms = selection.select_hydrogen_atoms(mda_universe, repid, return_selstr=True)

    # Note, hydrogen had to bond to donor, a QM donor would ensure a QM hydrogen.
    hba = HBA(universe=mda_universe, 
              donors_sel=heavy_atoms,
              hydrogens_sel=hydrogen_atoms,
              acceptors_sel=heavy_atoms, 
              d_h_a_angle_cutoff=110
              )
    hba.run()
    hlabels=[]

    for hb in hba.hbonds:
        donor = mda_universe.atoms[int(hb[1])]
        hydro = mda_universe.atoms[int(hb[2])]
        accep = mda_universe.atoms[int(hb[3])]

        # exclude intra-residue hydrogen bond
        if (donor.residue.resname == accep.residue.resname and \
            donor.residue.resid   == accep.residue.resid): 
            continue
        
        # carbon is never a donor/acceptor in CHARMM topology.
        if donor.name[0] == 'C' or accep.name[0] == 'C': 
            continue

        # donor-acceptor label: H must be bonded topologically to donor so there are no overcounting.
        dh_l = f"{donor.residue.resname}.{donor.residue.resid}.{donor.name}:" \
               f"{hydro.residue.resname}.{hydro.residue.resid}.{hydro.name}"
        hlabels.append(dh_l)

        ah_l = f"{accep.residue.resname}.{accep.residue.resid}.{accep.name}:" \
               f"{hydro.residue.resname}.{hydro.residue.resid}.{hydro.name}"
        hlabels.append(ah_l)
    
    # Fix possible Hbonds concerning IMI-N4-H -- accep
    imi_n4  = mda_universe.select_atoms(f"segid Q{repid} and resname IMI and resid 286 and name  N4")
    s70_hg1 = mda_universe.select_atoms(f"segid Q{repid} and resname SER and resid  64 and name HG1")
    if s70_hg1.n_atoms != 1 or imi_n4.n_atoms != 1: raise ValueError(f"Bad selection on IMI N-H atoms")
    
    donor = imi_n4[0]
    hydro = s70_hg1[0]
    candid_acceptors = mda_universe.select_atoms(
        f"(around 3.0 (segid Q{repid} and resname IMI and resid 286 and name  N4)) and (group qmhvy)",
        qmhvy=selection.select_heavy_atoms(mda_universe, repid)
    )
    for accep in candid_acceptors:
        if _is_hbond(donor, hydro, accep) == True:
            dh_l = f"{donor.residue.resname}.{donor.residue.resid}.{donor.name}:" \
                   f"{hydro.residue.resname}.{hydro.residue.resid}.{hydro.name}"

            ah_l = f"{accep.residue.resname}.{accep.residue.resid}.{accep.name}:" \
                   f"{hydro.residue.resname}.{hydro.residue.resid}.{hydro.name}"

            if not (dh_l in hlabels): hlabels.append(dh_l)
            if not (ah_l in hlabels): hlabels.append(ah_l)

    return hlabels

def find_all(sysname, npath=500, nrep=1):
    """Find all hydrogen bonds."""
    hlabel_mat = []

    for ipath in range(1, npath+1):
        u = iomisc.loadpath(sysname, ipath)

        for irep in range(1, nrep+1):
    
            print(f"Extracting: ges_imi.{sysname}.path{ipath}.rep{irep}...", flush=True)
            hlabel_row = find_hbonds(u, irep)
            hlabel_mat.append(hlabel_row)

    return hlabel_mat

if __name__ == '__main__':
    with multiprocessing.Pool(processes=2) as pool:
        
        # Async multiprocessing.
        d1res = pool.apply_async(find_all, args=['d1'])
        d2res = pool.apply_async(find_all, args=['d2'])
        
        d1_hlabel_mat = d1res.get()
        d2_hlabel_mat = d2res.get()

    # Merge all selections. 
    unified_hlabels = []
    for hlabel_mat in [d1_hlabel_mat, d2_hlabel_mat]:

        for hlabel_row in hlabel_mat:

            for hlabel in hlabel_row:

                if not hlabel in unified_hlabels:
                    unified_hlabels.append(hlabel)
    
    unified_hlabels = numpy.asarray(unified_hlabels)
    
    print(unified_hlabels)
    print(unified_hlabels.shape)

    numpy.save(f"./rawds/label_hbonds.npy", unified_hlabels)
