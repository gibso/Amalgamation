import subprocess

from amalgamation import hets_helper, settings, langCasl
from amalgamation.input_metadata import InputMetadata



def run_blending():

    input = InputMetadata()

    # Generate an xml file from a CASL input file.
    inputSpacesXmlFileName = langCasl.input2Xml(input.inputFile, input.inputSpaceNames)
    inputSpaces = langCasl.parseXml(inputSpacesXmlFileName)
    print("blending the following CASL specs:")
    for s in inputSpaces:
        print(s.toCaslStr())
    print("\n\n\n")
    # raw_input()
    # Generate the Logic Programming representation of the CASL input spaces.
    lpRep = langCasl.toLP(inputSpaces)
    lpRep = "#program base.\n\n" + lpRep
    generic_file_name = hets_helper.get_generic_filename_for(filename=input.inputFile)
    lpFileName = f'/data/{generic_file_name}.lp'
    lpFile = open(lpFileName, 'w')
    lpFile.write(lpRep)
    lpFile.close()
    print("Generated Logic Programming facts from CASL Spec.")

    subprocess.call([
        "/opt/conda/bin/clingo",
        "--number=" + str(settings.numModels),
        "--quiet", "amalgamation/iterationGeneralize.py.lp",
        "amalgamation/caslInterface.lp",
        "amalgamation/generalize.lp",
        lpFileName
    ])
