from clingo import *
from amalgamation.settings import *
from amalgamation.langCasl import *
from amalgamation import hets_helper


def findLeastGeneralizedBlends(modelAtoms, inputSpaces, highestValue, blends):
    global blendValuePercentageBelowMinToKeep
    # generalizationCost = float("inf")
    if highestValue == -float("inf"):
        minBlendValueToConsider = -float("inf")
    else:
        minBlendValueToConsider = highestValue - int(
            float(highestValue) / float(100) * float(blendValuePercentageBelowHighestValueToKeep))

    # Parse model and execute actions on internal data structure to obtain the generalized inut spaces. 
    genInputSpaces = getGeneralizedSpaces(modelAtoms, inputSpaces)

    # print("specs:")
    # print(genInputSpaces.keys())
    # for specTypeList in genInputSpaces.values():
    #     for spec in specTypeList:
    #         print(spec.toCaslStr())

    # # Get possible combinations of generalization combinations
    blendCombis = getBlendCombiCost(genInputSpaces)

    # # initialize output string for casl file
    cstr = ''

    # # First state generic spaces
    cstr = cstr + genInputSpaces["Generic"][0].toCaslStr() + "\n\n"

    # State the mappings with inheritance        
    for specName in genInputSpaces.keys():
        if specName == "Generic":
            continue

        for spec in genInputSpaces[specName]:

            specStr = spec.toCaslStr() + "\n\n"

            mappingStr = ""
            mappingStr = mappingStr + "view GenTo" + spec.name + " : Generic to " + spec.name + " \n"
            specTo = spec
            specFrom = genInputSpaces["Generic"][0]
            renamings = getRenamingsFromModelAtoms(modelAtoms, specFrom, specTo, specName)
            # print(mappingStr)
            # print(renamings)

            if len(renamings.keys()) > 0:
                mappingStr += " =  "
                for step in sorted(renamings.keys()):
                    mappingStr = mappingStr + lpToCaslStr(renamings[step][1]) + " |-> " + lpToCaslStr(
                        renamings[step][0]) + ", "
                mappingStr = mappingStr[:-2]

                # print(act)
                # if atom.find("exec(renameOp(") != -1:
                # atomSpec =
            mappingStr = mappingStr + " end\n\n"
            cstr += specStr + mappingStr

    # raw_input()
    # State blends (colimit operation)
    for value in sorted(blendCombis.keys(), reverse=True):
        if value < minBlendValueToConsider:
            continue
        print("Specifying blends with generalization value of " + str(value))
        for combi in blendCombis[value]:
            cstr = cstr + "spec Blend" + "_v" + str(value) + "_"
            for specName in combi.keys():
                steps = combi[specName]
                cstr = cstr + "_" + lpToCaslStr(specName) + "_" + str(steps)
            cstr = cstr + " = combine "

            for specName in combi.keys():
                caslSpecName = lpToCaslStr(specName)
                specList = genInputSpaces[caslSpecName]
                # print(specName)
                # print(combi)
                # print(int(combi[specName]))
                # print(len(specList))
                specStep = int(combi[specName])
                spec = specList[specStep]
                cstr = cstr + "GenTo" + spec.name + ","
            cstr = cstr[:-1]
            cstr = cstr + " end\n\n"

    amalgam_tmp_filepath = "/data/amalgam_tmp.casl"
    outFile = open(amalgam_tmp_filepath, "w")
    outFile.write(cstr)
    outFile.close()

    if not os.path.isfile(amalgam_tmp_filepath):
        raise Exception(f'could not write file {amalgam_tmp_filepath}')
    # raw_input()

    generalizationValue = -float("inf") - 1
    consistentFound = False
    for value in sorted(blendCombis.keys(), reverse=True):

        print("Trying blends with generalization value of " + str(value))
        if value < minBlendValueToConsider:
            print("value " + str(value) + " < " + str(minBlendValueToConsider) + " too low, aborting...")
            break

        # TODO: do not blend if generic space is reached. 
        # isBestBlendCost = False
        for combi in blendCombis[value]:
            # thisCombiConsistent = -1
            blendName = "Blend" + "_v" + str(value) + "_"
            for specName in combi.keys():
                step = combi[specName]
                blendName = blendName + "_" + lpToCaslStr(specName) + "_" + str(step)
            # blendName += "-v"+str(value)

            print("Checking consistency of " + blendName + "")
            # generate tptp format of theory and call eprover to check consistency
            
            ###TBD call HETS API
            amalgam_tmp_file = open(amalgam_tmp_filepath, 'rb')
            tptp_files = hets_helper.generate_tptp_files_from(amalgam_tmp_file)
            print("Done generating tptp")

            blendTptpName = "/data/amalgam_tmp_" + blendName + ".tptp"
            blend_tptp_file = list(filter(lambda file: file.name == blendTptpName, tptp_files))[0]

            print(blend_tptp_file.name)

            thisCombiConsistent = checkConsistency(blend_tptp_file.name)
            # skip tptp generation and consitency checking because tptp file creation with hets is buggy
            # thisCombiConsistent = 1

            # if thisCombiConsistent == 1: # If we can show that the blend is consistent
            if thisCombiConsistent != 0:  # If we can not show that the blend is inconsistent

                prettyBlendStr = prettyPrintBlend(genInputSpaces, combi, modelAtoms)
                blendInfo = {"combi": combi, "prettyHetsStr": prettyBlendStr, "blendName": blendName,
                             "generalizationValue": value}

                # consistentFound = True
                # If a better blend was found, delete all previous blends. 
                if value > highestValue:
                    # print('tptpfile name is '+blendTptpName;)

                    highestValue = value
                    minBlendValueToConsider = highestValue - int(
                        float(highestValue) / float(100) * float(blendValuePercentageBelowHighestValueToKeep))
                    print("New best value: " + str(
                        value) + ". Resetting global list of blends and keeping only blends with a value of at least " + str(
                        minBlendValueToConsider) + ", i.e., " + str(
                        blendValuePercentageBelowHighestValueToKeep) + "% below new highest value of " + str(
                        highestValue) + ".")
                    newBlends = []
                    # raw_input()
                    for blend in blends:
                        if blend['generalizationValue'] >= minBlendValueToConsider:
                            newBlends.append(blend)
                    blends = newBlends

                blends.append(blendInfo)

    # os.system("rm -rf *.tptp")
    # os.remove("/data/amalgam_tmp.casl")

    return [blends, highestValue]


