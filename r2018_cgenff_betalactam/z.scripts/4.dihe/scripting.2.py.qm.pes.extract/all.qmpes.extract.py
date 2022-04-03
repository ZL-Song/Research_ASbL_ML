# Proj Force Field Dev - cephalosporins
# Dihedral angle force constants: Fragment V.
# Decrpt Gaussian output for HF pes extract.
# Usage:
#       python qm.pes.extract.py directory
# directory:
#   the directory contains all gaussian outputs, .log as output format.
#   will map all subdirectories, so a root directory is suggested.
# NOTE:
#   for each system, the method write_dihe_log() 'for i in rang()' loop should be customized manually:
#   assigning atom symbol for each atom number.
# Zilin Song, 17 Jan 2019
#  

import os
import os.path
import sys
import subprocess as subp

#interested directory
directory = sys.argv[1]
outputdirec = '../0.qm.pes.decrypted'

# write 1 line in dihe.log
# output format:
#           1_O1_1_C2_1_N3_1_C4             0       dihe_0.log
# usage: ((fi.readline()).split())[0].replace("_", " ") -> 1 O1 1 C2 1 N3 1 C4 -> cons ...
dihename_list = []
def write_dihe_log(atomNumbers, f):
    # f is the dihedral number
    
    atom_list = []

    # from:
    #       D       1       2       3       4 S 120 3.0000 
    # build:
    #       O1_C2_N3_C4
    # and write dihe.log
    # note:
    # C1 N2 C3 C4 S5 N6 H7 H8 H9 H10
    for i in range (1, 5):              #### change here for different system.
        if atomNumbers[i] == "1" or atomNumbers[i] == "3" or atomNumbers[i] == "4":
            atom_list.append("C{0}".format(atomNumbers[i]))
        elif atomNumbers[i] == "2" or atomNumbers[i] == "6": 
            atom_list.append("N{0}".format(atomNumbers[i]))
        elif atomNumbers[i] == "5":
            atom_list.append("S{0}".format(atomNumbers[i]))
        else:
            atom_list.append("H{0}".format(atomNumbers[i]))
    dihename = f.split('/').pop().replace('.log', '').replace('.pos', '').replace('.neg', '')

    isRecorded = False
    for dihe in dihename_list:
        if dihename == dihe:
            isRecorded = True

    if isRecorded == False:
        write_dihe_cons(atom_list)      # [O1, C2, N3, C4]
        dihename_list.append(dihename)
        file_dihe_log = open('{0}/dihe.log'.format(outputdirec), 'a')
        file_dihe_log.write(
            "{0:30}\t{1}\n".format(
                "{0}_{1}_{2}_{3}".format(atom_list[0], atom_list[1], atom_list[2], atom_list[3]), 
                dihename
                )
            )
        file_dihe_log.close()
    else:
        return
    
# write 1 line in dihe.cons for copying to charmm input
def write_dihe_cons(atom_list):

    file_cons_out = open('{0}/dihe.cons'.format(outputdirec), 'a')
    file_cons_out.write("CONS DIHE 1 {0} 1 {1} 1 {2} 1 {3} FORCe 9999. MAIN PERIod 0\n".format(atom_list[0], atom_list[1], atom_list[2], atom_list[3]))

# write something else in dihe.log
def write_statistics():
    ene_list = []
    dihe_log_out = open('{0}/dihe.log'.format(outputdirec), 'a')
    unfreeStr = '\n\nThe following dihedrals should apply 3 pt scan\n\nUnfree dihedrals:\n'
    for root, dirs, files in os.walk(outputdirec):
        for f in files:
            if f.endswith('.qm.ene'):
                ene_list.append('{0}/{1}'.format(root, f))
            else:
                pass
    for ene in ene_list:
        ene_n = ene.split('/').pop().replace('.qm.ene', '')
        with open(ene, 'r') as ene_file:
            ene_length = len(ene_file.readlines())
            dihe_log_out.write('\n## {0}\t{1}'.format(ene_n, ene_length))
            if ene_length < 122:
                unfreeStr += '{0}\n'.format(ene_n)
    dihe_log_out.write(unfreeStr + 'END')


# main
def main():

    file_list = []

    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith('.log'):
                file_list.append('{0}/{1}'.format(root, f))
            else:
                pass
    
    subp.call('rm -r {0}'.format(outputdirec), shell=True)

    subp.call('mkdir {0}'.format(outputdirec), shell=True)
    file_bash_out = open("sh.log.extract", 'w')
    file_bash_out.write("#!/bin/bash\n\n")
    file_bash_out.write("module load python\n\n")
    
    # decrypt each log file 1 by 1
    for f in file_list:
        dihe_name = ''
        with open(str(f), 'r') as log:
            line = str(log.readline())
            while line:
                words = line.split()
                if len(words) == 8 and line.startswith(' The following ModRedundant input section has been read:'):
                    line = str(log.readline())

                    # current line: D       1       2       3       4 S 120 3.0000 
                    words = line.split()

                    # 'D(1,2,3,4)'
                    dihe_name = "'{0}({1},{2},{3},{4})'".format(words[0],words[1],words[2],words[3],words[4])

                    #       python pes.extract.py dihedral_name template_pdb log_file_name outputdirec
                    file_bash_out.write('python pes.extract.py {0} template.pdb {1} {2}\n'.format(dihe_name, f, outputdirec))

                    write_dihe_log(words, f)
                    break
                line = log.readline()
    file_bash_out.close()
    subp.call('bash sh.log.extract', shell=True)
    write_statistics()

if __name__ == "__main__":
    main()