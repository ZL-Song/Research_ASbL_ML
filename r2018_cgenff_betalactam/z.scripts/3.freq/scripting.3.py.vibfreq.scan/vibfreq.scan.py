# Molecular Vibrational Spectrum Scan
# parameters changed is marked with ## in strm file
# too much parameters so that this script is suggested reading carefully before run.
# NOTE:
#   the scan principle of bond length & angle force constant is different from charge: 
#   paramters are independent to each other (in charge, the total charge must stay unchanged)
# NOTE:
#   for each test, result file "freq.ene" is generated by "diff.extract.py"
#   diff.extract.py takes the input "log.mm", which should be the output name of CHARMM script "bond_vibfreq.inp"
#   "charmm < bond_vibfreq.inp > log.mm"
# this script is similiar to bond.LeAn.scan.py, but have some major differences: only 1 minima is tested
# 
# Zilin Song, 18 JAN 2019
# 

import subprocess as subp
import sys
import os

# establish working directory structure/ copy charmm files/ ready force field file.
def initialize(
    rootWorkPath: str, 
    mmSourceFolder: str,
    qmSourceFolder: str,
    pySourceFolder: str
    ):

    # establish working path directory structure & files
    subp.call('mkdir -p {0}'.format(rootWorkPath), shell=True)
    subp.call('mkdir -p {0}/forcefield'.format(rootWorkPath), shell=True)
    subp.call('cp {0}/frg5.hfmini.crd {1}/.'.format(mmSourceFolder, rootWorkPath), shell=True)
    subp.call('cp {0}/frg5.strm {1}/frg5.strm.original'.format(mmSourceFolder, rootWorkPath), shell=True)
    subp.call('cp {0}/vib_freq.inp {1}/.'.format(mmSourceFolder, rootWorkPath), shell=True)
    subp.call('cp {0}/log.qm {1}/.'.format(qmSourceFolder, rootWorkPath), shell=True)
    subp.call('cp {0}/vibfreq.extract.py {1}/.'.format(pySourceFolder, rootWorkPath), shell=True)
    subp.call('cp {0}/forcefield/*_all36_cgenff.* {1}/forcefield/.'.format(mmSourceFolder, rootWorkPath), shell=True)
    subp.call('cp {0}/forcefield/*.str {1}/forcefield/.'.format(mmSourceFolder, rootWorkPath), shell=True)

    # enter work directory
    os.chdir(rootWorkPath)

# write header in the output
def writeHeader(
    outputName: str,        # output file name: for writing mistake
    lenList: list,          # lenList: list of bond lengthes, used to generate targetSetList
    lenSteps: int,          # lenSteps: No. scan steps for bond lengthes, used to generate targetSetList
    lenPerStep: float,      # lenPerStep: scan step size for bond lengthes, used to generate targetSetList
    angList: list,          # angList: list of bond angles, used to generate targetSetList
    angSteps: int,          # angSteps: No. scan steps for bond angles, used to generate targetSetList
    angPerStep: float       # angPerStep: scan step size for bond angles, used to generate targetSetList
    ):
    # out put file ready
    file_out = open(outputName, 'w')

    originSet = lenList[:].extend(angList[:])

    # write header
    file_out.write("Molecular Vibrational Spectrum Scan for force field development.\nZilin Song, scripted on 17 Dec 2018.\n\nJob description:\n\n")
    file_out.write("Bond stretching force constants:\t{0}\nScan Steps:\t{1}\nStep Size:\t{2}\nBond Length set:\t{3}\n\n".format(len(lenList), lenSteps, lenPerStep, lenList))
    file_out.write("Bond scissoring force constants:\t{0}\nScan Steps:\t{1}\nStep Size:\t{2}\nBond Length set:\t{3}\n\n".format(len(angList), angSteps, angPerStep, angList))
    file_out.write("Original test Set:\t{0}\n\nScan Start.\n\n".format(originSet))
    file_out.flush()

    #done
    file_out.close()

# write summary in the output
def writeSummary(
    outputName: str, 
    global_min_diffSum: float, 
    global_min_diffSumTest: list, 
    global_min_absDiffSum: float,
    global_min_absDiffSumTest: list,
    totalCase: int,
    actualTotalCase: int
    ):
    file_out = open(outputName, 'a')

    file_out.write("\n\n===== Scan Done =====\n\nResult:\n\n")
    file_out.write("lowest diff sum: {0:0<8.6f}\nparams: {1}\n\n".format(global_min_diffSum, global_min_diffSumTest))
    file_out.write("lowest abs diff sum: {0:0<8.6f}\nparams: {1}\n\n".format(global_min_absDiffSum, global_min_absDiffSumTest))
    file_out.write("Total case count: {0}\nCase been processed: {1}\n\n".format(totalCase, actualTotalCase))
    file_out.flush()
    file_out.close()

