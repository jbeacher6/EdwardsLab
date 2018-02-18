from anilyze import downloadFiles
from anilyze import decompress
from anilyze import deleteFirstLineAndRename
from anilyze import deleteLineInfo
from anilyze import createReverseComplimentAndAppendToForward
from anilyze import convertToBinary
from anilyze import modifyLineLengthToSeventy
from anilyze import splitFastaForComplete
from anilyze import modifyFileNames
import sys
import getopt
import os
import unittest
import argparse

def runSetupA(inputDirectoryParam):
  decompress(inputDirectoryParam)
  deleteFirstLineAndRename(inputDirectoryParam)
  deleteLineInfo(inputDirectoryParam)
  modifyFileNames(inputDirectoryParam)
  createReverseComplimentAndAppendToForward(inputDirectoryParam)
  #convertToBinary(inputDirectoryParam)
  modifyLineLengthToSeventy(inputDirectoryParam, inputDirectoryParam)

def runSetupE(inputDirectoryParam):
  #decompress(inputDirectoryParam)
  #deleteFirstLineAndRename(inputDirectoryParam)
  #deleteLineInfo(inputDirectoryParam)
  #createReverseComplimentAndAppendToForward(inputDirectoryParam)
  #convertToBinary(inputDirectoryParam)
  modifyLineLengthToSeventy(inputDirectoryParam, inputDirectoryParam)

def runSetupF(inputDirectoryParam):
  splitFastaForComplete(inputDirectoryParam)
  modifyFileNames(inputDirectoryParam)
  createReverseComplimentAndAppendToForward(inputDirectoryParam)
  #convertToBinary(inputDirectoryParam)
  modifyLineLengthToSeventy(inputDirectoryParam, inputDirectoryParam)

def main(argv):
  inputFilesDefaultPathString = os.getcwd() + "/fnaFiles/"
  parser = argparse.ArgumentParser()
  parser.add_argument('-e', '--executeWithDefaultInputDirectory', help='Execute with .fna files in ./anilyze/fnaFiles', action='store_true')
  parser.add_argument('-a', '--autoDownloadNCBIComplete', help='Automatically download files and execute with NCBI complete bacteria DNA files', action='store_true')
  parser.add_argument('-f', '--executeWithDefaultInputDirectoryFasta', help='Execute with .fasta files in ./anilyze/fastaFiles', action='store_true')
  #parser.add_argument('-a', '--autoDownloadNCBIComplete', help='help')
  args = parser.parse_args() 
  if(args.executeWithDefaultInputDirectory):
    runSetupE(inputFilesDefaultPathString)
  if(args.autoDownloadNCBIComplete):
    downloadFiles(inputFilesDefaultPathString, False)
    runSetupA(inputFilesDefaultPathString)
  if(args.executeWithDefaultInputDirectoryFasta):
    runSetupE(inputFilesDefaultPathString)
#main  
if __name__=='__main__':
  main(sys.argv[1:])