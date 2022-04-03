# Proj Force Field Dev - cephalosporins
# Dihedral angle force constants: Fragment V.
# Decrypt outputs from gaussian qm pes & charmm mm pes for
#       a ** SINGLE ** dihedral angle pes calc
# In 1 word: from dihe_n.mm.ene and dihe_n.qm.ene => dihe_n.ene
# Usage:
#       python pes.extract.py dihe_n qm_directory
#       python pes.extract.py dihe_2 ../0.qm.pes.decrypted/
# dihedralName:
#   the name of dihedral in the following form: 
#       dihe_1
#       dihe_10
# qm_directory:
#   the directory that contains all qm extracted data
# Zilin Song, 18 Jan 2019
#  

import os
import os.path
import sys
import subprocess as subp

dihe_n = sys.argv[1]
qm_directory = sys.argv[2]

def main():
    logmm = '{0}.mm.ene'.format(dihe_n)
    logqm = '{0}/ene/{1}.qm.ene'.format(qm_directory, dihe_n)

    if os.path.isfile(logmm) and os.path.isfile(logqm):
    
        mm_list = decryptMmData(logmm)
        qm_list = decrypteQmData(logqm)

        mmqm_list = []

        for mm_angle, mm_ener in mm_list:
            for qm_angle, qm_ener in qm_list:
                if mm_angle == qm_angle:
                    mmqm_list.append((mm_angle, mm_ener, qm_ener, qm_angle))
                    break
        
        enerdiff = 0.
        abs_enerdiff = 0.

        with open('{0}.ene'.format(dihe_n), 'w') as file_out:
            for angle, mm_ener, qm_ener, angle_ref in mmqm_list:
                file_out.write('{0}\t{1:.6f}\t{2:.6f}\t{3}\n'.format(angle, mm_ener, qm_ener, angle_ref))
                enerdiff += round(mm_ener - qm_ener, 4)
                abs_enerdiff += round(abs(mm_ener - qm_ener), 4)

            enerdiff = round(enerdiff, 4)
            abs_enerdiff = round(abs_enerdiff, 4)

            file_out.write('&& Diff= {0} absDiff= {1}'.format(enerdiff, abs_enerdiff))
           
    else:
        pass

# decrypt mm pes data and return in a list of tuple(dihedral_angle, relative_energy)
# relative energy is the energy change compares to energy(initial comformation)
def decryptMmData(logmm: str) -> list:
    
    file_in_mm = open(logmm, 'r')

    lines = file_in_mm.readlines()
    
    mm_list_raw = []

    for l in lines:
        words = l.split()
        pe_coor_mm = (words[2].split('/').pop().replace('.PDB', ''), words[1])
        mm_list_raw.append(pe_coor_mm)

    inil_dihe_angle, inil_dihe_ener = mm_list_raw[0]
    
    inil_coor = (inil_dihe_angle, 0)

    mm_list = []
    mm_list.append(inil_coor)
    
    for i in range(1, len(mm_list_raw)):
        dihedral, energy = mm_list_raw[i]
        mm_list.append((int(dihedral), round(float(energy) - float(inil_dihe_ener), 6)))
        
    return mm_list

# decrypt qm pes data and return in a list of tuple(dihedral_angle, relative_energy)
# relative energy is the energy change compares to energy(initial comformation)
def decrypteQmData(logqm: str) -> list:

    file_in_qm = open(logqm, 'r')

    lines = file_in_qm.readlines()

    qm_list = []

    inil_angle, inil_ener = (int(lines[0].split()[0]), float(lines[0].split()[1]))

    for l in lines:
        angle, ener = (int(l.split()[0]), float(l.split()[1]))
        qm_list.append((int(angle), float(round(ener - inil_ener, 6))))

    return qm_list
                
if __name__ == "__main__":
    main()
