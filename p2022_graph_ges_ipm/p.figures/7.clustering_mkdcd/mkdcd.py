# Divide the dcd structures by clusters.
# Need to create dirs: 'aligned', 'pdb', 'rmsd', 'unaligned', 'ener_repr' before using.
# Zilin Song, 11 Feb 2022
# 

import MDAnalysis as mda
import MDAnalysis.analysis.align
import numpy

def write_traj(sysname, cluster_label):
    """Write the trajectories within one cluster."""
    # ==== Directories.
    _sys_idx = 0 if sysname == 'd2' else 1
    _basedir = "/users/zilins/scratch/6.proj_ges_imi/1.sampling"
    _psfdir = f"{_basedir}/{_sys_idx}.ges_imi.{sysname}/2.mkref/ges_imi.{sysname}.ref.psf"
    _dcddir = f"{_basedir}/{_sys_idx}.ges_imi.{sysname}/5.acylenzyme_valid/ges_imi.{sysname}_ae_validmini.dcd"

    # ==== Get the indices of snapshots in one cluster.
    cl = numpy.load(f"../6.clustering/cluster_{cluster_label}.npy")
    cl = cl[cl<500] if sysname=='d1' else cl[cl>=500]-500

    # ==== output unaligned dcd file.
    mda_u = mda.Universe(_psfdir, _dcddir, topology_format='PSF', format='DCD')
    prot_imi_sele = mda_u.select_atoms("(protein or (resname TIP3 and resid 287 and segid A) or resname IMI) and not name QQH")

    with mda.Writer(f"./unaligned/{sysname}.cluster_{cluster_label}_unaligned.dcd", n_atoms=prot_imi_sele.n_atoms) as w_dcd:
        print(f"Outputing... unaligned.dcd sysname {sysname} cluster {cluster_label}", flush=True)

        for ts in cl:
            mda_u.trajectory[ts]
            w_dcd.write(prot_imi_sele)

    # ==== output cluster_center pdb file.
    ref_u = mda.Universe(_psfdir, _dcddir, topology_format='PSF', format='DCD')
    ref_prot_imi_sele = ref_u.select_atoms("(protein or (resname TIP3 and resid 287 and segid A) or resname IMI) and not name QQH")
    
    ref_frame = 284 if sysname=='d1' and cluster_label==0 else \
                674 if sysname=='d2' and cluster_label==0 else \
                 55 if sysname=='d1' and cluster_label==1 else \
                756 if sysname=='d2' and cluster_label==1 else \
                 12 if sysname=='d1' and cluster_label==2 else \
                512 if sysname=='d2' and cluster_label==2 else \
                453 if sysname=='d1' and cluster_label==3 else \
                809 if sysname=='d2' and cluster_label==3 else \
                None
    ref_frame = ref_frame-500 if sysname=='d2' else ref_frame

    with mda.Writer(f"./pdb/{sysname}.ref_{cluster_label}.pdb", n_atoms=prot_imi_sele.n_atoms) as w_pdb:
        print(f"Outputing... pdb           sysname {sysname} cluster {cluster_label}", flush=True)
        ref_u.trajectory[ref_frame]
        w_pdb.write(ref_prot_imi_sele)

    # ==== output energy_repr pdb file.
    with mda.Writer(f"./ener_repr/{sysname}.ener.pdb", n_atoms=prot_imi_sele.n_atoms) as w_pdb:
        print(f"Outputing... pdb           sysname {sysname} ener", flush=True)
        ener_frame = 22 if sysname=='d1' else 464 # if sysname=='d2'
        ref_u.trajectory[ener_frame]
        w_pdb.write(ref_prot_imi_sele)

    # ==== reload universe for making aligned structures.
    mda_u=mda.Universe(f"./pdb/{sysname}.ref_{cluster_label}.pdb", f"./unaligned/{sysname}.cluster_{cluster_label}_unaligned.dcd")
    ref_u=mda.Universe(f"./pdb/{sysname}.ref_{cluster_label}.pdb")

    core_imi_sele = f" segid A and ("                                                             \
                    f"     (resid  64 and (name   OG                                      )) "    \
                    f"  or (resid  67 and (name   NZ                                      )) "    \
                    f"  or (resid 127 and (name  OD1 or name  ND2                         )) "    \
                    f"  or (resid 161 and (name  OE1 or name  OE2                         )) "    \
                    f"  or (resid 165 and (name   OG                                      )) "    \
                    f"  or (resid 286 and (name   C7 or name   O7 or name  O15 or name  N4)) "    \
                    f"  or (resid 287 and (name  OH2                                      )) "    \
                    f" ) "

    # ==== output aligned pdb file and rmsd array to reference.
    align = MDAnalysis.analysis.align.AlignTraj(mda_u, ref_u, select={'mobile':core_imi_sele, 'reference':core_imi_sele}, 
                                                filename=f"./aligned/{sysname}.cluster_{cluster_label}.dcd", verbose=True)
    align.run()
    
    
    print("reference frame idx:", cl[numpy.argmin(align.rmsd)], "aligned dcd index:", numpy.argmin(align.rmsd), "aver. rmsd", numpy.average(align.rmsd))
    numpy.save(f"./rmsd/{sysname}.cluster_{cluster_label}.rmsd.npy", align.rmsd)

if __name__ == '__main__':

    for sysname in ['d1', 'd2']:
    
        for cl in range(4):
    
            write_traj(sysname, cl)
    
