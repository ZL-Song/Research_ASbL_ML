# charge test for cephalosporins.
# NOTE:
#       Initial Test
# This script would:
#       1. Generate a output directory at father directory.
#       2. Copy the relevant files to output directory
#       3. Do charge scan.
#       4. Note that, 
#           the doTest() method should be altered regarding to the interested system.
# Zilin Song, 15 JAN 2O19
# 

import subprocess as subp
import sys
import os


# establish working directory structure/ copy charmm files/ ready force field file.
def initialize(
    realWorkPath: str, 
    sourceFolder: str
    ):
    # create working path & work file preparation
    subp.call('mkdir -p {0}'.format(realWorkPath), shell=True)
    subp.call('mkdir -p {0}/forcefield'.format(realWorkPath), shell=True)
    subp.call('cp {0}/frg5.hfmini.crd {1}/.'.format(sourceFolder, realWorkPath), shell=True)
    subp.call('cp {0}/frg5.strm {1}/frg5.strm.original'.format(sourceFolder, realWorkPath), shell=True)
    subp.call('cp {0}/water_interact.inp {1}/.'.format(sourceFolder, realWorkPath), shell=True)
    subp.call('cp {0}/forcefield/*_all36_cgenff.* {1}/forcefield/.'.format(sourceFolder, realWorkPath), shell=True)
    subp.call('cp {0}/forcefield/*.str {1}/forcefield/.'.format(sourceFolder, realWorkPath), shell=True)

    # enter work directory, beyond this point, all the working directory is changed to working path.
    os.chdir(realWorkPath)

def writeHeader(outputName: str, charges_origin: list, steps: int, perstep: float):
    
    # output file ready
    file_out = open(outputName, 'w')

    # write header
    file_out.write("Charge scan for force field development: all water scan\nZilin Song, scripted on 8 JAN 2O19.\n\n")
    file_out.write("Job description:\n\n")
    file_out.write("Original charges: {0}\n\n".format(charges_origin))
    file_out.write("per step length: {0}\nnumber of step: {1}\n\nScan Start.\n\n\nGenerating test set...\n\nStand By...\n\n\n".format(perstep, steps))
    file_out.flush()

    #done
    file_out.close()

# iteration method
def chargeScan(
    charges_origin: list,
    steps : int,
    perstep: float,
    realWorkPath: str,
    outputName: str):
    
    file_out = open(outputName, 'a')
    
    testSetList = testSetGenerate(charges_origin, steps, perstep)
    file_out.write('{0} cases to go.\n\n'.format(len(testSetList)))
    global_min_ener = 999.999
    global_min_list_ener = []
    global_min_dist = 999.999
    global_min_list_dist = []    
    global_min_dipl = 999.999
    global_min_list_dipl = []

    testCount = 1
    for test in testSetList:
        enerDiff, distDiff, diplDiff = doTest(realWorkPath, test)
        if enerDiff <= global_min_ener:
            global_min_ener = enerDiff
            global_min_list_ener = test[:]
        if distDiff <= global_min_dist:
            global_min_dist = distDiff
            global_min_list_dist = test[:]        
        if diplDiff <= global_min_dipl:
            global_min_dipl = diplDiff
            global_min_list_dipl = test[:]
            
        file_out.write('{0}\t|gE_min: {1:0<8.6f}\tgD_min: {2:0<8.6f}\tgDPL_min: {3:0<8.6f}\t|currE_min: {4:0<8.6f}\tcurrD_min: {5:0<8.6f}\tcurrDpl_min: {6:0<8.6f}\t|testDat: {7}\n'.format(
            testCount, global_min_ener, global_min_dist, global_min_dipl, enerDiff, distDiff, diplDiff, test
        ))
        file_out.flush()

        testCount += 1
    
    file_out.close()

    return testCount, global_min_ener, global_min_list_ener, global_min_dist, global_min_list_dist, global_min_dipl, global_min_list_dipl

