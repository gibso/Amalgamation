import os, glob
import subprocess

from amalgamation import hets_helper, settings, langCasl


def remove_all_output_files():
    fileList = glob.glob(f'/data/*')
    for fileName in fileList:
        os.remove(fileName)


def run_blending():
    remove_all_output_files()

    fName = settings.inputFile

    # Generate an xml file from a CASL input file.
    inputSpacesXmlFileName = langCasl.input2Xml(fName, settings.inputSpaceNames)
    inputSpaces = langCasl.parseXml(inputSpacesXmlFileName)
    print("blending the following CASL specs:")
    for s in inputSpaces:
        print(s.toCaslStr())
    print("\n\n\n")
    # raw_input()
    # Generate the Logic Programming representation of the CASL input spaces.
    lpRep = langCasl.toLP(inputSpaces)
    lpRep = "#program base.\n\n" + lpRep
    generic_file_name = hets_helper.get_generic_filename_for(filename=fName)
    lpFileName = f'/data/{generic_file_name}.lp'
    lpFile = open(lpFileName, 'w')
    lpFile.write(lpRep)
    lpFile.close()
    print("Generated Logic Programming facts from CASL Spec.")

    subprocess.call(["clingo", "--number=" + str(settings.numModels), "--quiet", "amalgamation/iterationGeneralize.py.lp", "amalgamation/caslInterface.lp",
                     "amalgamation/generalize.lp", lpFileName])
