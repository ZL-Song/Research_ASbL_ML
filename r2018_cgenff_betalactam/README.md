These are some very messy python scripts that implements the CGenFF parametrization scheme, i.e.:  

1. Charge;
2. Equilibrium Conf;
3. Force constants via CHARMM Local Mode analysis using Natural Internal Coordinates through Molvib module;
4. Charge reparametrization.

Do not spend too much time on this directory, there are easier and better ways to parametrize for a small organic (drug) molecule:

Unfortunately those efforts are unpublishable due to the limited number of fragments parametrized.  
(not-my-fault, this process is waaaaaaay tooooooo time-consuming for PhD students and I was new to CHARMM and python when starting all this stuff.)  

Very useful ref. for determining local modes via Natural Internal Coordinates.  
- J. Am. Chem. Soc. / 101:10 / May 9, 1979;  
- J. Am. Chem. Soc. 1992, 114, 8191-8201.  

Directory description.
- flavin.molvib:     The local model analysis based on Natural Internal Coordinates (NIC) using CHARMM/Molvib module;  
- z.scripts:         Here collects all (unsolved) scripts used for (not so) automatic parametrization of the 2-aminothiazole molecule;  
- cflt.tar.gz:       Case parametrization on cefalotin (putting several fragments together and make the big cefalotin molecule);  
- frg5.done.tar.gz:  Solved scripts for parametrizing 2-aminothiazole;  
- cgenff_ffdev_tutorial.docx/pdf: An unfinished document I wrote for describing how to do local mode analysis with CHARMM using its molvib module, this is a very crappy draft;  
- charmmff_format.dat: A (partial) description on the format of CGenFF parameters (CHARMM prm files).  
