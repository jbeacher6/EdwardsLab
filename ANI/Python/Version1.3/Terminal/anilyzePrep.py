import os
from collections import OrderedDict
import sys
import subprocess
import fileinput
import shutil
import Bio
from Bio.Seq import Seq
import sys, getopt
import datetime
from datetime import datetime
'''
This class will concatinate many .fna files into one .fna file, create a new directory and modify line length and header
Example:
user/directory1/file1.ext
user/directory1/file2.ext
Will turn directory1 into
user/directory1/directory1.ext
directory1.ext is the result of cat file1.ext file2.ext > dictionary1.ext
'''
class ConcatinateAndModifyManyFNAFilesInDirectory():
  def run(self, inputDirectoryParam, outputDirectoryParam):
    directory = inputDirectoryParam
    mkdirRcCommand = "mkdir " + outputDirectoryParam + "/reformatted/"
    os.system(mkdirRcCommand)
    ext = ".fna"
    currentDirectory = None
    previousDirectory = None
    listOfDirectoriesWithMultipleFNAfiles = []
    listOfDirectoriesWithMultipleFNAfilesNoRepeats = []
    x = 0
    for subdir, dirs, files in os.walk(directory, topdown=True):
      for file in files:
        currentDirectory = subdir
        if currentDirectory == previousDirectory:
          listOfDirectoriesWithMultipleFNAfiles.insert(x, currentDirectory)
          x +=1
        previousDirectory = subdir
    listOfDirectoriesWithMultipleFNAfilesNoRepeats = list(OrderedDict.fromkeys(listOfDirectoriesWithMultipleFNAfiles))
    listOfFNAfiles = []
    catCommand = None
    newFNAfileName = None
    for dirFile in listOfDirectoriesWithMultipleFNAfilesNoRepeats:
      uniqueFiles = True
      base = os.path.basename(dirFile)
      fnaConstruct = (os.path.join(dirFile, base))
      newFNAfileName = fnaConstruct+ext
      newFNAfileName2 = fnaConstruct+"MOD1"+ext
      newFNAfileName3 = fnaConstruct+"MOD2"+ext
      for root, dir, files in os.walk(dirFile, topdown=True):
        for f in files:
          currentFile = ((os.path.join(root, f)))
          if newFNAfileName == currentFile:
            uniqueFiles = False
            break
          if f.endswith(ext):
            catFileTo = ((os.path.join(root, f)))
            listOfFNAfiles.append(catFileTo+' ')
            #remove first line in .fna file(header)
            rmFirstLineCommand = "sed -i '' '1d' " + catFileTo
            os.system(rmFirstLineCommand)
      if uniqueFiles:
        string1 = ''.join(listOfFNAfiles)
        catCommand = "cat " + string1 + " > " + newFNAfileName2
        os.system(catCommand)
        #delete all new line characters
        rmNewLinesCommand = "tr -d '\n' < " + newFNAfileName2 + " > " + newFNAfileName3
        os.system(rmNewLinesCommand)
        #make line length 70 characters long and concatinate into /reformatted/ directory
        grepLinesCommand = "grep -oE '.{1,70}' " + newFNAfileName3 + " > " + outputDirectoryParam + "/reformatted/" + base + ext
        os.system(grepLinesCommand)
        rmCommand = "rm " + string1
        os.system(rmCommand)
        rmCommand2 = "rm " + newFNAfileName2
        os.system(rmCommand2)
        rmCommand3 = "rm " + newFNAfileName3
        os.system(rmCommand3)
        rmCommand4 = "rm -r " + dirFile
        os.system(rmCommand4)
        listOfFNAfiles = []
        catCommand = None
        newFNAfileName = None
        string1 = None
    listOfDirectoriesWithMultipleFNAfilesNoRepeats = None
    print("ConcatinatingFNAFiles complete")
    print("Script 25 percent complete")
