# dihedral test for cephalosporins.
# NOTE:
#       Initial Test
# This script would:
#       1. Generate a output directory at father directory.
#       2. Copy the relevant files to output directory
#       3. Do dihe scan.
#       4. Note that, 
#           the doTest() method should be altered regarding to the interested system.
# Zilin Song, 1 FEB 2O19
# 

import subprocess as subp
import sys
import os

# establish working directory structure/ copy charmm files/ ready force field file.
def initialize(
    rootWorkPath: str, 
    mmSourceFolder: str,
    pySourceFolder: str
    ):

    # establish working path directory structure & files
    subp.call('mkdir -p {0}'.format(rootWorkPath), shell=True)
    subp.call('mkdir -p {0}/forcefield'.format(rootWorkPath), shell=True)
    subp.call('cp {0}/dihe_pes.inp {1}/.'.format(mmSourceFolder, rootWorkPath), shell=True)
    subp.call('cp {0}/frg5.strm {1}/frg5.strm.original'.format(mmSourceFolder, rootWorkPath), shell=True)
    subp.call('cp {0}/forcefield/*_all36_cgenff.* {1}/forcefield/.'.format(mmSourceFolder, rootWorkPath), shell=True)
    subp.call('cp {0}/forcefield/*.str {1}/forcefield/.'.format(mmSourceFolder, rootWorkPath), shell=True)
    subp.call('cp {0}/frg5.strm {1}/frg5.strm.original'.format(mmSourceFolder, rootWorkPath), shell=True)
    subp.call('cp {0}/pes.extract.py {1}/pes.extract.py'.format(pySourceFolder, rootWorkPath), shell=True)

    # enter work directory
    os.chdir(rootWorkPath)

def diheScan(
    steps: int,             # total number of steps
    perstep: list,          # size of each step
    diheList: list,         # list of dihedral angles
    diheNameList: list,     # list of names of dihedrals
    realWorkPath: str,      # work folder
    qmDataFolder: str,      # qm data folder
    outputName: str         # output file name
    ):
    file_out = open(outputName, 'a')

    testSetList = testSetGenerate(diheList, steps, perstep)

    file_out.write('{0} cases to go.\n\n'.format(len(testSetList)))
    
    global_min_pes_sum = 9999.9999
    global_min_pes_sum_list = []    
    global_min_pes_abs_sum = 9999.9999
    global_min_pes_abs_sum_list = []

    testCount = 1

    for test in testSetList:
        pesDiffes, absDiffes, pesSum, pesAbsSum = doTest(realWorkPath, qmDataFolder, test, diheNameList)
        if global_min_pes_sum >= pesSum:
            global_min_pes_sum = pesSum
            global_min_pes_sum_list = test[:]
        if global_min_pes_abs_sum >= pesAbsSum:
            global_min_pes_abs_sum = pesAbsSum
            global_min_pes_abs_sum_list = test[:]
        
        file_out.write('{0}\t|gPesSum: {1:0<8.6f}\t|gAbsSum: {2:0<8.6f}\t|sumDihe_n: {3}\tabsSumDihe_n: {4}|testSet: {5}\n'.format(
            testCount, global_min_pes_sum, global_min_pes_abs_sum, pesDiffes, absDiffes, test
            ))
        file_out.flush()
        testCount += 1
    
    file_out.close()

    return testCount, global_min_pes_sum, global_min_pes_sum_list, global_min_pes_abs_sum, global_min_pes_abs_sum_list
     
# generate target data list to be tested, once & for all
def testSetGenerate(
    diheList: list,
    steps: int,
    perstep: list
    ):
    # deep first search
    # this def provides all list in range(-steps, steps + 1)    
    def dfs(path):
        if len(path) == len(diheList):
            stepList.append(path[:])
            return
        if len(path) == 1:
            dfs(path + [1])
        elif len(path) == 2:
            dfs(path + [1])
        else:
            for i in range(-steps, steps + 1):
                dfs(path + [i])

    stepList = []
    dfs([])

    testSetList = []

    for step in stepList:
        testSet = []
        for j in range(0, len(step)):
            testSet.append(round(diheList[j] + perstep[j] * step[j], 4))

        testContainsNegative = False
        for t in testSet:
            if t <= 0:
                testContainsNegative = True
        if testContainsNegative == False:
            testSetList.append(testSet[:])
        else:
            pass

    return testSetList

