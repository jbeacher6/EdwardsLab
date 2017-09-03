from anilyze import *
import sys
import getopt
import os
import unittest

def main(argv):
  inputArg = ''
  outputArg = ''
  split_i = False
  i = False
  try:
    optionals, arguments = getopt.getopt(argv,"hi:o:",["inputArg=","outputArg="])
  except getopt.GetoptError as error:
    print str(error)
    print 'Usage: anilyzePrep.py -i <unzipped forward fna files directory location> -o <output files directory location>'
    sys.exit(2)
  for opt, arg in optionals:
    if opt == '-h':
      printHelp()
      sys.exit()
    elif opt in ("-split_i", "--inDir"):
      split_i = True
      i = False
      outputArg = arg
    elif opt in ("-i", "--inDir"):
      i = True
      split_i = False
      inputArg = arg
    elif opt in ("-o", "--outDir"):
      outputArg = arg
    else:
      print 'python anilyzePrep.py -h'
  #check if / at the end, if not there then add
  if os.path.isdir(inputArg) is False:
    print 'Invalid Directory'
    sys.exit(2)
  if os.path.isdir(outputArg) is False:
    print 'InvalidDirectory'
    sys.exit(2)
  if(inputArg[-1:] != "/"):
    inputArg = inputArg + "/"
  if(outputArg[-1:] != "/"):
    outputArg = outputArg + "/"
  if split_i is True:
     splitFasta(inputArg, outputArg)
  if i is True:
    #print 'Input file is "', inputArg
    #print 'Output file is "', outputArg
    #downloadFiles(inputArg)
    decompress(inputArg)
    deleteFirstLineAndRename(inputArg)
    deleteLineInfo(inputArg)
    createReverseComplimentAndAppendToForward(inputArg)
    convertToBinary(inputArg)
    modifyLineLengthToSeventy(inputArg, outputArg)

#main  
if __name__=='__main__':
  main(sys.argv[1:])