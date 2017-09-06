from anilyze import downloadFiles
from anilyze import decompress
from anilyze import deleteFirstLineAndRename
from anilyze import deleteLineInfo
from anilyze import createReverseComplimentAndAppendToForward
from anilyze import convertToBinary
from anilyze import modifyLineLengthToSeventy
from anilyze import splitFastaForComplete
import sys
import getopt
import os
import unittest

def printHelp():
  print '************************************************************************************************************************************'
  print '                                                         Anilyze Prep Help                                                          '                                                                    
  print '************************************************************************************************************************************'
  print 'Options:'
  print 'python anilyze.py -i <Directory of .fna or .fasta files> '
  print 'python anilyze.py -d'
  print 'python anilyze.py -r'
  print 'Example: python anilyze.py -i /Users/user/desktop/fnaFilesLocation/'
  print 'Example Files: /path/Examplo_Bacterii.fna and /path/Examplus_Bacterii.fna'
  print '-d flag will automatically download and setup all complete genomes from NCBI location'
  print 'https://www.ncbi.nlm.nih.gov/genome/doc/ftpfaq/'
  print '-r flag will run setup on files located in ./inputFiles'
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '                                                     Prerequisite Instructions                                                      '
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '1. pip the requirements.txt'
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '                                                        Software Requirements                                                       '
  print '------------------------------------------------------------------------------------------------------------------------------------'   
  print '1. Prerequisite Software: Python 2.7, Biopython module installed and Mac OSX or a Linux Operating System'
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '                                                        Hardware Requirements                                                       '
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '1. About 30 times the size of the specified tar.gz file(s)'
  print '3. Program tested on 4GB of RAM'
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '                                                                Other                                                               '
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '************************************************************************************************************************************'
  print '                                                                                                                                    '                                                                    
  print '************************************************************************************************************************************'

def runSetup(inputDirectoryParam):
	decompress(inputArg)
  deleteFirstLineAndRename(inputArg)
  deleteLineInfo(inputArg)
  createReverseComplimentAndAppendToForward(inputArg)
  convertToBinary(inputArg)
  modifyLineLengthToSeventy(inputArg)
  numberOfFiles = 0
  for root, dir, files in os.walk(inputArg + "correctlyFormatted", topdown=True):#traverse the directory containing the files of type .fna.gz
    for currentFile in files:
      numberOfFiles =+ 1
  createCMakeFile(inputArg, outputArg, kmerSizeArg, fileSimilarityThresholdArg)

def main(argv):
  inputArg = ''
  outputArg = ''
  inputFilesDefaultPathString = os.getcwd() + "/inputFiles"
  inputFilesDefaultPathBoolean = False
  inputFilesManuallyBoolean = False
  autoDownloadNCBIFilesBoolean = False
  try:
    optionals, arguments = getopt.getopt(argv,"hi:o:",["inputArg="])
  except getopt.GetoptError as error:
    print str(error)
    print 'Usage:'
    sys.exit(2)
  for opt, arg in optionals:
    if opt == '-h':
      printHelp()
      sys.exit(2)
    elif opt in ("-i", "--inDir"):
      inputFilesManually = True
      inputArg = arg
    elif opt == '-d':
      autoDownloadNCBIFiles = True
    else:
      print 'python anilyze.py -h'
  if os.path.isdir(inputArg) is False:#check if / at the end, if not there then add
    print 'Invalid Directory'
    sys.exit(2)
  if os.path.isdir(outputArg) is False:
    print 'InvalidDirectory'
    sys.exit(2)
  if(inputArg[-1:] != "/"):
    inputArg = inputArg + "/"
  if inputFilesManuallyBopolean is True:
    autoDownloadNCBIFilesBolean = False
    runSetup(inputArg)
  elif autoDownloadNCBIFilesBoolean is True:
    downloadFiles(inputFilesDefaultPathString)
    runSetup(inputFilesDefaultPathString)
  elif inputFilesDefaultPathBoolean is True:
    runSetup(inputFilesDefaultPathString)
  else:
    printHelp()
#main  
if __name__=='__main__':
  main(sys.argv[1:])
