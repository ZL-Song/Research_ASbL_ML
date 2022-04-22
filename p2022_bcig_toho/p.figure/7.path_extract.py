import MDAnalysis as mda

def get_path(sysname, pathname, theoryname):
    '''Get psf and cor.'''

    if   sysname == 'toho_amp' and pathname == 'r1' and theoryname == 'b3lyp':
        psf = '../../1.sampling/2.toho_amp.ae/x.r1.benchmark/1.b3lyp.path_dftb.endpoint/path_opt/toho_amp.path_f1.psf'
        cor = '../../1.sampling/2.toho_amp.ae/x.r1.benchmark/1.b3lyp.path_dftb.endpoint/path_opt/toho_amp.path.opt.cor'
    elif sysname == 'toho_amp' and pathname == 'r2' and theoryname == 'b3lyp':
        psf = '../../1.sampling/2.toho_amp.ae/x.r2.benchmark/1.b3lyp.path_dftb.endpoint/path_opt/toho_amp.path_f1.psf'
        cor = '../../1.sampling/2.toho_amp.ae/x.r2.benchmark/1.b3lyp.path_dftb.endpoint/path_opt/toho_amp.path.opt.cor'
    elif sysname == 'toho_cex' and pathname == 'r1' and theoryname == 'b3lyp':
        psf = '../../1.sampling/5.toho_cex.ae/x.r1.benchmark/1.b3lyp.path_dftb.endpoint/path_opt/toho_cex.path_f97.psf'
        cor = '../../1.sampling/5.toho_cex.ae/x.r1.benchmark/1.b3lyp.path_dftb.endpoint/path_opt/toho_cex.path.opt.cor'
    elif sysname == 'toho_cex' and pathname == 'r2' and theoryname == 'b3lyp':
        psf = '../../1.sampling/5.toho_cex.ae/x.r2.benchmark/1.b3lyp.path_dftb.endpoint/path_opt/toho_cex.path_f42.psf'
        cor = '../../1.sampling/5.toho_cex.ae/x.r2.benchmark/1.b3lyp.path_dftb.endpoint/path_opt/toho_cex.path.opt.cor'

    elif sysname == 'toho_amp' and pathname == 'r1' and theoryname == '3obf':
        psf = '../../1.sampling/2.toho_amp.ae/8a.r1.dftb.paths/path_opt/toho_amp.path_f1.psf'
        cor = '../../1.sampling/2.toho_amp.ae/8a.r1.dftb.paths/path_opt/toho_amp.path_f1.cor'
    elif sysname == 'toho_amp' and pathname == 'r2' and theoryname == '3obf':
        psf = '../../1.sampling/2.toho_amp.ae/8b.r2.dftb.paths/path_opt/toho_amp.path_f1.psf'
        cor = '../../1.sampling/2.toho_amp.ae/8b.r2.dftb.paths/path_opt/toho_amp.path_f1.cor'
    elif sysname == 'toho_cex' and pathname == 'r1' and theoryname == '3obf':
        psf = '../../1.sampling/5.toho_cex.ae/8a.r1.dftb.paths/path_opt/toho_cex.path_f97.psf'
        cor = '../../1.sampling/5.toho_cex.ae/8a.r1.dftb.paths/path_opt/toho_cex.path_f97.cor'
    elif sysname == 'toho_cex' and pathname == 'r2' and theoryname == '3obf':
        psf = '../../1.sampling/5.toho_cex.ae/8b.r2.dftb.paths/path_opt/toho_cex.path_f42.psf'
        cor = '../../1.sampling/5.toho_cex.ae/8b.r2.dftb.paths/path_opt/toho_cex.path_f42.cor'

    elif sysname == 'toho_amp' and pathname == 'r1' and theoryname == 'dftb3':
        psf = '../../1.sampling/2.toho_amp.ae/x.r1.benchmark/2.dftb.3ob.path/path_opt/toho_amp.path_f1.psf'
        cor = '../../1.sampling/2.toho_amp.ae/x.r1.benchmark/2.dftb.3ob.path/path_opt/toho_amp.path_f1.cor'
    elif sysname == 'toho_amp' and pathname == 'r2' and theoryname == 'dftb3':
        psf = '../../1.sampling/2.toho_amp.ae/x.r2.benchmark/2.dftb.3ob.path/path_opt/toho_amp.path_f1.psf'
        cor = '../../1.sampling/2.toho_amp.ae/x.r2.benchmark/2.dftb.3ob.path/path_opt/toho_amp.path_f1.cor'
    elif sysname == 'toho_cex' and pathname == 'r1' and theoryname == 'dftb3':
        psf = '../../1.sampling/5.toho_cex.ae/x.r1.benchmark/2.dftb.3ob.path/path_opt/toho_cex.path_f97.psf'
        cor = '../../1.sampling/5.toho_cex.ae/x.r1.benchmark/2.dftb.3ob.path/path_opt/toho_cex.path_f97.cor'
    elif sysname == 'toho_cex' and pathname == 'r2' and theoryname == 'dftb3':
        psf = '../../1.sampling/5.toho_cex.ae/x.r2.benchmark/2.dftb.3ob.path/path_opt/toho_cex.path_f42.psf'
        cor = '../../1.sampling/5.toho_cex.ae/x.r2.benchmark/2.dftb.3ob.path/path_opt/toho_cex.path_f42.cor'

    elif sysname == 'toho_amp' and pathname == 'r1' and theoryname == 'b3lyp_pol':
        psf = '../../1.sampling/2.toho_amp.ae/x.r1.benchmark/0.b3lyp_pol.path_dftb.endpoint/path_opt/toho_amp.path_f1.psf'
        cor = '../../1.sampling/2.toho_amp.ae/x.r1.benchmark/0.b3lyp_pol.path_dftb.endpoint/path_opt/toho_amp.path.opt.cor'
    elif sysname == 'toho_amp' and pathname == 'r2' and theoryname == 'b3lyp_pol':
        psf = '../../1.sampling/2.toho_amp.ae/x.r2.benchmark/0.b3lyp_pol.path_dftb.endpoint/path_opt/toho_amp.path_f1.psf'
        cor = '../../1.sampling/2.toho_amp.ae/x.r2.benchmark/0.b3lyp_pol.path_dftb.endpoint/path_opt/toho_amp.path.opt.cor'
    elif sysname == 'toho_cex' and pathname == 'r1' and theoryname == 'b3lyp_pol':
        psf = '../../1.sampling/5.toho_cex.ae/x.r1.benchmark/0.b3lyp_pol.path_dftb.endpoint/path_opt/toho_cex.path_f97.psf'
        cor = '../../1.sampling/5.toho_cex.ae/x.r1.benchmark/0.b3lyp_pol.path_dftb.endpoint/path_opt/toho_cex.path.opt.cor'
    elif sysname == 'toho_cex' and pathname == 'r2' and theoryname == 'b3lyp_pol':
        psf = '../../1.sampling/5.toho_cex.ae/x.r2.benchmark/0.b3lyp_pol.path_dftb.endpoint/path_opt/toho_cex.path_f42.psf'
        cor = '../../1.sampling/5.toho_cex.ae/x.r2.benchmark/0.b3lyp_pol.path_dftb.endpoint/path_opt/toho_cex.path.opt.cor'

    elif sysname == 'toho_amp' and pathname == 'r1' and theoryname == 'b3lyp_pol_disp':
        psf = '../../1.sampling/2.toho_amp.ae/x.r1.benchmark/4.b3lyp_disp_pol.path_dftb.endpoint/path_opt/toho_amp.path_f1.psf'
        cor = '../../1.sampling/2.toho_amp.ae/x.r1.benchmark/4.b3lyp_disp_pol.path_dftb.endpoint/path_opt/toho_amp.path.opt.cor'
    elif sysname == 'toho_amp' and pathname == 'r2' and theoryname == 'b3lyp_pol_disp':
        psf = '../../1.sampling/2.toho_amp.ae/x.r2.benchmark/4.b3lyp_disp_pol.path_dftb.endpoint/path_opt/toho_amp.path_f1.psf'
        cor = '../../1.sampling/2.toho_amp.ae/x.r2.benchmark/4.b3lyp_disp_pol.path_dftb.endpoint/path_opt/toho_amp.path.opt.cor'
    elif sysname == 'toho_cex' and pathname == 'r1' and theoryname == 'b3lyp_pol_disp':
        psf = '../../1.sampling/5.toho_cex.ae/x.r1.benchmark/4.b3lyp_disp_pol.path_dftb.endpoint/path_opt/toho_cex.path_f97.psf'
        cor = '../../1.sampling/5.toho_cex.ae/x.r1.benchmark/4.b3lyp_disp_pol.path_dftb.endpoint/path_opt/toho_cex.path.opt.cor'
    elif sysname == 'toho_cex' and pathname == 'r2' and theoryname == 'b3lyp_pol_disp':
        psf = '../../1.sampling/5.toho_cex.ae/x.r2.benchmark/4.b3lyp_disp_pol.path_dftb.endpoint/path_opt/toho_cex.path_f42.psf'
        cor = '../../1.sampling/5.toho_cex.ae/x.r2.benchmark/4.b3lyp_disp_pol.path_dftb.endpoint/path_opt/toho_cex.path.opt.cor'
        
    return mda.Universe(psf, cor, topology_format='PSF', format='CRD', )

