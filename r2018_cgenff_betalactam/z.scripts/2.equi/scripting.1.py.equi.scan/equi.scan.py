# equilibrium bond length & angle test for cephalosporins.
# NOTE:
#       Initial Test
# This script would:
#       1. Generate a output directory at father directory.
#       2. Copy the relevant files to output directory
#       3. Do charge scan.
#       4. Note that, 
#           the doTest() method should be altered regarding to the interested system.
# NOTE: the scan principle of bond length & angle is different from charge: 
#               paramters are independent to each other 
#               in charge, the total charge must REMAIN unchanged
# NOTE: this script defaultly considers lengthes presents before angles in each test list:
#            testSetGenerate() 
# 
# too much parameters in main() so that this script is suggested reading carefully before run.
# 
# Zilin Song, 16 JAN 2O18
# 

import subprocess as subp
import sys
import os

# establish working directory structure/ copy charmm files/ ready force field file.
def initialize(
    realWorkPath: str, 
    sourceFolder: str
    ):

    # establish working path directory structure & files
    subp.call('mkdir -p {0}'.format(realWorkPath), shell=True)
    subp.call('mkdir -p {0}/forcefield'.format(realWorkPath), shell=True)
    subp.call('cp {0}/frg5.hfmini.crd {1}/.'.format(sourceFolder, realWorkPath), shell=True)
    subp.call('cp {0}/frg5.strm {1}/frg5.strm.original'.format(sourceFolder, realWorkPath), shell=True)
    subp.call('cp {0}/equi_quick.inp {1}/.'.format(sourceFolder, realWorkPath), shell=True)
    subp.call('cp {0}/forcefield/*_all36_cgenff.* {1}/forcefield/.'.format(sourceFolder, realWorkPath), shell=True)
    subp.call('cp {0}/forcefield/*.str {1}/forcefield/.'.format(sourceFolder, realWorkPath), shell=True)

    # enter work directory
    os.chdir(realWorkPath)
    
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
    file_out.write("Equilibrium bonding angle & length scan for force field development.\nZilin Song, scripted on 17 Dec 2018.\n\nJob description:\n\n")
    file_out.write("Bond Lengthes:\t{0}\nScan Steps:\t{1}\nStep Size (A):\t{2}\nBond Length set:\t{3}\n\n".format(len(lenList), lenSteps, lenPerStep, lenList))
    file_out.write("Bond Angles:\t{0}\nScan Steps:\t{1}\nStep Size (D):\t{2}\nBond Length set:\t{3}\n\n".format(len(angList), angSteps, angPerStep, angList))
    file_out.write("Original test Set:\t{0}\n\nScan Start.\n\n".format(originSet))
    file_out.flush()

    #done
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

    # target testSetList generation method:
    #       not tolal combination for all circumstances
    #       lenList.extend(angList) as original list: 
    #       testSetList only change the member in the original list, one at a time in test range
    #       test range: {original[i] - lenSteps * lenPerStep, original[i] + lenSteps * lenPerStep}

    testSetList = []        # target testSetList to be generated

    # sets that contains all length & angles: 
    # seperated because len & ang could have different step size & step count
    lenSetList = []
    angSetList = []
    
    # buffer list
    tempList = []
    
    # lenSetList or angSetList:
    # partial testSetList within length list or angle list

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
        # extent each list in lenSetList with original angle list, append extended list to testSetList
        for l in lenSetList:
            tempList.extend(l[:])
            tempList.extend(angList[:])
            testSetList.append(tempList[:])
            tempList.clear()

        # extent original length list with angSetList, append extended list to testSetList
        for a in angSetList:
            tempList.extend(lenList[:])
            tempList.extend(a[:])
            testSetList.append(tempList[:])
            tempList.clear()

    elif targetParam == 1:       # 1: only bond lengthes to be scaned
        for l in lenSetList:
            tempList.extend(l[:])
            tempList.extend(angList[:])
            testSetList.append(tempList[:])
            tempList.clear()
    elif targetParam == 2:       # 2: only bond angles to be scaned
        for a in angSetList:
            tempList.extend(lenList[:])
            tempList.extend(a[:])
            testSetList.append(tempList[:])
            tempList.clear()
    else:
        file_out.wirte("\nwhichParam specification mistake: 0 1 2 3 alowed only.")
        quit()

    return testSetList

