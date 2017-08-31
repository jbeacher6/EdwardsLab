import ftplib
import os
import time
from collections import OrderedDict
import sys
import subprocess
import fileinput
import shutil
import Bio
from Bio.Seq import Seq
import sys, getopt

class DownloadAndDecompress():
  def run(self, inputDirectoryParam, outputDirectoryParam):
    currentDirectory = "/Users/jon/desktop/anilyzeDocumentation/"
    email = 'jonbeacher@gmail.com'
    prepDirectoryName = "prep/"
    prepDirectoryName2 = "prep"
    fnaFilesDirectoryName = "fnaFiles"
    ftpDirPathsModFilename = prepDirectoryName + "ftpDirPathsMod"
    ftpDirPathsFilename = prepDirectoryName + "ftpDirPaths"
    ftpFilePathsFilename = prepDirectoryName + "ftpFilePaths"
    mkdirCommandFnaFilesDirectory = "mkdir " + str(fnaFilesDirectoryName)
    mkdirCommandPrepFilesDirectory = "mkdir " + str(prepDirectoryName)
    numDirs = 0
    numFiles = 0
    dirList = []
    fileList = []
    print("Creating output directories")
    if not os.path.exists(fnaFilesDirectoryName):
      os.system(mkdirCommandFnaFilesDirectory)
    else:
      os.system("rm -r " + fnaFilesDirectoryName)
      os.system(mkdirCommandFnaFilesDirectory)
    if not os.path.exists(prepDirectoryName2):
      os.system(mkdirCommandPrepFilesDirectory)
    else:
      os.system("rm -r " + prepDirectoryName2)
      os.system(mkdirCommandPrepFilesDirectory)
    ftp = ftplib.FTP('ftp.ncbi.nlm.nih.gov')
    ftp.login('anonymous', email)
    #Awk commands and more details can be found at https://www.ncbi.nlm.nih.gov/genome/doc/ftpfaq/#asmsumfiles
    ftp.cwd("/genomes/refseq/bacteria/")
    print("Downloading assembly_summary.txt and executing awk commands")
    assemblySummaryText = str(currentDirectory) + str(prepDirectoryName) + "assembly_summary.txt"
    assemblySummaryTextDownloadCommand = ftp.retrbinary("RETR assembly_summary.txt", open(str(assemblySummaryText), 'wb').write)
    ftpdirpathsAwk = prepDirectoryName + "ftpdirpaths"
    awkFtpDirPathsDownloadCommand = "awk -F \"\t\" \'$12==\"Complete Genome\" && $11==\"latest\"{print $20}\' assembly_summary.txt > " + str(ftpdirpathsAwk)
    os.system(awkFtpDirPathsDownloadCommand)
    ftpfilepathsAwk = prepDirectoryName + "ftpfilepaths"
    awkFtpFilePathsDownloadCommand2 = "awk \'BEGIN{FS=OFS=\"/\";filesuffix=\"genomic.fna.gz\"}{ftpdir=$0;asm=$10;file=asm\"_\"filesuffix;print file}\' " + ftpdirpathsAwk +  " > " + str(ftpfilepathsAwk)
    os.system(awkFtpFilePathsDownloadCommand2)
    print("Downloading files")
    with open(ftpDirPathsModFilename, "w") as ftpDirPathMod:
      ftpDirPathMod.write('')
    with open(ftpDirPathsFilename, "rw+") as ftpDirPath:
      for dirPathStringLine in ftpDirPath:
        with open(ftpDirPathsModFilename, "a") as ftpDirPathMod:
          ftpDirPathMod.write(str(dirPathStringLine[26:]))
          ftpDirPathMod.close()
      ftpDirPath.close()
    with open(ftpDirPathsModFilename, "rw+") as ftpDirPath:
      for dirPathStringLine in ftpDirPath:
        dirList.append(str(dirPathStringLine.strip()))
        numDirs =+ 1
    with open(ftpFilePathsFilename, "rw+") as ftpFilePath:
      for filePathStringLine in ftpFilePath:
        fileList.append(str(filePathStringLine.strip()))
        numFiles =+1
    if numDirs != numFiles:
      print(str("Error, numDirs != numFiles"))
    for i, val in enumerate(dirList):
      ftp.cwd(str(dirList[i]))
      newFileName = str(fnaFilesDirectoryName + "/" + fileList[i])
      print(str(dirList[i]) + str(fileList[i]))
      ftp.retrbinary("RETR " + fileList[i], open(newFileName, 'wb').write)
    print("Download of files complete")
    print("Decompressing files")
    for i, val in enumerate(fileList):
      unGzCommand = "gunzip -d " + str(currentDirectory) + str(prepDirectoryName) + str(fileList[i])
      print(str(unGzCommand))
      os.system(unGzCommand)
    print("Decompressing files complete")
    

