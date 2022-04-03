import subprocess as subp
import sys

# Molecular Vibrational Spectrum test for pnm part III
# This script is used for extracting CHARMM output log file to FREQ.ENE.
# Could not be called by CHARMM script
# NOTE:     
#       qm molvib output log must be named as "log.qm"
#       mm molvib output log must be named as "log.mm"
# 
# Zilin Song, 27 DEC 2018
# 

# check is number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
# Extract log file with the name, file_name. this method returns a list with frequencies
def extract_log(
    file_name :str
    ) -> list:

    switch_start = False
    freq_result = []
    freq_list = []
    
    with open(file_name, 'r') as fr:
        line = fr.readline()
        while line:
            words = line.split()
            # note: interested output region could have 
            #     1, empty lines; 2, 1 frequency discription on multiple lines.
            if switch_start == True and line != "\n" and is_number(words[0]):
                freq_result.append(words[1])
            else: 
                pass
            # check if entered interested output region.
            if line.startswith("    Symbolic PED matrix [%] (sorted)"):
                switch_start = True
                line = fr.readline()
            elif line.startswith(" GFX option finished"):
                switch_start = False
                freq_result.pop()
            else:
                pass
            
            line = fr.readline()
    
    for txtFr in freq_result:
        freq_list.append(float(txtFr))

    return freq_list

def main():
    qm_molvib_file = "log.qm"
    mm_molvib_file = "log.mm"

    qm_freq_list = extract_log(qm_molvib_file)
    mm_freq_list = extract_log(mm_molvib_file)

    freq_diff_abs = 0.
    freq_diff = 0.

    # write freq.ene
    with open("freq.ene", 'w') as fw:
        fw.write("qm\t\tmm\n")
        if len(qm_freq_list) == len(mm_freq_list):
            for flag in range(0, len(qm_freq_list)):
                freq_diff_abs += abs(mm_freq_list[flag] - qm_freq_list[flag])
                freq_diff += mm_freq_list[flag] - qm_freq_list[flag]
                fw.write("{0}\t\t{1}\n".format(qm_freq_list[flag], mm_freq_list[flag]))
        else:
            fw.write("\n\nIllegal frequency list: no. qm freq != no. mm freq.")
            exit
        
        fw.write("&& DIFF: {0} Abs(Diff): {1}".format(freq_diff, freq_diff_abs))

if __name__ == "__main__":
    main()