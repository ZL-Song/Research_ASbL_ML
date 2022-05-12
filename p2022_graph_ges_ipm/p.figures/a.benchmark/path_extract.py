import MDAnalysis as mda

def get_path(sysname, theoryname):
    '''Get psf and cor.
    theoryname: b3lyp,3ob,3ob_f
    '''
    psf = f"../../6.benchmark/{theoryname}/ges_imi.{sysname}_f22.psf"
    cor = f"../../6.benchmark/{theoryname}/ges_imi.{sysname}_f22.cor"
    return mda.Universe(psf, cor, topology_format='PSF', format='CRD')

def dist_rx(mda_universe, repid):
    '''Compute and return all reaction coordinates.
    These selections have to be hard-coded, one way or the other.

    dx:  sel_atom_i    sel_atom_j
    d0:  Glu166-OE1  =    WAT-H1
    d1:    WAT-H1    =    WAT-OH2
    d2:    WAT-OH2   =    IPM-C7
    d3:    IPM-C7    =   Ser70-OG
    d4:   Ser70-OG   =   Lys73-HZ1
    d5:   Lys73-NZ   =   Lys73-HZ1
    '''
    _selbase = 'segid Q{0} and'.format(str(repid))
    atom_i_sel = [
        ' (resid 161 and resname  GLU and name OE1)',	# d0
        ' (resid 287 and resname TIP3 and name  H1)',	# d1
        ' (resid 287 and resname TIP3 and name OH2)',	# d2
        ' (resid 286 and resname  IMI and name  C7)',	# d3
        ' (resid  64 and resname  SER and name  OG)',	# d4
        ' (resid  67 and resname  LYS and name  NZ)',	# d5
    ]
    atom_j_sel = [
        ' (resid 287 and resname TIP3 and name  H1)',	# d0
        ' (resid 287 and resname TIP3 and name OH2)',	# d1
        ' (resid 286 and resname  IMI and name  C7)',	# d2
        ' (resid  64 and resname  SER and name  OG)',	# d3
        ' (resid  67 and resname  LYS and name HZ1)',	# d4
        ' (resid  67 and resname  LYS and name HZ1)',	# d5
    ]
    _distmat = []
    _distlbl = []
    for i in range(len(atom_i_sel)):
        group0 = mda_universe.select_atoms(_selbase + atom_i_sel[i])
        group1 = mda_universe.select_atoms(_selbase + atom_j_sel[i])

        if group0.n_atoms == 1 and group1.n_atoms == 1:
            atom_i = group0.atoms[0]
            atom_j = group1.atoms[0]
            d = interatomic_dist(atom_i, atom_j, )
            l =	'{0}.{1}.{2}:{3}.{4}.{5}'.format(
                atom_i.residue.resname, atom_i.residue.resid, atom_i.name,
                atom_j.residue.resname, atom_j.residue.resid, atom_j.name,
            )
            _distmat.append(d)
            _distlbl.append(l)
        else: 
            print(i, group0.n_atoms, group1.n_atoms)
            raise ValueError('Pairwise selection retrived more than 1 atoms in each group: Check dist_compute.dist_rx()\n')
            
    return _distmat, _distlbl

def interatomic_dist(atom_i, atom_j, ):
    '''Compute the interatomic distance between 2 atoms.
    '''
    return	round(
        ((atom_i.position[0] - atom_j.position[0])**2 + \
         (atom_i.position[1] - atom_j.position[1])**2 + \
         (atom_i.position[2] - atom_j.position[2])**2   \
        ) ** 0.5, 8)

def extract_rxc(mda_universe, nrep=36, ):
    '''Extract all reaction coordinates in one RPM coordinate of nrep replicas..
    '''
    path_rxc_distmat    = []
    path_rxc_labelmat   = []

    for repid in range(1, nrep+1):
        print(repid)
        path_rxc_distrow, path_rxc_labelrow = dist_rx(mda_universe, repid)
        path_rxc_distmat.append(path_rxc_distrow)
        path_rxc_labelmat.append(path_rxc_labelrow)
    
    return path_rxc_distmat, path_rxc_labelmat


import numpy

for sysname in ['d1', 'd2']:
    for theoryname in ['b3lyp', '3ob', '3ob_f']:
        u = get_path(sysname, theoryname)
        distmat, lblmat = extract_rxc(u)
        numpy.save(f'./dist_npy/{sysname}.{theoryname}.dist.npy', distmat)
        numpy.save(f'./dist_npy/{sysname}.{theoryname}.label.npy', lblmat[0])