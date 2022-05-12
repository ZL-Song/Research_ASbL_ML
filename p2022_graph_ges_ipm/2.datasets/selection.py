# Helper functions to select different set of atoms. 
# Zilin Song, 04 Dec 2021
# 
import numpy

from MDAnalysis.analysis.dihedrals import Dihedral

def dihedral(atom_C7C6C6aO6a):
    """Compute the interatomic distance between 2 atoms."""
    dihe = Dihedral([atom_C7C6C6aO6a]).run().angles
    return dihe

def dist(atom_i, atom_j):
    """Compute the interatomic distance between 2 atoms."""
    d = 0
    for k in range(3):
        d += ((atom_i.position[k] - atom_j.position[k]) ** 2)
    return round(d**0.5, 8)

def invert_dist(atom_i, atom_j):
    """Compute the interatomic distance between 2 atoms."""
    d = 0
    for k in range(3):
        d += ((atom_i.position[k] - atom_j.position[k]) ** 2)
    return 1./round(d**0.5, 8)

def invariant_dist(atom_i, atom_j):
    """Compute the invariant dist."""
    dx = atom_i.position[0] - atom_j.position[0]
    dy = atom_i.position[1] - atom_j.position[1]
    dz = atom_i.position[2] - atom_j.position[2]
    d  = (dx**2 + dy**2 + dz**2)**0.5

    return [1./round(d, 8), dx/round(d, 8), dy/round(d, 8), dz/round(d, 8)]

def angle(donor, hydrogen, acceptor):
    """Compute the D-H-A angle."""
    d = numpy.array([donor.position[0],     donor.position[1],      donor.position[2]])
    h = numpy.array([hydrogen.position[0],  hydrogen.position[1],   hydrogen.position[2]])
    a = numpy.array([acceptor.position[0],  acceptor.position[1],   acceptor.position[2]])

    hd = d - h
    ha = a - h

    cosine_angle = numpy.dot(hd, ha) / (numpy.linalg.norm(hd) * numpy.linalg.norm(ha))
    angle = numpy.arccos(cosine_angle)
    return numpy.abs(numpy.degrees(angle))

def select_heavy_atoms(mda_universe, repid, return_selstr=False):
    """Select all QM heavy atoms in one replica.  
     A        64       SER CB OG      
     A        67       LYS CB CG CD CE NZ      
     A        125      SER CB OG      
     A        127      ASN CB CG OD1 ND2     
     A        161      GLU CB CG CD OE1 OE2     
     A        165      SER CB OG      
     A        286      IMI C1 C2 C3 N4 C5 C6 C7 O7 S8 C9 C10 N11 C12 N13 C14 O14A O14B C15 O15 C16     
     A        287      TIP3 OH2 
    """
    selcmd = f" segid Q{repid} and ("                                                                   \
             f"     (resid  64 and (name   CB or name   OG                                        )) "  \
             f"  or (resid  67 and (name   CB or name   CG or name   CD or name   CE or name   NZ )) "  \
             f"  or (resid 125 and (name   CB or name   OG                                        )) "  \
             f"  or (resid 127 and (name   CB or name   CG or name  OD1 or name  ND2              )) "  \
             f"  or (resid 161 and (name   CB or name   CG or name   CD or name  OE1 or name  OE2 )) "  \
             f"  or (resid 165 and (name   CB or name   OG                                        )) "  \
             f"  or (resid 287 and (name  OH2                                                     )) "  \
             f"  or (resid 286 and (name   C1 or name   C2 or name   C3 or name   N4 or name   C5 or "  \
             f"                     name   C6 or name   C7 or name   O7 or name   S8 or name   C9 or "  \
             f"                     name  C10 or name  N11 or name  C12 or name  N13 or name  C14 or "  \
             f"                     name O14A or name O14B or name  C15 or name  O15 or name  C16 )) "  \
             f" ) "

    if return_selstr:
        return selcmd
    else:
        qmhvy = mda_universe.select_atoms(selcmd)
        if qmhvy.n_residues != 8 or qmhvy.n_atoms != 41:
            print([i for i in qmhvy.atoms])
            raise ValueError(f"qmhvy selected {qmhvy.n_residues}/{qmhvy.n_atoms} residues/atoms, should be 8/41.")
        else:
            return qmhvy

def select_hydrogen_atoms(mda_universe, repid, return_selstr=False):
    """Select all QM hydrogen atoms in one replica."""
    selcmd = f"segid Q{repid} and name H* and ( "  \
             f"    (resid  64 and resname  SER) "  \
             f" or (resid  67 and resname  LYS) "  \
             f" or (resid 125 and resname  SER) "  \
             f" or (resid 127 and resname  ASN) "  \
             f" or (resid 161 and resname  GLU) "  \
             f" or (resid 165 and resname  SER) "  \
             f" or (resid 165 and resname  SER) "  \
             f" or (resid 287 and resname TIP3) "  \
             f" or (resid 286 and resname  IMI) "  \
             f" ) "
    if return_selstr:
        return selcmd
    else:
        qmhyd = mda_universe.select_atoms(selcmd)
        return qmhyd
    
def select_reacting_hydrogen_atoms(mda_universe, repid, return_selstr=False):
    """Select all reacting QM hydrogen atoms."""
    selcmd = f"segid Q{repid} and ("                           \
             f"    (resname  LYS and resid  67 and name HZ1) " \
             f" or (resname TIP3 and resid 287 and name  H1) " \
             f" or (resname TIP3 and resid 287 and name  H2) " \
             f" ) "
    if return_selstr:
        return selcmd
    else:
        qmrxhyd = mda_universe.select_atoms(selcmd)
        if qmrxhyd.n_residues != 2 or qmrxhyd.n_atoms != 3:
            print([i for i in qmrxhyd])
            raise ValueError(f"qmhvy selected {qmrxhyd.n_residues}/{qmrxhyd.n_atoms} residues/atoms, should be 2/3.")
        return qmrxhyd
