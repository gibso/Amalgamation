from langCasl import *
import os, glob
import subprocess

from settings import *

def remove_all_output_files():
    for output_type in ['th', 'xml', 'casl', 'tp']:
        remove_output_files(output_type)

def remove_output_files(file_type):
    fileList = glob.glob(f'/data/{file_type}/*.{file_type}')
    for fileName in fileList:
        os.remove(fileName)

remove_all_output_files()

fName = inputFile

# Generate an xml file from a CASL input file. 
inputSpacesXmlFileName = input2Xml(fName,inputSpaceNames) 
inputSpaces = parseXml(inputSpacesXmlFileName)
print("blending the following CASL specs:")
for s in inputSpaces:
    print(s.toCaslStr())
print("\n\n\n")
# raw_input()
# Generate the Logic Programming representation of the CASL input spaces. 
lpRep = toLP(inputSpaces)
lpRep = "#program base.\n\n" + lpRep
lpFileName = fName.split(".")[0]+".lp"
lpFile = open(lpFileName,'w')
lpFile.write(lpRep)
lpFile.close()
print("Generated Logic Programming facts from CASL Spec.")

subprocess.call(["clingo", "--number="+str(numModels), "--quiet", "iterationGeneralize.py.lp", "caslInterface.lp", "generalize.lp", lpFileName])