#Reformat and rename list of fna files
class ReverseComplimentComplete():
  def run(self, inputDirectoryParam, outputDirectoryParam):
    mkdirCatCommand = "mkdir " + outputDirectoryParam + "complete" 
    print(str(mkdirCatCommand))
    os.system(mkdirCatCommand)
    mkdirMODCommand = "mkdir " + outputDirectoryParam + "complete/MOD"
    os.system(mkdirMODCommand)
    mkdirMODCommand2 = "mkdir " + outputDirectoryParam + "complete/MOD2"
    os.system(mkdirMODCommand2)
    mkdirMODCommand3 = "mkdir " + outputDirectoryParam + "complete/complete"
    os.system(mkdirMODCommand3)
    mkdirRcCommand = "mkdir " + outputDirectoryParam + "rc"
    os.system(mkdirRcCommand)
    ext = ".fna"
    outputDirectory = outputDirectoryParam
    reformattedDirectory = outputDirectoryParam
    #creates reverse compliment of TkANI.allFnaDirectoryLocationString and puts the result in TkANI.allFnaDirectoryLocationString/rc
    directoryRC = outputDirectory + "rc"
    #
    for root, dir, files in os.walk(inputDirectoryParam, topdown=True):
      for f in files:
        if f.endswith(ext):
          filePath = inputDirectoryParam + f
          with open(filePath) as file:
            currentFile = ((os.path.join(root, f)))
            seqString = file.read()
            seq = Seq(seqString)
            base = os.path.basename(outputDirectoryParam)
            newFileString = outputDirectoryParam + "rc/" + f
            newFile = open(newFileString, "w")
            string = seq.reverse_complement()
            newFile.write(str(string))
            newFile.close()
    #concatinate reverse compliment
    for root, dir, files in os.walk(inputDirectoryParam, topdown=True):
      for f in files:
        if f.endswith(ext):
          fileReformatted = inputDirectoryParam + f
          fileRC = outputDirectoryParam + "rc/" + f
          fileComplete = outputDirectoryParam + "complete/MOD/" + f
          catCommand = "cat " + fileReformatted + " " + fileRC + " > " + fileComplete
          os.system(catCommand)
    #format to a line length of 70
    directoryCompleteMOD = outputDirectoryParam + "complete/MOD/"
    directoryCompleteMOD2 = outputDirectoryParam + "complete/MOD2/"
    directoryCompleteMOD3 = outputDirectoryParam + "complete/complete/"
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
    shutil.rmtree(directoryCompleteMOD)
    shutil.rmtree(directoryCompleteMOD2)
    #shutil.rmtree(directoryCompleteMOD3)       
    print("ReverseComplimentComplete(): complete")

class ConvertToBinary(): 
  def run(self, inputDirectoryParam, outputDirectoryParam):
    x = 0
    binaryString = ""
    binaryDirectory = outputDirectoryParam + "complete/binary" 
    mkdirBinaryCommand = "mkdir " + binaryDirectory
    os.system(mkdirBinaryCommand)
    mkdirBinaryCommand2 = "mkdir " + binaryDirectory + "/trLines"
    os.system(mkdirBinaryCommand2)
    mkdirBinaryCommand3 = "mkdir " + binaryDirectory + "/complete"
    os.system(mkdirBinaryCommand3)
    mkdirBinaryCommand4 = "mkdir " + binaryDirectory + "/incomplete"
    os.system(mkdirBinaryCommand4)
    completeDirectory = outputDirectoryParam + "complete/complete/"
    ext = ".fna"
    for root, dir, files in os.walk(completeDirectory, topdown=True):
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
                    #print("error: " + str(character) + " in " + str(fileMod) + " is not a newline, A C G or T")
                    x =+1
            currentFile = ((os.path.join(root, f)))
            #base = os.path.basename(outputDirectoryParam)
            newFileString = binaryDirectory + "/incomplete/" + f
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
    shutil.rmtree(binaryDirectory + "/incomplete")
    print("ReverseComplimentComplete(): complete")
    print("Script 100 percent complete")

