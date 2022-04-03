# Proj Force Field Dev - cephalosporins
# Water interaction: Fragment V.
# Decrpt Gaussian output for HF energy extract.
# Usage:
#       python qm.waterInterac.extract.py directory
#   directory:
#       the directory contains all gaussian outputs, .log as output format.
#       will map all subdirectories in this specification.
# Zilin Song, 14 Jan 2019
#  

import os
import os.path
import sys

# interested directory
directory = sys.argv[1]

file_list = []
file_origin = "frg5.original.log"

# Directory scan
for root, dirs, files in os.walk(directory):
    for f in files:
        if f.endswith('.log'):
            file_list.append('{0}/{1}'.format(root, f))
        else:
            pass

# Decrypt each file
decrypted_list = []
for f in file_list:
    with open(f, 'r') as log_file:
        ener = 0
        lines = log_file.readlines()
        for l in lines:
            if len(l.split()) == 9 and l.split()[2] == 'E(RHF)':        # specifies the target line to extract in .log file
                words = l.split()
                ener = words[4]
            else:
                pass

        decrypted_list.append('{0}\t{1}'.format(f.split('/').pop(), ener))

# organize qm energy file
ener_base = 0.
ener_list = []
ener_hoh = -76.010530 * 627.509
for d in decrypted_list:
    if d.split()[0] == file_origin:
        ener_base = float(d.split()[1]) * 627.509
    else:
        ener_list.append("{0}\t{1}".format(d.split()[0], float(d.split()[1]) * 627.509))
ener_list.sort()

# calc all interaction energy
with open('qm.target', 'w') as out_file:
    out_file.write('base\t{0}\n'.format(ener_base))
    out_file.write('hoh\t{0}\n'.format(ener_hoh))
    out_file.write('total\t{0}\n'.format(ener_hoh + ener_base))
    out_file.write('{0}\t{1}\t{2}\n'.format('file_name', 'inte_ener_scaled_1.16', 'complex_energy'))
    for entry in ener_list:
        name = entry.split()[0]
        ener = float(entry.split()[1])
        inter_ener = (ener - ener_base - ener_hoh) * 1.16
        out_file.write('{0}\t{1}\t{2}\n'.format(name, inter_ener, ener))