'''
This class will remove header and concatinate to a new directory
Example:
user/directory1/file1.ext
Will turn directory1 into
user/directory1/directory1.ext
directory1.ext has a modified header 
'''
class ConcatinateAndModifySingleFNAFileInDirectory():
  def run(self, inputDirectoryParam, outputDirectoryParam):
    directory = inputDirectoryParam
    ext = ".fna"
    listOfDirectories = []
    x = 0
    first = True
    firstDirectoryString = ""
    for subdir, dirs, files in os.walk(directory, topdown=True):
      for file in files:
        currentDirectory = subdir
        if first:
          firstDirectoryString = str(currentDirectory) 
        if not first:
          listOfDirectories.insert(x, currentDirectory)
        x += 1
        first = False
    listOfDirectories = list(OrderedDict.fromkeys(listOfDirectories))
    currentFile = None
    catFile = None
    newFNAfileName = None
    uniqueFile = True
    for dirFile in listOfDirectories:
      uniqueFiles = True
      base = os.path.basename(dirFile)
      fnaConstruct = (os.path.join(dirFile, base))
      newFNAfileName = fnaConstruct+ext
      for root, dir, files in os.walk(dirFile, topdown=True):
        for f in files:
          if str(dir) == str(firstDirectoryString):
            break
          currentFile = ((os.path.join(root, f)))
          if newFNAfileName == currentFile:
            print ("already taken care of")
            uniqueFile = False
            break
          elif f.endswith(ext):
            catFile = currentFile
            base2 = os.path.basename(dirFile)
            fnaConstruct = (os.path.join(dirFile, base2))
            newFNAfileName = fnaConstruct + "MOD1" + ext
            catCommand = "cat " + catFile + " > " + newFNAfileName
            os.system(catCommand)
            #remove first line in .fna file
            rmFirstLineCommand = "sed -i '' '1d' " + newFNAfileName
            os.system(rmFirstLineCommand)
            catCommand2 = "cat " + newFNAfileName + " > " + outputDirectoryParam + "/reformatted/" + base + ext
            os.system(catCommand2)
            rmCommand = "rm " + newFNAfileName
            os.system(rmCommand)
            rmCommand2 = "rm -r " + dirFile
            os.system(rmCommand2)
    listOfDirectories = None
    print("ChangeFilesToDirectoryName(): complete")
    print("Script 50 percent complete")
#creates reverse compliment of fna files into /complete
class ReverseComplimentComplete():
  def run(self, inputDirectoryParam, outputDirectoryParam):
    mkdirCatCommand = "mkdir " + outputDirectoryParam + "/complete" 
    os.system(mkdirCatCommand)
    mkdirMODCommand = "mkdir " + outputDirectoryParam + "/complete/MOD"
    os.system(mkdirMODCommand)
    mkdirMODCommand2 = "mkdir " + outputDirectoryParam + "/complete/MOD2"
    os.system(mkdirMODCommand2)
    mkdirMODCommand3 = "mkdir " + outputDirectoryParam + "/complete/complete"
    os.system(mkdirMODCommand3)
    ext = ".fna"
    outputDirectory = outputDirectoryParam
    reformattedDirectory = outputDirectoryParam + "/reformatted"
    #creates reverse compliment of TkANI.allFnaDirectoryLocationString and puts the result in TkANI.allFnaDirectoryLocationString/rc
    mkdirRcCommand = "mkdir " + outputDirectory + "/rc"
    os.system(mkdirRcCommand)
    directoryRC = outputDirectory + "/rc"
    #
    for root, dir, files in os.walk(outputDirectory, topdown=True):
      for f in files:
        if f.endswith(ext):
          fileMod = outputDirectoryParam + "/reformatted/" + f
          with open(fileMod) as file:
            currentFile = ((os.path.join(root, f)))
            seqString = file.read()
            seq = Seq(seqString)
            base = os.path.basename(outputDirectory)
            newFileString = outputDirectoryParam + "/rc/" + f
            newFile = open(newFileString, "w")
            string = seq.reverse_complement()
            newFile.write(str(string))
            newFile.close()
    #
    directoryComplete = outputDirectory + "/complete"
    for root, dir, files in os.walk(directoryComplete, topdown=True):
      for f in files:
         if f.endswith(ext):
            currentFile1 = ((os.path.join(root, f)))
         else:
            currentFile2 = ((os.path.join(root, f)))
            rmCommand = "rm " + currentFile2
            os.system(rmCommand)
    #concatinate reverse compliment
    for root, dir, files in os.walk(outputDirectory, topdown=True):
      for f in files:
        if f.endswith(ext):
          fileModReformatted = outputDirectoryParam + "/reformatted/" + f
          fileModRC = outputDirectoryParam + "/rc/" + f
          fileModComplete = outputDirectoryParam + "/complete/MOD/" + f
          catCommand = "cat " + fileModReformatted + " " + fileModRC + " > " + fileModComplete
          os.system(catCommand)
    #format to a line length of 70
    directoryCompleteMOD = outputDirectoryParam + "/complete/MOD/"
    directoryCompleteMOD2 = outputDirectoryParam + "/complete/MOD2/"
    directoryCompleteMOD3 = outputDirectoryParam + "/complete/complete/"
    #
    for root, dir, files in os.walk(directoryCompleteMOD, topdown=True):
      for f in files:
        if f.endswith(ext):
          currentFile = ((os.path.join(root, f)))
          newFNAfileName1 = directoryCompleteMOD2 + str(f)
          newFNAfileName2 = directoryCompleteMOD3 + str(f)
          #remove all new lines
          rmNewLinesCommand = "tr -d '\n' < " + currentFile + " > " + newFNAfileName1
          os.system(rmNewLinesCommand)
          #modify to 70 characters long
          grepLinesCommand = "grep -oE '.{1,70}' " + newFNAfileName1 + " > " + newFNAfileName2
          os.system(grepLinesCommand)
    shutil.rmtree(directoryRC)
    shutil.rmtree(reformattedDirectory)
    shutil.rmtree(directoryCompleteMOD)
    shutil.rmtree(directoryCompleteMOD2)
    #shutil.rmtree(directoryCompleteMOD3)       
    print("ReverseComplimentComplete(): complete")
    print("Script 75 percent complete")