def prettyPrintBlend(genInputSpaces, combi, modelAtoms):
    print("Pretty printing blend")

    lastSpecs = {}

    # state generic space
    cstr = genInputSpaces["Generic"][0].toCaslStr() + "\n\n"

    # initiate blend spec string
    blendStr = "spec Blend = combine "
    for iSpaceName in genInputSpaces.keys():
        if iSpaceName == "Generic":
            continue
        lastSpecName = ''
        lastSpec = None
        numGeneralizations = 0

        for spec in genInputSpaces[iSpaceName]:
            cstr += "%% Spec values: \n%% Information value: "
            cstr += str(spec.infoValue)
            cstr += "\n%% Compression value: "
            cstr += str(spec.compressionValue) + "\n"

            cstr += spec.toCaslStr() + "\n\n"
            # define view to previous spec. 
            viewToPrevSpecStr = ''
            if lastSpecName != '':
                viewToPrevSpecStr = "view " + spec.name + "To" + lastSpecName + " : " + spec.name + " to " + lastSpecName
                renamings = getRenamingsFromModelAtoms(modelAtoms, spec, lastSpec, iSpaceName)
                if len(renamings.keys()) > 0:
                    viewToPrevSpecStr += " =  "
                    for step in sorted(renamings.keys()):
                        renameFrom = lpToCaslStr(renamings[step][1])
                        renameTo = lpToCaslStr(renamings[step][0])
                        viewToPrevSpecStr += renameFrom + " |-> " + renameTo + ", "
                    viewToPrevSpecStr = viewToPrevSpecStr[:-2]
                viewToPrevSpecStr += " end \n\n"
                cstr += viewToPrevSpecStr

            lastSpecName = spec.name
            lastSpec = spec
            # The most general input space has been found
            if numGeneralizations == combi[toLPName(iSpaceName, "spec")]:
                # view from generic space to generalized input space:
                cstr = cstr + "view GenTo" + lastSpecName + " : Generic to " + lastSpecName
                specFrom = genInputSpaces["Generic"][0]
                renamings = getRenamingsFromModelAtoms(modelAtoms, specFrom, spec, iSpaceName)
                if len(renamings.keys()) > 0:
                    cstr = cstr + " =  "
                    for step in sorted(renamings.keys()):
                        cstr = cstr + lpToCaslStr(renamings[step][1]) + " |-> " + lpToCaslStr(renamings[step][0]) + ", "
                    cstr = cstr[:-2]

                cstr += " end \n\n"
                # Specify blend
                blendStr = blendStr + "GenTo" + spec.name + ","
                break
            numGeneralizations = numGeneralizations + 1

    blendStr = blendStr[:-1] + " end\n\n"

    cstr = cstr + blendStr

    print("End Pretty printing blend")

    return cstr


