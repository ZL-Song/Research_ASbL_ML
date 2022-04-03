1
                 Chemistry at HARvard Macromolecular Mechanics
           (CHARMM) - Developmental Version 42b2   February 15, 2018            
       Copyright(c) 1984-2014  President and Fellows of Harvard College
                              All Rights Reserved
  Current operating system: Linux-3.10.0-693.21.1.el7.x86_64(x86_64)@login04.   
                 Created on  1/18/19 at 10:51:24 by user: zilins      

            Maximum number of ATOMS:    360720, and RESidues:      120240
 RDTITL> * PROJ FORCE FIELD DEV - SMALL DRUG MOLECULES
 RDTITL> * MOLECULAR VIBRATION FREQUENCY OPTIMIZATION
 RDTITL> * BASING ON GAUSSIAN MP2/6-31GD VIRBATIONAL SPECTRUM TO GENERATE QM TARGET DATA
 RDTITL> * USAGE: "important output file name"
 RDTITL> *   CHARMM < VIB_FREQ.INP > LOG.MM
 RDTITL> * ZILIN SONG, 18 JAN 2018
 RDTITL> *
  
 CHARMM>     
  
 CHARMM>     IOFOrmat EXTEented
 MISCOM> Expanded I/O format is used.
  
 CHARMM>     BOMLev -1
  
 CHARMM>     FASTer 1
 MISCOM> FAST option: ON (generic fast routines)
  
 CHARMM>     PRNLev 0

 DRUDES PARTICLES WILL BE GENERATED AUTOMATICALLY FOR ALL ATOMS WITH NON-ZERO ALPHA
 Thole-type dipole screening, Slater-Delta shape {S(u) = 1 - (1+u/2)*exp(-u)}, default radius =  1.300000
 WARNING from DECODF -- Zero length string being converted to 0.

      ***** LEVEL  0 WARNING FROM <PARRDR> *****
      ***** NO MATCH FOR NBFIX
      ******************************************
      BOMLEV ( -2) IS NOT REACHED. WRNLEV IS  5

 PARRDR> WARNING: ATOMS IN NBFIX O        CLGR1      -0.20000   3.40000 DONT EXIST

      ***** LEVEL  0 WARNING FROM <PARRDR> *****
      ***** NO MATCH FOR NBFIX
      ******************************************
      BOMLEV ( -2) IS NOT REACHED. WRNLEV IS  5

 PARRDR> WARNING: ATOMS IN NBFIX ON1      CLGR1      -0.20000   3.40000 DONT EXIST

      ***** LEVEL  0 WARNING FROM <PARRDR> *****
      ***** NO MATCH FOR NBFIX
      ******************************************
      BOMLEV ( -2) IS NOT REACHED. WRNLEV IS  5

 PARRDR> WARNING: ATOMS IN NBFIX ON1C     CLGR1      -0.20000   3.40000 DONT EXIST

      ***** LEVEL  0 WARNING FROM <PARRDR> *****
      ***** NO MATCH FOR NBFIX
      ******************************************
      BOMLEV ( -2) IS NOT REACHED. WRNLEV IS  5

 PARRDR> WARNING: ATOMS IN NBFIX OC2D1    CLGR1      -0.20000   3.40000 DONT EXIST

      ***** LEVEL  0 WARNING FROM <PARRDR> *****
      ***** NO MATCH FOR NBFIX
      ******************************************
      BOMLEV ( -2) IS NOT REACHED. WRNLEV IS  5

 PARRDR> WARNING: ATOMS IN NBFIX S        CLGR1      -0.38000   3.83000 DONT EXIST

      ***** LEVEL  0 WARNING FROM <PARRDR> *****
      ***** NO MATCH FOR NBFIX
      ******************************************
      BOMLEV ( -2) IS NOT REACHED. WRNLEV IS  5

 PARRDR> WARNING: ATOMS IN NBFIX HS       CLGR1      -0.20000   2.82000 DONT EXIST
 RDCMND: can not substitute energy "?NATC""
 RDCMND: can not substitute energy "?NATC""
 RDCMND: can not substitute energy "?WRNLEV""

 CONJUG> Minimization exiting with number of steps limit (  200) exceeded.

 FASTST> Second derivatives are not supported with FAST option.
         Using generic routines (enables second derivatives).

   >>>>>> Entering MOLVIB module of CHARMM <<<<<<


     MLVCOM: CHARMM RTF/PSF will be used inside MOLVIB


     MLVCOM: CHARMM second derivatives will be
      evaluated and passed directly to MOLVIB

  MOLVIB dimensions have been set

   NQ,NIC,NIC0,NAT =      24      24      34      -1
   IZMAX,MAXSYB,NGMAX,NBLMAX =      10      24      24      24

  The maximum dimension has been set to NQM =          34


   CHARMM cartesian coordinates passed to MOLVIB

    Atom #       X         Y         Z       MASS  
     1      0.75735   0.01301  -0.04850  12.01100
     2      0.27205   1.21014   0.14852  14.00700
     3     -1.13233   1.12739   0.13312  12.01100
     4     -1.64247  -0.13250  -0.07172  12.01100
     5     -0.36006  -1.24964  -0.25165  32.06000
     6      2.12297  -0.06943  -0.05592  14.00700
     7     -1.68875   2.04724   0.28137   1.00800
     8     -2.67201  -0.45734  -0.12616   1.00800
     9      2.47600   0.80696  -0.41356   1.00800
    10      2.47026  -0.08083   0.89049   1.00800

   Atomic masses passed to MOLVIB:

  12.01100 14.00700 12.01100 12.01100 32.06000 14.00700  1.00800  1.00800
   1.00800  1.00800 12.01100 14.00700 12.01100 12.01100 32.06000 14.00700
   1.00800  1.00800  1.00800  1.00800 12.01100 14.00700 12.01100 12.01100
  32.06000 14.00700  1.00800  1.00800  1.00800  1.00800



      MOLVIB : PROGRAM FOR MOLECULAR VIBRATIONAL SPECTROSCOPY



 GFX      0    0    0    0


   SELECTED OPTION : VIBRATIONAL EIGENVALUE PROBLEM IN CARTESIAN COORDINATES


 PRNT     0    0    0    0
  U matrix has been read : INU =            1

 The PED cutoff will be CUTPED =   0.150

       Starting FX diagonalization 


  **** Found            2   negative eigenvalues ****


    Symbolic PED matrix [%] (sorted)

   1     63.9   dNH2C1    92.
   2    244.3   5rTor_    53.   wagC1     45.
   3    278.4   rocC1     89.
   4    497.9   5rTor     65.   wagC1     21.
   5    514.5   5rDef     36.   sC1-N6    26.
   6    638.5   sC1-S5    33.   5rDef_    16.
   7    669.3   5rTor     35.   5rTor_    32.   wagC1     24.
   8    756.1   sC4-S5    38.   sC1-S5    23.   5rDef     21.
   9    783.8   wagC4     65.   wagC3     35.
  10    888.7   wagC3     73.   wagC4     39.
  11    943.1   sC4-S5    27.   5rDef_    25.   sC3=C4    16.
  12    963.4   wagN6     60.   sC1=N2    15.
  13   1070.3   rocN6     75.
  14   1091.6   rocC3     46.   rocC4     24.
  15   1131.8   sN2-C3    26.   rocC4     18.   rocC3     17.
  16   1341.1   sC1-N6    36.
  17   1385.6   sC1=N2    33.   rocC4     26.
  18   1465.2   sC1=N2    25.   sN2-C3    25.   rocC4     18.
  19   1549.6   sC3=C4    38.   scsN6     25.
  20   1583.8   scsN6     63.
  21   3134.6   sC4-H8    99.
  22   3183.0   sC3-H7    99.
  23   3353.0   sN6-H10   56.   sN6-H9    44.
  24   3401.4   sN6-H9    56.   sN6-H10   44.
 GFX option finished

      $$$$$$  New timer profile Local node$$$$$

      Heuristic check                 0.00 Other:            0.00
   List time                       0.00 Other:            0.00
         Electrostatic & VDW             0.00 Other:            0.00
      Nonbond force                   0.00 Other:            0.00
         Bond energy                     0.00 Other:            0.00
         Angle energy                    0.00 Other:            0.00
         Dihedral energy                 0.00 Other:            0.00
         Restraints energy               0.00 Other:            0.00
      INTRNL energy                   0.01 Other:            0.00
      Comm energy                     0.00 Other:            0.00
      Comm force                      0.00 Other:            0.00
   Energy time                     0.01 Other:            0.00
 Total time                      0.72 Other:            0.71

         $$$$$$  Average   profile $$$$$

      Heuristic check                 0.00 Other:            0.00
   List time                       0.00 Other:            0.00
         Electrostatic & VDW             0.00 Other:            0.00
      Nonbond force                   0.00 Other:            0.00
         Bond energy                     0.00 Other:            0.00
         Angle energy                    0.00 Other:            0.00
         Dihedral energy                 0.00 Other:            0.00
         Restraints energy               0.00 Other:            0.00
      INTRNL energy                   0.01 Other:            0.00
      Comm energy                     0.00 Other:            0.00
      Comm force                      0.00 Other:            0.00
   Energy time                     0.01 Other:            0.00
 Total time                      0.72 Other:            0.71