# iteration method
def iterateWithMinima(
    inheritMode: int,       # inheritMode:
                            #       1: always retain parameters with bond length Minima
                            #       2: always ...... .......... .... .... angle  ......
                            #       3: when bond length is under test proceed with length Minima, same for angle
                            #       else: no Minima, each test is independent
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
    realWorkPath: str,      # work folder
    outputName: str         # output file name
    ):
    
    # meaning of section in the following notation:
    #       in a bond len & ang list, the number of data being iterated.
    
    # get testSetList
    testSetList = testSetGenerate(targetParam, lenList, lenSteps, lenPerStep, angList, angSteps, angPerStep, outputName)

    # open file for output
    file_out = open(outputName, 'a')

    # Minima and test data list in all test sets.
    global_min_lenDiffSum = 999.9999
    global_min_lenTest = []
    global_min_angDiffSum = 999.9999
    global_min_angTest = []

    # Minima and test data list in current section
    local_min_lenDiff = 999.99
    local_min_lenDiffTest = []
    local_min_angDiff = 999.99
    local_min_angDiffTest = []
    
    testCountFlag = 0           # total number of tests
    actualTestCountFlag = 0     # total number of tests been ran
    
    # size of each section: how many tests in each section ?
    section_size = lenSteps * 2 + 1
    
    # number of length sections, 
    # NOTE length section is always prior to angle section
    len_count = len(lenList)

    # flag for section notation, relating to current_section_flag in the loop. 
    current_section_flag = 0                    # this flag notes the position of data in each list being processed
    actual_run_number_flag = 0                  # this flag notes the No. of section actually been processed

    if targetParam == 2:
        current_section_flag += len_count
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
        # modify for inheritance: NOTE all testlist t in testset is modified, 
        # but iteration will NOT go back, so sections under influence are those afterwards.
        if last_section_flag != current_section_flag:   # LINE 226 ensures this if would not be called at i == 0
            if inheritMode == 0:                        # inheritMode = 0: each section run independently, no inheritance between section.
                pass
            elif inheritMode == 1:                      # inheritMode = 1: section should inherit data that produces lowest local lenDiffSum.
                for t in testSetList:
                    t[last_section_flag] = local_min_lenDiffTest[last_section_flag]
            elif inheritMode == 2:                      # inheritMode = 2: inherit lowest local angDiffSum.
                for t in testSetList:
                    t[last_section_flag] = local_min_angDiffTest[last_section_flag]
            elif inheritMode == 3:                      # inheritMode = 3: inherit lowest local lenDiffSum in length section; angDiffSum / angle.
                if last_section_flag < len_count:         #       length section
                    for t in testSetList:
                        t[last_section_flag] = local_min_lenDiffTest[last_section_flag]
                elif last_section_flag >= len_count:      #       angle section
                    for t in testSetList:
                        t[last_section_flag] = local_min_angDiffTest[last_section_flag]
            else:
                file_out.wirte("\nwhichMinima specification mistake: 0 1 2 3 alowed only.")
                quit()
            
            # section completed & upon switching section:
            # reset local Minima recorders & update section flag
            last_section_flag = current_section_flag
            local_min_lenDiff = 999.99
            local_min_lenDiffTest = []
            local_min_angDiff = 999.99
            local_min_angDiffTest = []
        
        
        test = testSetList[i]
        testCountFlag += 1
        
        # lenDiffSum: summation of length differences from current run
        # angDiffSum: ......... ..  angle ........... .... ....... ...
        lenDiffSum, angDiffSum = doTest(realWorkPath, test)
        actualTestCountFlag += 1
        
        # retain global Minima for lenDiff & angDiff, test input as well.
        if lenDiffSum <= global_min_lenDiffSum:
            global_min_lenDiffSum = lenDiffSum
            global_min_lenTest = test[:]
        if angDiffSum <= global_min_angDiffSum:
            global_min_angDiffSum = angDiffSum
            global_min_angTest = test[:]

        # last_section_flag == current_section_flag: iteration still goes in 1 section:
        # retain local Minimas and for lenDiff & angDiff, relevant test data as well
        if lenDiffSum <= local_min_lenDiff:
            local_min_lenDiff = lenDiffSum
            local_min_lenDiffTest = test[:]
        if angDiffSum <= local_min_angDiff:
            local_min_angDiff = angDiffSum
            local_min_angDiffTest = test[:]

        
        #file_out.write("{0}\t{1}\t{2:0<8.6f}\t{3:0<8.6f}\t|\t{5:0<8.6f}\t{6:0<8.6f}\t|\t{4}\n".format(last_section_flag, current_section_flag, local_min_angDiff, local_min_lenDiff, test, angDiffSum, lenDiffSum))
        # write current step to file_out
        file_out.write("{0}\t{1}\t|globalMin: sumLen: {2:0<8.6f}\tsumAng: {3:0<8.6f}\t|localMin:  sumLen: {4:0<8.6f}\t sumAng: {5:0<8.6f}\t|crtDiff: sumLen: {6:0<8.6f}\tsumAng: {7:0<8.6f}|\ttestDat:{8}\n".format(
                i, current_section_flag, global_min_lenDiffSum, global_min_angDiffSum, local_min_lenDiff, local_min_angDiff, lenDiffSum, angDiffSum, test
        ))
        file_out.flush()

    file_out.close()

    return testCountFlag, actualTestCountFlag, global_min_lenDiffSum, global_min_lenTest, global_min_angDiffSum, global_min_angTest