def dist_rx(mda_universe, repid, pathname, ):
    '''Compute and return all reaction coordinates.
    These selections have to be hard-coded, one way or the other.

    dx:  sel_atom_i    sel_atom_j
    d0:  Ser70-HG1  =  Ser70-OG
    d1:  Ser70-HG1  = Wat433-OH2
    d2:  Wat433-H2  = Wat433-OH2
    d3:  Wat433-H2  = Glu165-OE1
    d3a: Wat433-H2  = Glu165-OE2
    d4:  Lys73-HZ2  =  Ser70-OG
    d5:  Lys73-HZ2  =  Lys73-NZ
    d6:  Lys73-HZ1  =  Lys73-NZ
    d7:  Lys73-HZ1  = Ser130-OG
    d8:  Ser130-HG1 = Ser130-OG
    d9:  Ser130-HG1 = Lig285-N
    d10: Ser70-OG   = Lig285-C  -> this entry is included in the chembonds selection;
    d11: Lig285-C   = Lig285-N  -> this entry is included in the chembonds selection.
    d12: Ser130-HG1 = Lig285-CO2-O
    '''
    _selbase = 'segid Q{0} and'.format(str(repid))
    atom_i_sel = [
        ' (resid  72 and resname  LYS and name HZ2)',	# d4
        ' (resid  72 and resname  LYS and name HZ2)',	# d5
        ' (resid  72 and resname  LYS and name HZ1)',	# d6
        ' (resid  72 and resname  LYS and name HZ1)',	# d7
        ' (resid 129 and resname  SER and name HG1)',	# d8
        ' (resid 129 and resname  SER and name HG1)',	# d9
        ' (resid 129 and resname  SER and name HG1)',	# d9
        ' (resid  69 and resname  SER and name HG1)',	# d9
        ' (resid  69 and resname  SER and name  OG)',	# d9
    ]
    atom_j_sel = [
        ' (resid  69 and resname  SER and name  OG)',	# d4
        ' (resid  72 and resname  LYS and name  NZ)',	# d5
        ' (resid  72 and resname  LYS and name  NZ)',	# d6
        ' (resid 129 and resname  SER and name  OG)',	# d7
        ' (resid 129 and resname  SER and name  OG)',	# d8
        # missing Lig285-N				# d9
        # missing Lig285-CO2-O				# d12
    ]
    
    # Determine ligand name. 
    lig_sel= 'segid Q{0} and resid 285 and (resname {1} or resname {2})'.format(str(repid), 'AMP', 'CEX')
    lig = mda_universe.select_atoms(lig_sel)
    if lig.n_residues != 1 or (not lig.residues[0].resname in ['AMP', 'CEX', ]):
        print('LIG selected {0} residues or selected residue name {1}: check dist_rx().'.format(str(lig.n_residues), str(lig.residues[0])))
        exit()
    
    # Append missing ligand rx atoms.
    if lig.residues[0].resname == 'AMP':
        atom_i_sel.append(' (resid 285 and resname {0} and name  N4)'.format(lig.residues[0].resname))
        atom_i_sel.append(' (resid 285 and resname {0} and name  C7)'.format(lig.residues[0].resname))
        atom_i_sel.append(' (resid 285 and resname {0} and name  C7)'.format(lig.residues[0].resname))
        atom_j_sel.append(' (resid 285 and resname {0} and name  N4)'.format(lig.residues[0].resname))
        atom_j_sel.append(' (resid 285 and resname {0} and name O12)'.format(lig.residues[0].resname))
        atom_j_sel.append(' (resid 285 and resname {0} and name  C7)'.format(lig.residues[0].resname))
        atom_j_sel.append(' (resid 285 and resname {0} and name  C7)'.format(lig.residues[0].resname))
        atom_j_sel.append(' (resid 285 and resname {0} and name  C7)'.format(lig.residues[0].resname))
        atom_j_sel.append(' (resid 285 and resname {0} and name  C6)'.format(lig.residues[0].resname))
        atom_j_sel.append(' (resid 285 and resname {0} and name  O8)'.format(lig.residues[0].resname))
    elif lig.residues[0].resname == 'CEX':
        atom_i_sel.append(' (resid 285 and resname {0} and name  N5)'.format(lig.residues[0].resname))
        atom_i_sel.append(' (resid 285 and resname {0} and name  C8)'.format(lig.residues[0].resname))
        atom_i_sel.append(' (resid 285 and resname {0} and name  C8)'.format(lig.residues[0].resname))
        atom_j_sel.append(' (resid 285 and resname {0} and name  N5)'.format(lig.residues[0].resname))
        atom_j_sel.append(' (resid 285 and resname {0} and name O10B)'.format(lig.residues[0].resname))
        atom_j_sel.append(' (resid 285 and resname {0} and name  C8)'.format(lig.residues[0].resname))
        atom_j_sel.append(' (resid 285 and resname {0} and name  C8)'.format(lig.residues[0].resname))
        atom_j_sel.append(' (resid 285 and resname {0} and name  C8)'.format(lig.residues[0].resname))
        atom_j_sel.append(' (resid 285 and resname {0} and name  C7)'.format(lig.residues[0].resname))
        atom_j_sel.append(' (resid 285 and resname {0} and name  O8)'.format(lig.residues[0].resname))
    else:
        print('Wrong residue[0] name at resid 285: ' + str(lig.residue[0].resname))
        exit()

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

def extract_rxc(mda_universe, pathname, nrep=50, ):
    '''Extract all reaction coordinates in one RPM coordinate of nrep replicas..
    '''
    path_rxc_distmat    = []
    path_rxc_labelmat   = []

    for repid in range(1, nrep+1):
        print(repid)
        path_rxc_distrow, path_rxc_labelrow = dist_rx(mda_universe, repid, pathname, )
        path_rxc_distmat.append(path_rxc_distrow)
        path_rxc_labelmat.append(path_rxc_labelrow)
    
    return path_rxc_distmat, path_rxc_labelmat


import numpy

for s in ['toho_amp', 'toho_cex']:
    for p in ['r1', 'r2']:
        for t in ['dftb3', '3obf', 'b3lyp', 'b3lyp_pol', 'b3lyp_pol_disp']:
            u = get_path(s, p, t)
            distmat, lblmat= extract_rxc(u, p)
            numpy.save(f'./dist_npy/{s}.{p}.{t}.dist.npy', distmat)
            numpy.save(f'./dist_npy/{s}.{p}.{t}.label.npy', lblmat[0])