def writeJsonOutput(blends, inputSpaceNames):
    jsonOutput = {}
    jsonOutput['blendList'] = []

    print(inputSpaceNames)
    blendNr = 1
    for blend in blends:
        jsonBlend = {}

        blendStr = blend['prettyHetsStr']
        print('Blend' + str(blendNr))

        genericSpacePattern = "(spec\sGeneric.*?end)"
        jsonBlend['blendId'] = str(blendNr)
        jsonBlend['blendName'] = blend['blendName']
        jsonBlend['cost'] = blend['generalizationValue']
        match = re.search(genericSpacePattern, blendStr, re.DOTALL)
        jsonBlend['genericSpace'] = match.group(0)

        # 'combi': {'spec_G7': 1, 'spec_Bbmin': 3}
        # G7_gen_1
        combi = blend['combi']
        # ['G7', 'Bbmin']
        inputSpaceNr = 1
        for inputSpaceName in inputSpaceNames:
            inputSpace = inputSpaceName
            if combi[toLPName(inputSpace, 'spec')] > 0:
                genSpaceName = '_' + 'gen' + '_' + str(combi[toLPName(inputSpace, 'spec')])
            else:
                genSpaceName = ''
            print('TETEET:' + genSpaceName)
            genericSpacePattern = "(spec\s" + inputSpace + "(?=)" + genSpaceName + ".*?end)"

            match = re.search(genericSpacePattern, blendStr, re.DOTALL)

            jsonBlend['input' + str(inputSpaceNr)] = match.group(0)

            inputSpaceNr = inputSpaceNr + 1

        jsonBlend['blend'] = generateBlend(blend)
        jsonOutput['blendList'].append(jsonBlend)
        blendNr = blendNr + 1

    return jsonOutput


# This function takes a list of blend speciications and writes them to disk.
def generateBlend(blend):
    # os.system("rm -rf Blend_*.casl")
    # os.system("rm -rf Blend_*.th")
    bNum = 0
    blendFilesList = ''

    blendStr = blend["prettyHetsStr"]
    fName = f'/data/{blend["blendName"]}_b_{str(bNum)}.casl'
    outFile = open(fName, "w")
    outFile.write(blendStr)
    outFile.close()

    blend_casl_file = open(fName, 'r')
    th_files = hets_helper.generate_th_files_from(blend_casl_file)
    blend_node_th_filename = f'/data/{hets_helper.get_generic_filename_for(blend_casl_file)}_Blend.th'
    blend_node_th_file = list(filter(lambda file: file.name == blend_node_th_filename, th_files))[0]

    explicitBlendStr = blend_node_th_file.read()
    blend_node_th_file.close()
    # remove first two lines and rename explicit blend spec
    lineBreakPos = explicitBlendStr.find("\n")
    explicitBlendStr = explicitBlendStr[lineBreakPos + 1:]
    lineBreakPos = explicitBlendStr.find("\n")
    explicitBlendStr = explicitBlendStr[lineBreakPos + 1:]
    explicitBlendStr = "\n\n\nspec BlendExplicit = \n" + explicitBlendStr + "\n end\n"

    outFile = open(fName, "r")
    fullBlendStr = outFile.read()
    outFile.close()

    fullBlendStr = fullBlendStr + explicitBlendStr

    outFile = open(fName, "w")
    outFile.write(fullBlendStr)
    outFile.close()

    # os.system("cp " + thName + " " + thName[:-3]+".casl")
    # os.system("rm -rf *.th")
    # blendFilesList += thName[:-3]+".casl\n"
    blendFilesList += fName

    bNum = bNum + 1

    # raw_input
    fileListFile = open("/data/blendFiles.txt", "w")
    fileListFile.write(blendFilesList)
    fileListFile.close()
    return explicitBlendStr