# generate target data list to be tested, once & for all
def testSetGenerate(
    targetParam: int,       # targetParam:
                            #       Used in testSetGenerate(...)
                            #       0: both bond lengthes and angles to be scaned
                            #       1: only bond lengthes to be scaned
                            #       2: only bond angles to be scaned
                            #       also used to generate targetSetList
    lenList: list,          # lenList: list of bond lengthes, used to generate targetSetList
    lenSteps: int,          # lenSteps: No. scan steps for bond lengthes, used to generate targetSetList
    lenPerStep: float,      # lenPerStep: scan step size for bond lengthes, used to generate targetSetList
    angList: list,          # angList: list of bond angles, used to generate targetSetList
    angSteps: int,          # angSteps: No. scan steps for bond angles, used to generate targetSetList
    angPerStep: float,      # angPerStep: scan step size for bond angles, used to generate targetSetList
    outputName: str         # output file name: for writing mistake
    ) -> list:

    # target rawTestSetList generation method:
    #       not tolal combination for all circumstances
    #       lenList.extend(angList) as original list: 
    #       rawTestSetList only change the member in the original list, one at a time in test range
    #       test range: {original[i] - lenSteps * lenPerStep, original[i] + lenSteps * lenPerStep}

    rawTestSetList = []        # target rawTestSetList to be generated

    # sets that contains all length & angles: 
    # seperated because len & ang could have different step size & step count
    lenSetList = []
    angSetList = []
    
    # buffer list
    tempList = []

    # generate lenSetList
    for noLe in range(0, len(lenList)):
        for i in range(-lenSteps, lenSteps + 1):
            lenRaw = lenList[:]
            length = round(lenList[noLe] + i * lenPerStep, 4)
            lenRaw[noLe] = length
            lenSetList.append(lenRaw[:])
    
    # generate angSetList
    for noAn in range(0, len(angList)):
        for j in range(-angSteps, angSteps +1):
            angRaw = angList[:]
            angle = round(angList[noAn] + j * angPerStep, 4)
            angRaw[noAn] = angle
            angSetList.append(angRaw[:])

    file_out = open(outputName, 'a')
    if targetParam == 0:         # 0: both bond lengthes and angles to be scaned
        # extent each list in lenSetList with original angle list, append extended list to rawTestSetList
        for l in lenSetList:
            tempList.extend(l[:])
            tempList.extend(angList[:])
            rawTestSetList.append(tempList[:])
            tempList.clear()

        # extent original length list with angSetList, append extended list to rawTestSetList
        for a in angSetList:
            tempList.extend(lenList[:])
            tempList.extend(a[:])
            rawTestSetList.append(tempList[:])
            tempList.clear()

    elif targetParam == 1:       # 1: only bond lengthes to be scaned
        for l in lenSetList:
            tempList.extend(l[:])
            tempList.extend(angList[:])
            rawTestSetList.append(tempList[:])
            tempList.clear()
    elif targetParam == 2:       # 2: only bond angles to be scaned
        for a in angSetList:
            tempList.extend(lenList[:])
            tempList.extend(a[:])
            rawTestSetList.append(tempList[:])
            tempList.clear()
    else:
        file_out.wirte("\nwhichParam specification mistake: 0 1 2 3 alowed only.")
        quit()

    testSetList = []
    
    for t in rawTestSetList:
        isAllPositive = True
        for d in t:
            if d <= 0:
                isAllPositive = False
        if isAllPositive == True:
            testSetList.append(t[:])
            

    return testSetList