# use CHARMM to do test & obtain result
def doTest(
    realWorkPath: str, 
    test: list
    ):

    # copy a new force field file
    subp.call('cp {0}/frg5.strm.original {1}/frg5.strm'.format(realWorkPath, realWorkPath), shell=True)
    
    # modify the parameters in the force field file
    subp.call("sed -i -e 's/CG2R53 NG321   330.00     1.4000/CG2R53 NG321   330.00     {0:5.4f}/g' frg5.strm".format(test[0]), shell=True)
    subp.call("sed -i -e 's/NG2R50 CG2R53 NG321    45.80    123.00/NG2R50 CG2R53 NG321    45.80    {0:5.2f}/g' frg5.strm".format(test[1]), shell=True)
    subp.call("sed -i -e 's/NG321  CG2R53 SG2R50   25.00    119.80/NG321  CG2R53 SG2R50   25.00    {0:5.2f}/g' frg5.strm".format(test[2]), shell=True)
    subp.call("sed -i -e 's/CG2R53 NG321  HGPAM2   45.00    115.00/CG2R53 NG321  HGPAM2   45.00    {0:5.2f}/g' frg5.strm".format(test[3]), shell=True)
    
    # execute CHARMM script, will produce a output of frg5_bond.ene. shell ensures the workflow does not return before CHARMM script finish.
    subp.call('/users/zilins/software/mpi.charmm/exec/gnu_M/charmm -i equi_quick.inp -o log', shell=True)
    
    # used to record lenDiff/angDiff values
    lenDiffList = []
    angDiffList = []
    
    # read result
    for line in open("frg5_bond.ene"):
        words = line.split()
        if words[0] == 'AN':
            angDiffList.append(float(words[7]))
        elif words[0] == 'LE':
            lenDiffList.append(float(words[7]))
    
    # calc lenDiffSum 
    lenDiffSum = 0
    for leDiff in lenDiffList:
        lenDiffSum += round(abs(leDiff), 4)

    # calc angDiffSum 
    angDiffSum = 0
    for anDiff in angDiffList:
        angDiffSum += round(abs(anDiff), 4)
        
    return lenDiffSum, angDiffSum

# write summary in the output
def writeSummary(
    outputName: str, 
    global_min_lenDiffSum: float, 
    global_min_lenTest: list, 
    global_min_angDiffSum: float, 
    global_min_angTest: list, 
    totalCase: int,
    actualTotalCase: int
    ):
    file_out = open(outputName, 'a')

    file_out.write("\n\n===== Scan Done =====\n\nResult:\n\n")
    file_out.write("min bond len sum: {0:0<8.6f}\nparams: {1}\n\n".format(global_min_lenDiffSum, global_min_lenTest))
    file_out.write("min bond ang sum: {0:0<8.6f}\nparams: {1}\n\n".format(global_min_angDiffSum, global_min_angTest))
    file_out.write("Total case count: {0}\nCase been processed: {1}".format(totalCase, actualTotalCase))
    file_out.flush()
    file_out.close()

# main
def main():
    
    # origin from which test sets will be built
    len_target_list = [1.365]
    ang_target_list = [129.3, 119.80, 117.20]
    
    inheritMode = 3     # inheritMode specification:
                        #       0: no param inheritance, each test section is independent
                        #       1: always inherit params with bond length Minima
                        #       2: always inherit params with bond angle Minima
                        #       3: when bond length is under test, retain params with length Minima, same for bond angle

    targetParam = 2     # targetParam specification:
                        #       0: both bond lengthes and angles to be scaned
                        #       1: only bond lengthes to be scaned
                        #       2: only bond angles to be scaned

    # scan criterias: perstep variables must be float 
    len_steps = 100
    len_perstep = 0.005
    ang_steps = 100
    ang_perstep = 0.1

    # specify directories
    workFolder = "test.medium/case_{0}{1}".format(inheritMode, targetParam)                    # folder name where all tests are done (critical to provide an unused folder name)
    sourceFolder = "scripting.0.charmm.equi_quick.inp"                                          # folder name where all relevent files exists
    outputName = "equi.scan.py.out"                                                             # output file name
    workPath = "/scratch/users/zilins/forcefielddev/1.cephalosporins/0.fragmets/4.frg5/2.equi/" # directory where workFolder & sourceFolder locates / absolute directory in the file system

    # realWorkPath: absolute directory in system to locate work folder
    realWorkPath = "{0}/{1}".format(workPath, workFolder)
    realSourcePath = "{0}/{1}".format(workPath, sourceFolder)

    # ready the test 
    initialize(realWorkPath, realSourcePath)

    # write header in output file
    writeHeader(outputName, len_target_list, len_steps, len_perstep, ang_target_list, ang_steps, ang_perstep)

    # do scan
    totalCase, actualTotalCase, global_min_lenDiffSum, global_min_lenTest, global_min_angDiffSum, global_min_angTest = iterateWithMinima(
        inheritMode, targetParam, len_target_list, len_steps, len_perstep, ang_target_list, ang_steps, ang_perstep, realWorkPath, outputName
    )

    # write summary in output file
    writeSummary(outputName, global_min_lenDiffSum, global_min_lenTest, global_min_angDiffSum, global_min_angTest, totalCase, actualTotalCase)

if __name__ == "__main__":
    main()

# NOTE: 
#   do not modify iterateWithMinima() loop.
#   write your own scan method and replace relevant code in main().
#   That method is TRICKY !!!