# use CHARMM to do test, obtain/decrypt/return result
def doTest(
    realWorkPath: str, 
    test: list
    ):

    # copy a new force field file
    subp.call('cp {0}/frg5.strm.original {0}/frg5.strm'.format(realWorkPath), shell=True)

    # modify the parameters in the force field file
    subp.call("sed -i -e 's/ATOM C1     CG2R53  0.302/ATOM C1     CG2R53 {0:6.3f}/g' frg5.strm".format(test[0]), shell=True)
    subp.call("sed -i -e 's/ATOM N2     NG2R50 -0.620/ATOM N2     NG2R50 {0:6.3f}/g' frg5.strm".format(test[1]), shell=True)
    subp.call("sed -i -e 's/ATOM C3     CG2R51  0.209/ATOM C3     CG2R51 {0:6.3f}/g' frg5.strm".format(test[2]), shell=True)
    subp.call("sed -i -e 's/ATOM C4     CG2R51 -0.185/ATOM C4     CG2R51 {0:6.3f}/g' frg5.strm".format(test[3]), shell=True)
    subp.call("sed -i -e 's/ATOM S5     SG2R50 -0.053/ATOM S5     SG2R50 {0:6.3f}/g' frg5.strm".format(test[4]), shell=True)
    subp.call("sed -i -e 's/ATOM N6     NG321  -0.670/ATOM N6     NG321  {0:6.3f}/g' frg5.strm".format(test[5]), shell=True)
    subp.call("sed -i -e 's/ATOM H7     HGR52   0.130/ATOM H7     HGR52  {0:6.3f}/g' frg5.strm".format(test[6]), shell=True)
    subp.call("sed -i -e 's/ATOM H8     HGR52   0.177/ATOM H8     HGR52  {0:6.3f}/g' frg5.strm".format(test[7]), shell=True)
    subp.call("sed -i -e 's/ATOM H9     HGPAM2  0.355/ATOM H9     HGPAM2 {0:6.3f}/g' frg5.strm".format(test[8]), shell=True)
    subp.call("sed -i -e 's/ATOM H10    HGPAM2  0.355/ATOM H10    HGPAM2 {0:6.3f}/g' frg5.strm".format(test[9]), shell=True)

    subp.call('/users/zilins/software/mpi.charmm/exec/gnu_M/charmm -i water_interact.inp -o log', shell=True)

    enerList = []
    distList = []
    
    qm_x = 0.
    qm_y = 0.
    qm_z = 0.
    
    mm_x = 0.
    mm_y = 0.
    mm_z = 0.

    for l in open('frg5_water_interact.ene', 'r'):
        words = l.split()
        if words[0] == "ENE":
            enerList.append(float(words[2]))
            distList.append(float(words[5]))
        elif words[0] == 'HF/6-31G(D)':
            qm_x = float(words[2].replace('X=', ''))
            qm_y = float(words[3].replace('Y=', ''))
            qm_z = float(words[4].replace('Z=', ''))
        elif words[0] == 'EMPIRICAL':
            mm_x = float(words[2].replace('X=', ''))
            mm_y = float(words[3].replace('Y=', ''))
            mm_z = float(words[4].replace('Z=', ''))
        else:
            pass
    
    enerTot = 0.
    distTot = 0.
    diplTot = 0

    for ener in enerList:
        enerTot += round(abs(ener), 3)
    for dist in distList:
        distTot += round(abs(dist), 3)
    diplTot = ((mm_x - qm_x) ** 2 + (mm_y - qm_y) ** 2 + (mm_z - qm_z) ** 2) ** (1 / 2)

    return enerTot, distTot, diplTot