# use CHARMM to do test, obtain/decrypt/return result
def doTest (
    realWorkPath: str,
    qmDataFolder: str,
    test: list,
    diheNameList: list
    ):

    # copy a new force field file
    subp.call('cp {0}/frg5.strm.original {0}/frg5.strm'.format(realWorkPath), shell=True)

    # modify the parameters in the force field file
    subp.call("sed -i -e 's/CG2R53 NG2R50 NG321  SG2R50    45.0000/CG2R53 NG2R50 NG321  SG2R50    {0:7.4f}/g' frg5.strm".format(test[0]), shell=True)
    subp.call("sed -i -e 's/NG321  CG2R53 NG2R50 CG2R51     3.0000/NG321  CG2R53 NG2R50 CG2R51     {0:6.4f}/g' frg5.strm".format(test[1]), shell=True)
    subp.call("sed -i -e 's/NG321  CG2R53 SG2R50 CG2R51     4.0000/NG321  CG2R53 SG2R50 CG2R51     {0:6.4f}/g' frg5.strm".format(test[2]), shell=True)
    
    for i in range(0, len(diheNameList)):
        print('/users/zilins/software/mpi.charmm/exec/gnu_M/charmm dihename:{0} pdbdir:{1}/{0}.pdbdir < dihe_pes.inp -o log'.format(diheNameList[i], qmDataFolder))
        subp.call('/users/zilins/software/mpi.charmm/exec/gnu_M/charmm dihename:{0} pdbdir:{1}/pdbdir/{0}.pdbdir < dihe_pes.inp -o log'.format(diheNameList[i], qmDataFolder), shell = True)
        print('python pes.extract.py {0} {1}'.format(diheNameList[i], qmDataFolder))
        subp.call('python pes.extract.py {0} {1}'.format(diheNameList[i], qmDataFolder), shell=True)

    pes_sum_list = []
    pes_abs_sum_list = []

    for j in range(0, len(diheNameList)):
        for k in open('{0}.ene'.format(diheNameList[j]), 'r'):
            words = k.split()
            if words[0] == '&&':
                pes_sum_list.append(float(words[2]))
                pes_abs_sum_list.append(float(words[4]))

    pes_sum = 0.
    pes_abs_sum = 0.
    
    for pes in pes_sum_list:
        pes_sum += abs(pes)
    
    for pesabs in pes_abs_sum_list:
        pes_abs_sum += abs(pesabs)

    return pes_sum_list, pes_abs_sum_list, pes_sum, pes_abs_sum
      
# write header in the output
def writeHeader(
    outputName: str,        # output file name: for writing mistake
    diheList: list,         # list of interested dihedrals
    diheNameList: list,     # list of names of interested dihedrals
    perstep: list,         # scan step size
    steps: int              # No. of scan steps
    ):
    # out put file ready
    file_out = open(outputName, 'w')

    # write header
    file_out.write("Molecular Dihedral Angle PES Scan for force field development.\nZilin Song, scripted on 1 FEB 2019.\n\nJob description:\n\n")
    file_out.write("Original test Set:\t{0}\nTest Dihedrals: \t{1}\nSteps for scanning:\t{2}\nScan Range: [-{3}, +{3}]\nScan Start.\n\n".format(diheList, diheNameList, steps, perstep))
    file_out.flush()

    #done
    file_out.close()

# write the summary
def writeSummary(
    outputName: str, 
    totalCase: int, 
    global_min_pes_sum: float, 
    global_min_pes_sum_list: list, 
    global_min_pes_abs_sum: float, 
    global_min_pes_abs_sum_list: list,
    ):
    file_out = open(outputName, 'a')

    file_out.write("\n\n===== Scan Done =====\n\nResult:\n\n")
    file_out.write("min pes diff sum: {0:0<8.6f}\nparams: {1}\n\n".format(global_min_pes_sum, global_min_pes_sum_list))
    file_out.write("min pes abs diff sum: {0:0<8.6f}\nparams: {1}\n\n".format(global_min_pes_abs_sum, global_min_pes_abs_sum_list))
    file_out.write("Case been processed: {0}".format(totalCase))
    file_out.flush()
    file_out.close()

# main(), entrance.
def main():
    # original dihes
    # 
    dihe_names = ['dihe_0', 'dihe_1', 'dihe_2']
    dihe_origin = [45.0000, 3.0000, 4.0000]
    
    # search range: original charges +/- (steps*perstep)
    steps = 100
    perstep = [1.0, 1.0, 1.0]

    workFolder = "result.init/case0"                      # folder name where all tests are done (critical to provide an unused folder name)
    outputName = "impr.pes.scan.py.out"                       # output file name
    workPath = "/users/zilins/scratch/forcefielddev/1.cephalosporins/0.fragmets/4.frg5/5.impr"    # directory where workFolder & sourceFolder locates / absolute directory in the file system
    mmSourceFolder = workPath + "/scripting.3.charmm.dihe_pes"       # folder name where all relevent files locates
    pySourceFolder = workPath + "/scripting.4.py.mm.pes.extract"     # folder name where all relevent files locates
    qmDataFolder = "../../0.qm.pes.decrypted"

    realWorkPath = "{0}/{1}".format(workPath, workFolder)
    
    # ready the test 
    initialize(realWorkPath, mmSourceFolder, pySourceFolder)

    writeHeader(outputName, dihe_origin, dihe_names, perstep, steps)

    caseCount, global_min_pes_sum, global_min_pes_sum_list, global_min_pes_abs_sum, global_min_pes_abs_sum_list = diheScan(
        steps, perstep, dihe_origin, dihe_names, realWorkPath, qmDataFolder, outputName
        )

    writeSummary(outputName, caseCount, global_min_pes_sum, global_min_pes_sum_list, global_min_pes_abs_sum, global_min_pes_abs_sum_list)


if __name__ == "__main__":
    main()