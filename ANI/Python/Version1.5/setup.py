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
  print 'python anilyzePrep.py -i <Directory of .fna files> -o <Anilyze Prep Output Directory>'
  print 'Example: python anilyzePrep.py -tree_i /Users/user/desktop/all.fna/ -tree_o /Users/user/desktop/AnilyzePrepOutputDirectory/'
  print 'Example Files: /path/Examplo_Bacterii.fna and /path/Examplus_Bacterii.fna'
  print ''
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '                                                     Prerequisite Instructions                                                      '
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '1. Download all fna files from ftp://ftp.ncbi.nlm.nih.gov/genomes/archive/old_refseq/Bacteria/all.fna.tar.gz to an empty directory' 
  print '2. Unzip and delete the tar.gz file'
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '                                                        Software Requirements                                                       '
  print '------------------------------------------------------------------------------------------------------------------------------------'   
  print '1. Prerequisite Software: Python'
  print '2. 2.7, Mac OSX or a Linux Operating System'
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '                                                        Hardware Requirements                                                       '
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '1. About 30 times the size of the downloaded tar.gz file(s)'
  print '3. Program tested on 4GB of RAM'
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '                                                                Other                                                               '
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '1. Non-Binary fna files location after program completion: /outDirectoryGiven/complete/complete/'
  print '2. Binary fna files location after program completion: /outDirectoryGiven/complete/binary/complete/'
  print '3. Program will not work correctly if the output directory is in the same location as the last input directory(e.g. /all.fna/)'
  print '------------------------------------------------------------------------------------------------------------------------------------'
  print '************************************************************************************************************************************'
  print '                                                                                                                                    '                                                                    
  print '************************************************************************************************************************************'

def createCMakeFile(inputDirectoryParam, kmerSizeParam, fileSimilarityThresholdParam):
  cMakeFile = open(os.getcwd() + "/anilyze/MAKEFILE", "rw+")
  cMakeFile.write('')
  cMakeFile.write('actual')
  cMakeFile.close()

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
  kmerSizeArg = 10
  fileSimilarityThresholdArg = 95
  i = False
  autoDownloadNCBIFiles = True
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
      i = True
      inputArg = arg
    elif opt == "-k"
      kmerSizeArg = arg
    elif opt == "-s"  
      fileSimilarityThresholdArg = arg
    else:
      print 'python anilyzePrep.py -h'
  if os.path.isdir(inputArg) is False:#check if / at the end, if not there then add
    print 'Invalid Directory'
    sys.exit(2)
  if os.path.isdir(outputArg) is False:
    print 'InvalidDirectory'
    sys.exit(2)
  if(inputArg[-1:] != "/"):
    inputArg = inputArg + "/"
  if i is True:
  	autoDownloadNCBIFiles = False
    runSetup(inputArg)
  if autoDownloadNCBIFiles is True:
    downloadFiles(inputArg)
    runSetup(inputArg)

#main  
if __name__=='__main__':
  main(sys.argv[1:])