# generate target data list to be tested, once & for all
def testSetGenerate(charges_origin: list, steps: int, perstep: float):
    # deep first search
    # this def provides all list in range(-steps, steps + 1) with elememt sum = 0
    def dfs(path, sumv):
        if len(path) == len(charges_origin):
            if sumv == 0 :
                stepList.append(path)
            return

        # NOTE: the stepList only contains lists of "steps" to take for each chrg. 
        # NOT the chrg value
        
        # make sure path[8] == path[9] 
        if len(path) == 9:
            dfs(path + [path[8]], sumv + path[8])
        elif len(path) == 6:    # H7 stay the same
            dfs(path + [0], sumv + 0)
        elif len(path) == 7:    # H8 stay the same
            dfs(path + [0], sumv + 0)
        else:
            for i in range(-steps, steps + 1):
                dfs(path+[i], sumv+i)
    
    stepList = []
    dfs([], 0)
    
    testSetList = []
    for i in stepList:
        testSet = []
        for j in range(0, len(i)):
            testSet.append(round(charges_origin[j] + perstep * i[j], 3))
        sum = 0.
        for t in testSet:
            sum += t
        if sum != 0:
            sys.stdout.write(str(i))
            sys.stdout.write('\t')
            sys.stdout.write(str(testSet))
            sys.stdout.write('\t')
            sys.stdout.write(str(sum))
            sys.stdout.write('\n')
        testSetList.append(testSet[:])
    
    return testSetList

# write the summary
def writeSummary(
    outputName: str, 
    totalCase: int, 
    global_min_ener: float, 
    global_min_list_ener: list, 
    global_min_dist: float, 
    global_min_list_dist: list,
    global_min_dipl: float, 
    global_min_list_dipl: list
    ):
    file_out = open(outputName, 'a')

    file_out.write("\n\n===== Scan Done =====\n\nResult:\n\n")
    file_out.write("min energy sum: {0:0<8.6f}\nparams: {1}\n\n".format(global_min_ener, global_min_list_ener))
    file_out.write("min distan sum: {0:0<8.6f}\nparams: {1}\n\n".format(global_min_dist, global_min_list_dist))
    file_out.write("min dipole sum: {0:0<8.6f}\nparams: {1}\n\n".format(global_min_dipl, global_min_list_dipl))
    file_out.write("Case been processed: {0}".format(totalCase))
    file_out.flush()
    file_out.close()

# main(), entrance.
def main():
    # original charges   C1     N2      C3      C4      S5      N6      H7    H8    H9    H10
    #                    0      1       2       3       4       5       6     7     8      9 
    charges_origin = [0.952, -0.54, -0.151, -0.675, 0.417, -0.56, 0.13, 0.177, 0.125, 0.125]
    
    # search range: original charges +/- (steps*perstep)
    steps = 1
    perstep = 0.01

    workFolder = "result.high/case4"                      # folder name where all tests are done (critical to provide an unused folder name)
    sourceFolder = "scripting.0.charmm.water_interac"       # folder name where all relevent files locates
    outputName = "charge.scan.py.out"                       # output file name
    workPath = "/scratch/users/zilins/forcefielddev/1.cephalosporins/0.fragmets/4.frg5/1.chrg"    # directory where workFolder & sourceFolder locates / absolute directory in the file system

    realWorkPath = "{0}/{1}".format(workPath, workFolder)
    realSourcePath = "{0}/{1}".format(workPath, sourceFolder)
    
    # ready the test 
    initialize(realWorkPath, realSourcePath)

    # write header in output file
    writeHeader(outputName, charges_origin, perstep, steps)

    #totalCase, global_min_ener, global_min_dist, global_min_list = 
    totalCase, global_min_ener, global_min_list_ener, global_min_dist, global_min_list_dist, global_min_dipl, global_min_list_dipl = chargeScan(
        charges_origin, steps, perstep, realWorkPath, outputName
        )

    writeSummary(outputName, totalCase, global_min_ener, global_min_list_ener, global_min_dist, global_min_list_dist, global_min_dipl, global_min_list_dipl)

if __name__ == "__main__":
    main()