# iteration method
def iterateWithMinima(
    inheritMode: int,       # inheritMode:
                            #       1: always retain parameters with local Minima
                            #       0: no Minima, each test is independent
    targetParam: int,       # targetParam:
                            #       Used in testSetGenerate(...)
                            #       0: both bond lengthes and angles to be scaned
                            #       1: only bond lengthes to be scaned
                            #       2: only bond angles to be scaned
                            #       also used to generate targetSetList
    lenList: list,          # lenList: list of bond lengthes, used to generate targetSetList
    lenSteps: int,          # lenSteps: No. scan steps for bond lengthes, used to generate targetSetList
    lenPerStep: float,      # lenPerStep: scan step size for bond lengthes, used to generate targetSetList
    angList: list,          # angList: list of bond angles, used to generate targetSetList
    angSteps: int,          # angSteps: No. scan steps for bond angles, used to generate targetSetList
    angPerStep: float,      # angPerStep: scan step size for bond angles, used to generate targetSetList
    rootWorkPath: str,      # work folder
    outputName: str         # output file name
    ):
        # meaning of section in the following notation:
    #       in a bond len & ang list, the number of data being iterated.
    
    # get testSetList
    testSetList = testSetGenerate(targetParam, lenList, lenSteps, lenPerStep, angList, angSteps, angPerStep, outputName)

    # open file for output
    file_out = open(outputName, 'a')

    # Minima and test data list in all test sets.
    global_min_diffSum = 9999.9999
    global_min_diffSumTest = []
    global_min_absDiffSum = 9999.9999
    global_min_absDiffSumTest = []

    # Minima and test data list in current section
    local_min_diffSum = 9999.9999
    local_min_diffSumTest = []
    local_min_absDiffSum = 9999.9999
    local_min_absDiffSumTest = []

    testCountFlag = 0           # total number of tests
    actualTestCountFlag = 0     # total number of tests been ran

    # size of each section: how many tests in each section ?
    section_size = lenSteps * 2 + 1
    
    # flags for section notation, relating to current_section_flag in the loop. 
    current_section_flag = 0                    # this flag notes the position of data in each list being processed
    actual_run_number_flag = 0                  # this flag notes the No. of section actually been processed

    if targetParam == 2:
        current_section_flag += len(lenList)
    else:
        pass

    last_section_flag = current_section_flag    # this flag notes the position of data in each list already processed

    # test start
    for i in range(0, len(testSetList)):
        
        # current_section_flag determines in which section is testSetList[i], 
        # it retains the position(int) of data (in the list testSetList[i]/test) under iteration in this section.
        if actual_run_number_flag < i // section_size:
            current_section_flag += 1
            actual_run_number_flag += 1

        # UPON SWITCHING SECTIONS:
        # last_section_flag != current_section_flag: section completed:
        # at this stage: test[last_section_flag] has done iteration, test[current_section_flag] is the section will be iterated in the next run
        # decide if data producing local Minima should be inherited, see inheritMode for ref.
        # modify for inheritance: note that all testlist t in testset is modified, 
        # but iteration will NOT go back, so output under influence are sections afterwards.
        if last_section_flag != current_section_flag:   # LINE 226 ensures this if would not be called at i == 0
            if inheritMode == 0:                        # inheritMode = 0: each section run independently, no inheritance between section.
                pass
            elif inheritMode == 1:                      # inheritMode = 1: section should inherit data that produces lowest local lenDiffSum.
                for t in testSetList:
                    t[last_section_flag] = local_min_diffSumTest[last_section_flag]
            else:
                file_out.write("\nwhichMinima specification mistake: 0 1 2 3 alowed only.")
                quit()
            
            # section completed & upon switching section:
            # reset local Minima recorders & update section flag
            last_section_flag = current_section_flag
            local_min_diffSum = 9999.9999
            local_min_absDiffSum = 9999.9999
            local_min_diffSumTest = []

        test = testSetList[i]                       # get test for run
        testCountFlag +=1                           # tests no. flag
        diffSum, absDiffSum = doTest(rootWorkPath, test)        # difference summation of qm & mm frequencies 
        actualTestCountFlag += 1                    # tests ran no. flag
        
        # retain global Minima for lenDiff & angDiff, test input as well.
        if diffSum <= global_min_diffSum:
            global_min_diffSum = diffSum
            global_min_diffSumTest = test[:]
        elif absDiffSum <= global_min_absDiffSum:
            global_min_absDiffSum = absDiffSum
            global_min_absDiffSumTest = test[:]
        else:
            pass

        # last_section_flag == current_section_flag: iteration still goes in 1 section:
        # retain local Minimas and for lenDiff & angDiff, relevant test data as well
        if diffSum <= local_min_diffSum:
            local_min_diffSum = diffSum
            local_min_diffSumTest = test[:]
        elif absDiffSum <= local_min_absDiffSum:
            local_min_absDiffSum = absDiffSum
            local_min_absDiffSumTest = test[:]
        else:
            pass

        file_out.write("{0}\t{1}\t|globalMin: {2:0<8.6f} abs:{3:0<8.6f}\t|localMin: {4:0<8.6f} abs:{5:0<8.6f}\t|crtDiff: {6:0<8.6f} abs:{7:0<8.6f}\t|testDat:{8}\n".format(
                i, current_section_flag, global_min_diffSum, global_min_absDiffSum, local_min_diffSum, local_min_absDiffSum, diffSum, absDiffSum, test
        ))
        file_out.flush()
    
    file_out.close()

    return testCountFlag, actualTestCountFlag, global_min_diffSum, global_min_diffSumTest, global_min_absDiffSum, global_min_absDiffSumTest