class SplitFasta():
  def run(self, inputFileParam, outputDirectoryParam):
    x = 0
    #"/Users/jon/desktop/split/split16S"
    os.system("mkdir " + outputDirecotryParam)
    firstLine = True
    fnaName = ''
    prevFileName = ''
    newFileName = ''
    #'/Users/jon/Desktop/split/sequence.fasta'
    with open(inputFileParam) as file:
      for line in file:
        if line.strip() == '':
          firstLine = True
          x += 1
        else:
          if firstLine is True:
            fnaList = line.strip().split()
            fnaName = fnaList[1] + "_" + fnaList[2]
            newFileName = outputDirectoryParam + str(fnaName) + ".fna"
            if str(newFileName) == str(prevFileName):
              newFileName = outputDirectoryParam + str(fnaName) + str(x) + ".fna"
            else:
              prevFileName = newFileName
              newFileName = outputDirectoryParam + str(fnaName) + ".fna"
          else: 
            with open(newFileName, 'a') as newFile:
              newFile.write(line.strip())
          firstLine = False
    file.close()

def main(argv):
  inputArg = ''
  outputArg = ''
  tree_i = False
  split_i = False
  i = False
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
      print '1. About 30 times the size of the input directory as a tar.gz file'
      print '2. 60GB of space needed for all.fna.tar.gz(2.93GB)'
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
      sys.exit()
    elif opt in ("-tree_i", "--inDir"):
      tree_i = True
      split_i = False
      inputArg = arg
    elif opt in ("-split_i", "--inDir"):
      split_i = True
      tree_i = False
      i = False
      outputArg = arg
    elif opt in ("-i", "--inDir"):
      i = True
      tree_i = False
      split_i = False
      inputArg = arg
    elif opt in ("-o", "--outDir"):
      outputArg = arg
    else:
      print 'python anilyzePrep.py -h'

  #print 'Input file is "', inputArg
  #print 'Output file is "', outputArg
  #
  if os.path.isdir(inputArg) is False:
    print 'Invalid Directory'
    sys.exit(2)
  if os.path.isdir(outputArg) is False:
    print 'InvalidDirectory'
    sys.exit(2)
  if tree_i is True:
     concatinateAndModifyManyFNAFilesInDirectory = ConcatinateAndModifyManyFNAFilesInDirectory()
     concatinateAndModifySingleFNAFileInDirectory = ConcatinateAndModifySingleFNAFileInDirectory()
     reverseComplimentComplete = ReverseComplimentComplete()
     convertToBinary = ConvertToBinary()

     concatinateAndModifyManyFNAFilesInDirectory.run(inputArg, outputArg)
     concatinateAndModifySingleFNAFileInDirectory.run(inputArg, outputArg)
     reverseComplimentComplete.run(inputArg, outputArg)
     convertToBinary.run(inputArg, outputArg)
  if split_i is True:
     split = Split()
     split.run(inputArg, outputArg)
  if i is True:
     downloadAndDecompress = DownloadAndDecompress()
     reverseComplimentComplete = ReverseComplimentComplete()
     convertToBinary = ConvertToBinary()
     downloadAndDecompress.run(inputArg, outputArg)
     #reverseComplimentComplete2.run(inputArg, outputArg)
     #convertToBinary2.run(inputArg, outputArg)
     #downloadAndDecompress.run(inputArg, outputArg)
#main  
if __name__=='__main__':
  main(sys.argv[1:])
