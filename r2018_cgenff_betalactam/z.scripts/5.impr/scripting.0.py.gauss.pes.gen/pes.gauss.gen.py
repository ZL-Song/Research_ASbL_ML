import subprocess as subp
import sys
import os

# Dihedral force constant test for pnm part III
# Input requirement:
#       a file named 'dihedrals' must present in the same directory with this script
#       format requisition of 'dihedrals
#               O1-C2-N3-C4,  penalty= 30.8
#               O1-C2-N3-C7,  penalty= 10.3
#
# This script is used for generating:
#       gaussian input files for dihedral pes scan
# 
# Zilin Song, 8 JAN 2019
#

# string shared for all gauss.inp
gaussian_header = r"""%nprocshared=1
# opt=modredundant mp2/6-31g(d)

frg5

0 1
 C                  0.76857200    0.21338200   -0.00624200
 N                  0.15904000    1.33576600    0.00118500
 C                 -1.20736200    1.14292000    0.00566600
 C                 -1.63785200   -0.12118800    0.01215200
 S                 -0.26413400   -1.19491700   -0.00837300
 N                  2.13128500    0.08621300   -0.07082200
 H                 -1.84362500    2.00598800    0.01197700
 H                 -2.64062500   -0.49170000    0.02789200
 H                  2.60861200    0.94146900    0.12083000
 H                  2.52936200   -0.70161200    0.39127400"""

def trimStr(stringToTrim: str):
    return stringToTrim.replace('-', ' ').replace('C', '').replace('N', '').replace('O', '').replace('H', '').replace('S', '').replace(',', '')

def main():
    subp.call('mkdir gaussIn', shell=True)
    with open('dihedrals', 'r') as file_log:
        line = file_log.readline()
        dihe_no = 0
        gjf_name = 'dihe_{0}'.format(dihe_no)
        while line:
            words = line.split()
            if len(words) != 0:

                with open('{0}/{1}.pos.gjf'.format('gaussIn', gjf_name), 'w') as file_out_pos:
                    file_out_pos.write(gaussian_header)
                    dihe_name = trimStr(str(words[0]))
                    file_out_pos.write("\n\nD {0} S 1 2.0\n\n\n\n\n".format(dihe_name))
            
                with open('{0}/{1}.neg.gjf'.format('gaussIn', gjf_name), 'w') as file_out_neg:
                    file_out_neg.write(gaussian_header)
                    dihe_name = trimStr(str(words[0]))
                    file_out_neg.write("\n\nD {0} S 1 -2.0\n\n\n\n\n".format(dihe_name))
                dihe_no += 1
                gjf_name = 'dihe_{0}'.format(dihe_no)

            line = file_log.readline()

if __name__ == "__main__":
    main()