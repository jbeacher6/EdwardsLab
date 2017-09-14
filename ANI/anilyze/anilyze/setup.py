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

def runSetup(inputDirectoryParam):
  decompress(inputDirectoryParam)
  deleteFirstLineAndRename(inputDirectoryParam)
  deleteLineInfo(inputDirectoryParam)
  splitFastaForComplete(inputDirectoryParam)
  modifyFileNames(inputDirectoryParam)
  createReverseComplimentAndAppendToForward(inputDirectoryParam)
  convertToBinary(inputDirectoryParam)
  modifyLineLengthToSeventy(inputDirectoryParam, inputDirectoryParam)
  numberOfFiles = 0

def main(argv):
  inputFilesDefaultPathString = os.getcwd() + "/inputFiles/"
  parser = argparse.ArgumentParser()
  parser.add_argument('-e', '--executeWithDefaultInputDirectory', help='Execute with .fna or .fasta files in ./anilyze/inputFiles', action='store_true')
  parser.add_argument('-a', '--autoDownloadNCBIComplete', help='Automatically download files and execute with NCBI complete bacteria DNA files', action='store_true')
  #parser.add_argument('-a', '--autoDownloadNCBIComplete', help='help')
  args = parser.parse_args() 
  if(args.executeWithDefaultInputDirectory):
    runSetup(inputFilesDefaultPathString)
  if(args.autoDownloadNCBIComplete):
    downloadFiles(inputFilesDefaultPathString)
    runSetup(inputFilesDefaultPathString)
#main  
if __name__=='__main__':
  main(sys.argv[1:])