# This function takes a list of blend speciications and writes them to disk.
def writeBlends(blends):
    global genExplicitBlendFiles
    # raw_input
    # os.system("rm -rf Blend_*.casl")
    # os.system("rm -rf Blend_*.th")
    bNum = 0
    blendFilesList = ''
    for blend in blends:

        blendStr = blend["prettyHetsStr"]
        fName = blend["blendName"] + "_b_" + str(bNum) + ".casl"
        outFile = open(fName, "w")
        outFile.write(blendStr)
        outFile.close()
        tries = 0
        while True:
            ### call HETS API
            subprocess.call([hetsExe, "-o th", fName])
            thName = fName[:-5] + "_Blend.th"
            thFileSize = 0
            if os.path.isfile(thName):
                thFileSize = os.stat(thName).st_size

            if tries > 15:
                print("ERROR: file " + thName + " not yet written in " + str(tries) + " times ! Aborting...")
                exit(1)
            tries = tries + 1

            if thFileSize != 0:
                break

        blend_node_th_file = open(thName, "r")
        explicitBlendStr = blend_node_th_file.read()
        blend_node_th_file.close()
        # remove first two lines and rename explicit blend spec
        lineBreakPos = explicitBlendStr.find("\n")
        explicitBlendStr = explicitBlendStr[lineBreakPos + 1:]
        lineBreakPos = explicitBlendStr.find("\n")
        explicitBlendStr = explicitBlendStr[lineBreakPos + 1:]
        explicitBlendStr = "\n\n\nspec BlendExplicit = \n" + explicitBlendStr + "\n end\n"

        outFile = open(fName, "r")
        fullBlendStr = outFile.read()
        outFile.close()

        fullBlendStr = fullBlendStr + explicitBlendStr

        outFile = open(fName, "w")
        outFile.write(fullBlendStr)
        outFile.close()

        if genExplicitBlendFiles == True:
            os.system("cp " + thName + " " + thName[:-3] + ".casl")
            # os.system("rm -rf *.th")
            blendFilesList += thName[:-3] + ".casl\n"

        # blendFilesList += fName

        bNum = bNum + 1

    # raw_input
    if genExplicitBlendFiles == True:
        fileListFile = open("blendFiles.txt", "w")
        fileListFile.write(blendFilesList)
        fileListFile.close()


# Returns an array of possible Blend combinations and provides a blend value for the combination
def getBlendCombiCost(genInputSpaces):
    # combis maps costs to a list of combinations of generalised input spaces.
    combis = {}
    for specName1 in genInputSpaces.keys():
        if specName1 == "Generic":
            continue
        for specName2 in genInputSpaces.keys():
            if specName2 == "Generic":
                continue
            if specName1 == specName2:
                continue
            # print("specs: " + specName1 + specName2)

            gs1Ctr = 0
            for genSpace1 in genInputSpaces[specName1]:
                gs2Ctr = 0
                for genSpace2 in genInputSpaces[specName2]:
                    combi = {}
                    combi[toLPName(specName1, "spec")] = gs1Ctr
                    combi[toLPName(specName2, "spec")] = gs2Ctr
                    informationValue = genSpace1.infoValue + genSpace2.infoValue
                    compressionValue = genSpace1.compressionValue + genSpace2.compressionValue
                    balancePenalty = int(abs(genSpace1.infoValue - genSpace2.infoValue) / 2)
                    value = compressionValue + informationValue - balancePenalty
                    if value not in combis.keys():
                        combis[value] = []
                    combis[value].append(copy.deepcopy(combi))
                    # print(value)
                    gs2Ctr = gs2Ctr + 1
                gs1Ctr = gs1Ctr + 1
        # TODO: This only works for two input spaces.
        # Have to break here, because otherwise blends will be specified twice. I.e., the combi S1_5 and S2_3 plus the combi S2_3 and S1_5 will be produced.
        break
    # print("combis:")
    # print(combis[-30])
    # exit(1)
    return combis


# Returns an array of possible Blend combinations and provides a generalization cost value for the combination
# def getPossBlendCombis(modelAtoms):
#     # maxGeneralizationsPerSpace = 0
#     combis = {}
#     for atom in modelAtoms:
#         if str(atom).find("combinedGenCost") != 0:
#             continue
#         # combi is a pair of generalised specification names
#         combi = {}
#         # combinedGenCost(spec_Boat,6,spec_House,2,38,7).
#         argItems = str(atom).split("(")[1].split(")")[0].split(",")
#         # print(argItems)
#         combi[argItems[0]] = int(argItems[1])-1
#         combi[argItems[2]] = int(argItems[3])-1
#         # cost is the cost of the combination
#         cost = int(argItems[4])
#         if cost not in combis.keys():
#             combis[cost] = []
#         if combi not in combis[cost]:
#             combis[cost].append(combi)
#     return combis