#Get input and output directories from terminal and run the program
#creates binary of teh forward and reverse complimented files created earlier in the program. 
class ConvertToBinary(): 
  def run(self, inputDirectoryParam, outputDirectoryParam):
    binaryString = ""
    binaryDirectory = outputDirectoryParam + "/complete/binary" 
    mkdirBinaryCommand = "mkdir " + binaryDirectory
    os.system(mkdirBinaryCommand)
    mkdirBinaryCommand2 = "mkdir " + binaryDirectory + "/trLines"
    os.system(mkdirBinaryCommand2)
    mkdirBinaryCommand3 = "mkdir " + binaryDirectory + "/complete"
    os.system(mkdirBinaryCommand3)
    mkdirBinaryCommand4 = "mkdir " + binaryDirectory + "/binary"
    os.system(mkdirBinaryCommand4)
    completeDirectory = outputDirectoryParam + "/complete/complete/"
    ext = ".fna"
    for root, dir, files in os.walk(outputDirectoryParam, topdown=True):
      for f in files:
        if f.endswith(ext):
          fileMod = completeDirectory + f
          with open(fileMod) as file:
            binaryString = ""
            for line in file:
              for character in line:
                if character == "A":
                  binaryString += "00"
                elif character == "C":
                  binaryString += "01"
                elif character == "G":
                  binaryString += "10"
                elif character == "T":
                  binaryString += "11"
                else:
                  if character != "\n" and character != "A" and character != "G" and character != "C" and character != "T":
                    print("error: " + str(character) + " in " + str(fileMod) + " is not a newline, A C G or T")
            currentFile = ((os.path.join(root, f)))
            #base = os.path.basename(outputDirectoryParam)
            newFileString = binaryDirectory + "/binary/" + f
            newFile = open(newFileString, "w")
            newFile.write(str(binaryString))
            newFile.close()
            #
            newFNAfileName1 = binaryDirectory + "/trLines/" + str(f)
            newFNAfileName2 = binaryDirectory + "/complete/" + str(f)
            #remove all new lines
            rmNewLinesCommand = "tr -d '\n' < " + newFileString + " > " + newFNAfileName1
            os.system(rmNewLinesCommand)
            #modify to 70 characters long
            grepLinesCommand = "grep -oE '.{1,70}' " + newFNAfileName1 + " > " + newFNAfileName2
            os.system(grepLinesCommand)
    shutil.rmtree(binaryDirectory + "/trLines")
    shutil.rmtree(binaryDirectory + "/binary")
    print("ReverseComplimentComplete(): complete")
    print("Script 100 percent complete")

def main(argv):
  try:
    optionals, arguments = getopt.getopt(argv,"hi:o:",["inputArg=","outputArg="])
  except getopt.GetoptError as error:
    print str(error)
    print 'Usage: anilyzePrep.py -i <unzipped forward fna files directory location> -o <forward and reverse compliment fna files directory location>'
    sys.exit(2)
  for opt, arg in optionals:
    if opt == '-h':
     print '************************************************************************************************************************************'
      print '                                                         Anilyze Prep Help                                                          '                                                                    
      print '************************************************************************************************************************************'
      print 'python anilyzePrep.py -i <Unzipped all.fna.tar.gz Directory> -o <Anilyze Prep Output Directory>'
      print 'Example: python anilyzePrep.py -i /Users/jon/desktop/all.fna/ -o /Users/jon/desktop/AnilyzePrepOutputDirectory/'
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
      print '1. 60GB of space'
      print '2. Program tested on 4GB of RAM'
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
      sys.exit()
    elif opt in ("-i", "--inDir"):
      inputArg = arg
    elif opt in ("-o", "--outDir"):
      outputArg = arg
  print 'Input file is "', inputArg
  print 'Output file is "', outputArg
  #
  print("Program started running at time: " + str(datetime.now()))
  if os.path.isdir(inputArg) is False:
    print 'Invalid Directory'
    sys.exit(2)
  if os.path.isdir(outputArg) is False:
    print 'InvalidDirectory'
    sys.exit(2)
  concatinateAndModifyManyFNAFilesInDirectory = ConcatinateAndModifyManyFNAFilesInDirectory()
  concatinateAndModifySingleFNAFileInDirectory = ConcatinateAndModifySingleFNAFileInDirectory()
  reverseComplimentComplete = ReverseComplimentComplete()
  convertToBinary = ConvertToBinary()
  concatinateAndModifyManyFNAFilesInDirectory.run(inputArg, outputArg)
  concatinateAndModifySingleFNAFileInDirectory.run(inputArg, outputArg)
  reverseComplimentComplete.run(inputArg, outputArg)
  convertToBinary.run(inputArg, outputArg)
  print("Program completed at time: " + str(datetime.now()))
#main  
if __name__=='__main__':
  main(sys.argv[1:])
