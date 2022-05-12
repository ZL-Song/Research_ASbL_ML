# I/O for processing raw MEP files. 
# Zilin Song, 04 Dec 2021
# 

import MDAnalysis as mda
import numpy

def basedir():
    """Store the base directory."""
    return "/users/zilins/scratch/6.proj_ges_imi"

def loadpath(sysname, pathid, return_dir=False):
    """Load the pathway and return as a mda.universe object.
    e.g. /users/zilins/scratch/6.proj_ges_imi/1.sampling/1.ges_imi.d1/7.paths/path_opt/ges_imi.path_f1.cor
    """
    _basedir = basedir()
    _pathdir = f"{_basedir}/1.sampling/0.ges_imi.{sysname}/7.paths/path_opt" if sysname == 'd2' else \
               f"{_basedir}/1.sampling/1.ges_imi.{sysname}/7.paths/path_opt" if sysname == 'd1' else \
               None

    _psfdir  = f"{_pathdir}/ges_imi.path_f{pathid}.psf"
    _cordir  = f"{_pathdir}/ges_imi.path_f{pathid}.cor"

    if return_dir == True:
        return mda.Universe(_psfdir, _cordir, topology_format='PSF', format='CRD'), _psfdir, _cordir
    else:
        return mda.Universe(_psfdir, _cordir, topology_format='PSF', format='CRD')

def loadchrg(sysname, chrgscheme='nbo'):
    """Load the atomic charges."""
    _basedir = basedir()
    _sysdir = f"{_basedir}/1.sampling/0.ges_imi.{sysname}/8.sp" if sysname == 'd2' else \
              f"{_basedir}/1.sampling/1.ges_imi.{sysname}/8.sp" if sysname == 'd1' else \
              None
    
    _chrgdir = f"{_sysdir}/0.b3lyp_d3/chelpgs_mep.npy"      if chrgscheme == 'chelpg' else \
               f"{_sysdir}/1.b3lyp_d3_nbo/nbochrgs_mep.npy" if chrgscheme == 'nbo'    else \
               None
    
    _chrglabeldir = f"{_sysdir}/0.b3lyp_d3/chelpgs_label.npy"      if chrgscheme == 'chelpg' else \
                    f"{_sysdir}/1.b3lyp_d3_nbo/nbochrgs_label.npy" if chrgscheme == 'nbo'    else \
                    None
    
    return numpy.load(_chrgdir), numpy.load(_chrglabeldir)

def loadener(sysname):
    """Load the pathway energies.
    Return two numpy arrays: ener, barrier
    """
    _basedir = basedir()
    _sysdir = f"{_basedir}/1.sampling/0.ges_imi.{sysname}/8.sp/0.b3lyp_d3" if sysname == 'd2' else \
              f"{_basedir}/1.sampling/1.ges_imi.{sysname}/8.sp/0.b3lyp_d3" if sysname == 'd1' else \
              None
    
    _rawenedir = f"{_sysdir}/pathraw.ene"
    ener = []
    with open(_rawenedir, 'r') as infile:
        
        for line in infile:
            words = line.split()

            if words[0][0:2] == 'f:':
                ener.append(float(words[2]))
    
    _barriedir = f"{_sysdir}/pathbarrier.ene"
    barrier = []
    with open(_barriedir, 'r') as infile:

        for line in infile:
            words = line.split()
            barrier.append(float(words[1]))
    
    return numpy.asarray(ener), numpy.asarray(barrier)