import subprocess as subp
import sys
import os

# Dihedral force constant test for pnm part III
# This script is used for extracting ***SINGLE*** Gaussian pes calc output log file to:
#       pdbs, pes coor & pdb directories.
#       pdbs:               pdb coor files of each pes points
#       pdb directories:    a formated file recording abs directory of each pdb
#       pes coor:           a formated file recording all points on pes
#       
# usage:
#       python pes.extract.py dihedral_name template_pdb log_file_name output_direc
# 
# NOTE:
#       1. dihedral_name should be in the form:
#           'D(1,2,3,4)'
#       2. template_pdb in the same directory is required for this script.
#           template_pdb is the same pdb for the interested system, 
#           and is used for generate pdbs with different coor.
# 
# Zilin Song, 4 Jan 2018
# 

# read template pdb to generate template for output
def readTemp(temp_name):
    
    no_atoms = 0
    template = []

    file_temp = open(temp_name, 'r')
    for line in file_temp.readlines():
        words = line.split()
        if words[0] == "ATOM":
            no_atoms += 1
            template.append(line)
        elif words[0] == "TER" or words[0] == "END":
            template.append(line)
        else:
            pass
    file_temp.close()

    return template, no_atoms

def main():
    
    dihedral_name = sys.argv[1]
    temp_name = sys.argv[2]
    log_name = sys.argv[3]
    outputdirec = sys.argv[4]

    # ../scripting.1.bash.gauss.pes.launch/dihe_1.pos/dihe_1.pos.log  ->   DIHE_1
    dihe_number = log_name.split('/').pop().replace('.log', '').replace('.neg', '').replace('.pos', '')

    # read template pdb to generate template for output
    # note that in template_pdb, REMARK lines is not read in template[]
    template, no_atoms = readTemp(temp_name)

    subp.call('mkdir {0}'.format(outputdirec), shell=True)
    subp.call('mkdir {0}/ene'.format(outputdirec), shell=True)
    subp.call('mkdir {0}/pdbdir'.format(outputdirec), shell=True)
    subp.call('mkdir {0}/pdbs'.format(outputdirec), shell=True)
    subp.call('mkdir {0}/pdbs/{1}'.format(outputdirec, dihe_number), shell=True)

    file_ener_coor = open("{0}/ene/{1}.qm.ene".format(outputdirec, dihe_number), 'a')
    file_pdb_direc = open("{0}/pdbdir/{1}.pdbdir".format(outputdirec, dihe_number), 'a')

    ener = -999999.9999
    dihe = -361.0
    x = []
    y = []
    z = []

    # read log:
    # note that writing files when "Optimization completed." is reached ensures that,
    #   the coor & ener corresponds to the coor & ener that opt is completed.
    #   the coors & eners before opt completed is read but not writen.
    file_log = open(log_name, 'r')
    line = file_log.readline()
    while line:
        words = line.split()
        if len(words) > 1:          # not empty line
            
            # read energy:
            # E2 =    -0.1106240735D+01 EUMP2 =    -0.72132319415786D+03 
            if len(words) == 6 and words[3] == "EUMP2":
                ener = float(words[5].replace("D", "E")) * 627.5095     # convert HF to kcal/mol
                
            # read coor:
            #                          Input orientation:      
            elif len(words) == 2 and words[0] == "Input" and words[1] == "orientation:":
                
                # jump the current line & following 4 lines:
                # ---------------------------------------------------------------------
                # Center     Atomic      Atomic             Coordinates (Angstroms)
                # Number     Number       Type             X           Y           Z
                # ---------------------------------------------------------------------
                jump = 0
                while jump < 5:
                    line = file_log.readline()
                    jump += 1
                
                # record coors:
                #      1          8           0       43.410208   18.858419   27.045674
                iatom = 0
                x = []
                y = []
                z = []
                while iatom < no_atoms:
                    words = line.split()
                    x.append(float(words[3]))
                    y.append(float(words[4]))
                    z.append(float(words[5]))
                    line = file_log.readline()
                    iatom += 1
            
            # read optimized param:
            # Optimization completed.
            elif len(words) == 2 and words[0] == "Optimization" and words[1] == "completed.":

                # jump lines until interested D(1,2,3,4) parameters data
                # and read corresponding dihedral angle
                line = file_log.readline()       # keep reading lines
                while line:

                    words = line.split()
                    #print("xxxxXXX{0}".format(words))
                    # read param:
                    # ! D1    D(1,2,3,4)           -133.5243         -DE/DX =   -0.0008              !
                    # & make sure not:
                    # ! D1    D(1,2,3,4)             40.4758         Scan                            !
                    if len(words) == 8 and words[2] == dihedral_name and words[4] == "-DE/DX":
                        dihe = round(round(float(words[3]), 1))         # make sure no overlap dihe
                        break
                    line = file_log.readline()
                
                # reading done. dihedral found, write files
                if dihe < 0.:
                    dihe += 360
                file_ener_coor.write("{0}\t\t{1}\n".format(dihe, ener))

                with open("{0}/pdbs/{1}/{2}.pdb".format(outputdirec, dihe_number, dihe), 'w') as file_pdb_out:
                    file_pdb_direc.write("{0}\n".format(
                        os.path.realpath("{0}/pdbs/{1}/{2}.pdb".format(outputdirec, dihe_number, dihe)))
                        )
                    file_pdb_out.write("REMARK dihedral {0} at {1}, total energy by MP2 = {2} kcal/mol\n".format(
                        dihedral_name, dihe, ener
                    ))
                    for ia in range(0, no_atoms):
                        # no '\n' in the end of the string: '\n' included in template
                        file_pdb_out.write("{0}{1:8.3f}{2:8.3f}{3:8.3f}{4}".format(
                            template[ia][0:30], x[ia], y[ia], z[ia], template[ia][54:]
                        ))
                    file_pdb_out.write(template[no_atoms])
                    file_pdb_out.write(template[no_atoms + 1])

        line = file_log.readline()
                
if __name__ == "__main__":
    main()