# use CHARMM & python to do test, return result
def doTest(
    rootWorkPath: str, 
    test: list
    ):

    # copy a new force field file
    subp.call('cp -r {0}/frg5.strm.original {0}/frg5.strm'.format(rootWorkPath), shell=True)
    
    # modify the parameters in the force field file
    subp.call("sed -i -e 's/CG2R53 NG321   330.00     1.3650/CG2R53 NG321   {0:>6.2f}     1.3650/g' frg5.strm".format(test[0]), shell=True)
    subp.call("sed -i -e 's/NG2R50 CG2R53 NG321    45.80    129.20/NG2R50 CG2R53 NG321   {0:>6.2f}    129.20/g' frg5.strm".format(test[1]), shell=True)
    subp.call("sed -i -e 's/NG321  CG2R53 SG2R50   25.00    119.80/NG321  CG2R53 SG2R50  {0:>6.2f}    119.80/g' frg5.strm".format(test[2]), shell=True)
    subp.call("sed -i -e 's/CG2R53 NG321  HGPAM2   45.00    117.20/CG2R53 NG321  HGPAM2  {0:>6.2f}    117.20/g' frg5.strm".format(test[3]), shell=True)
    

    # execute CHARMM script, will produce a output of log.mm. shell ensures the workflow does not return before CHARMM script finish.
    subp.call('/users/zilins/software/mpi.charmm/exec/gnu_M/charmm -i vib_freq.inp -o log.mm', shell=True)

    # execute python script, will produce a output of freq.ene. Also takes a input log.mm, which was produced by CHARMM.
    subp.call('python vibfreq.extract.py', shell=True)
    
    diffSum = -999.99
    diffSum_abs = -999.99

    # read result
    for line in open("freq.ene"):
        words = line.split()
        if words[0] == "&&":
            diffSum = float(words[2])
            diffSum_abs = float(words[4])
        else:
            pass
    
    return abs(diffSum), diffSum_abs


# main
def main():

    # origin from which test sets will be built
    len_target_list = [330.00]
    ang_target_list = [45.80, 25.00, 45.00]
    
    inheritMode = 0     # inheritMode specification:
                        #       0: no param inheritance, each test goes independent
                        #       1: always inherit params with local Minima
                        
    targetParam = 0     # targetParam specification:
                        #       0: both bond lengthes and angles force constant to be scaned
                        #       1: only bond lengthes force constant to be scaned
                        #       2: only bond angles force constant to be scaned
    
    # scan criterias: perstep variables must be float 
    len_steps = 1000
    len_perstep = 1
    ang_steps = 1000
    ang_perstep = 0.1

    # specify directories
    workFolder = "result.init/case_{0}{1}".format(inheritMode, targetParam)                         # folder name where all tests are done (critical to provide an unused folder name)
    workPath = "/users/zilins/scratch/forcefielddev/1.cephalosporins/0.fragmets/4.frg5/3.freq"      # directory where workFolder & sourceFolder locates / absolute directory in the file system
    qmSourceFolder = workPath + "/scripting.0.charmm.vib_freq_qm.inp"                               # folder name where relevent files exists
    mmSourceFolder = workPath + "/scripting.1.charmm.vib_freq.inp"                                  # same
    pySourceFolder = workPath + "/scripting.2.py.vibfreq.extract"                                   # same
    outputName = "vibfreq.scan.py.out"                                                              # output file name
    
    # rootWorkPath: absolute directory in system to locate work folder
    rootWorkPath = "{0}/{1}".format(workPath, workFolder)

    # ready the test 
    initialize(rootWorkPath, mmSourceFolder, qmSourceFolder, pySourceFolder)

    # write header in output file
    writeHeader(outputName, len_target_list, len_steps, len_perstep, ang_target_list, ang_steps, ang_perstep)

    # do scan
    totalCase, actualTotalCase, global_min_diffSum, global_min_diffSumTest, global_min_absDiffSum, global_min_absDiffSumTest= iterateWithMinima(
        inheritMode, targetParam, len_target_list, len_steps, len_perstep, ang_target_list, ang_steps, ang_perstep, rootWorkPath, outputName
    )

    # write summary in output file
    writeSummary(outputName, global_min_diffSum, global_min_diffSumTest, global_min_absDiffSum, global_min_absDiffSumTest, totalCase, actualTotalCase)

if __name__ == "__main__":
    main()