def checkConsistency(blendTptpName):
    consistent = checkConsistencyEprover(blendTptpName)

    # if consistent == -1:
        # print("Consistency could not be determined by eprover, trying darwin")
        # consistent = checkConsistencyDarwin(blendTptpName)
        # if consistent == 0 or consistent == 1:
        # os.system("echo \"eprover could not determine inconsistency but darwn could for blend " + blendTptpName + "\" > consistencyCheckFile.tmp")
        # print("eprover could not determine (in)consistency but darwn could for blend " + blendTptpName + ". Result: " + str(consistent) + ". Press key to continue."))
        # raw_input()

    return consistent


def checkConsistencyEprover(blendTptpName):
    global eproverTimeLimit

    resFile = open("/data/consistencyRes.log", "w")
    subprocess.call(["eprover", "--auto", "--tptp3-format", "--cpu-limit=" + str(eproverTimeLimit), blendTptpName],
                    stdout=resFile)
    resFile.close()

    resFile = open("/data/consistencyRes.log", 'r')
    res = resFile.read()
    resFile.close()

    # os.system("rm -rf consistencyRes.log")

    if res.find("# No proof found!") != -1 or res.find("# Failure: Resource limit exceeded") != -1:
        print("Eprover: No consistency proof found.")
        return -1

    if res.find("SZS status Unsatisfiable") != -1:
        print("Eprover: Blend inconsistent.")
        return 0

    print("Eprover: Blend consistent.")
    return 1


def checkConsistencyDarwin(blendTptpName):
    global darwinTimeLimit

    darwinCmd = Command("darwin " + blendTptpName)

    status, output, error = darwinCmd.run(timeout=darwinTimeLimit)

    # print(output)
    cVal = -1
    if output.find("ABORTED termination") != -1:
        print("Consistency check w. darwin failed: TIMEOUT")
        cVal = -1
    if output.find("SZS status Satisfiable") != -1:
        print("Consistency check w. darwin succeeds: CONSISTENT")
        cVal = 1
    if output.find("SZS status Unsatisfiable") != -1:
        print("Consistency check w. darwin succeeds: INCONSISTENT")
        cVal = 0

    # raw_input()

    return cVal


def getRenamingsFromModelAtoms(modelAtoms, specFrom, specTo, origCaslSpecName):
    # global inputSpaces
    # spec = inputSpaces[caslSpecName]
    renamings = {}
    for atom in modelAtoms:
        a = str(atom)
        if a[:4] == "exec":
            act = getActFromAtom(a)
            if act["iSpace"] != toLPName(origCaslSpecName, "spec"):
                continue

            if act["actType"] == "renameOp":
                # print("renameOp happens")
                # Add renaming only if operator is in target spec.
                rnToExists = False
                for op in specTo.ops:
                    if act["argVect"][0] == toLPName(op.name, "po"):
                        rnToExists = True
                        break
                rnFromExists = False
                for op in specFrom.ops:
                    if act["argVect"][1] == toLPName(op.name, "po"):
                        rnFromExists = True
                        break
                if rnToExists and rnFromExists:
                    renamings[act["step"]] = act["argVect"]

            if act["actType"] == "renamePred":
                # Add renaming only if operator is in target spec.
                rnToExists = False
                for p in specTo.preds:
                    if act["argVect"][0] == toLPName(p.name, "po"):
                        rnToExists = True
                        break
                rnFromExists = False
                for p in specFrom.preds:
                    if act["argVect"][1] == toLPName(p.name, "po"):
                        rnFromExists = True
                        break
                if rnToExists and rnFromExists:
                    renamings[act["step"]] = act["argVect"]

            if act["actType"] == "renameSort":
                # Add renaming only if operator is in target spec.
                rnToExists = False
                for s in specTo.sorts:
                    if act["argVect"][0] == toLPName(s.name, "sort"):
                        rnToExists = True
                        break
                rnFromExists = False
                for s in specFrom.sorts:
                    if act["argVect"][1] == toLPName(s.name, "sort"):
                        rnFromExists = True
                        break
                if rnToExists and rnFromExists:
                    renamings[act["step"]] = act["argVect"]
    return renamings
