#!/user/bin/python
import ftplib#library used to download files using ftp
import os#library used to execute system commands
import time#library used to calculate total run time
from collections import OrderedDict
import sys#library used to execute system commands
import subprocess
import fileinput#library used to get file input
import shutil#library used to use shell
import Bio#library used to use seq to reverse concatinate the fna files
from Bio.Seq import Seq#library used to reverse concatinate the fna files
import getopt
#Step 1: Download current fna.gz files from NCBI
#This will download the complete bacterial files via ftp with file extensions of .fna.gz from refseq
#Details and more information can be found at https://www.ncbi.nlm.nih.gov/genome/doc/ftpfaq/#asmsumfiles
#Parameter inputDirectoryParam: the directory to download the .fna.gz files from refseq
class DownloadFiles():
  def run(self, inputDirectoryParam):
    print("DownloadAndDecompress() running")#print progress of program
    currentDirectory = "/Users/jon/desktop/anilyzeDocumentation/"
    email = 'jonbeacher@gmail.com'#email to login with refseq to 
    prepDirectoryName = "prep/"#name of the directory that will contain ftpDirPaths, ftpDirPathsMod, ftpFilePaths and assembly_summary.txt files
    prepDirectoryName2 = "prep"#name of the directory that will contain ftpDirPaths, ftpDirPathsMod, ftpFilePaths and assembly_summary.txt files
    fnaFilesDirectoryName = "fnaFiles"#name of the directory that will contain all of the .fna.gz files from refseq
    ftpDirPathsFilename = prepDirectoryName + "ftpDirPaths"#name of the file that will contain a list of all the file paths used to download using ftp
    ftpDirPathsModFilename = prepDirectoryName + "ftpDirPathsMod"#name of the modded file that will contain a list of all the modded directory paths used to download using ftplib
    ftpFilePathsFilename = prepDirectoryName + "ftpFilePaths"#name of the file that will contain a list of all the file paths used to download using ftplib
    mkdirCommandFnaFilesDirectory = "mkdir " + str(fnaFilesDirectoryName)#create directory of the .fna.gz files download location
    mkdirCommandPrepFilesDirectory = "mkdir " + str(prepDirectoryName)#create directory of the ftpDirPaths, ftpDirPathsMod, ftpFilePaths and assembly_summary.txt files
    numDirs = 0#number of directories contained in the ftpDirPathsMod file
    numFiles = 0#number of directories contained in the ftpFilePaths file
    dirList = []#python list containing the name of the directories used to download using ftp from ftpDirPathsMod
    fileList = []#python list containing the name of the files used to download using ftp from ftoFilePaths
    print("Creating output directories")#print the progress of the program
    if not os.path.exists(fnaFilesDirectoryName):#check if the directory that will contain all of the .fna.gz files exists
      os.system(mkdirCommandFnaFilesDirectory)#if it does not exist, create the directory
    else:#the directory already exists and this program will delete the contents of the directory
      os.system("rm -r " + fnaFilesDirectoryName)#remove the contents of the directory
      os.system(mkdirCommandFnaFilesDirectory)#create the directory that will contain all of the .fna.gz files
    if not os.path.exists(prepDirectoryName2):#check if the directory that will contain the ftpDirPaths, ftpDirPathsMod, ftpFilePaths and assembly_summary.txt files
      os.system(mkdirCommandPrepFilesDirectory)#if the directory does not exist, then create it
    else:#the directory has already been created and will be deleted
      os.system("rm -r " + prepDirectoryName2)#remove the directory
      os.system(mkdirCommandPrepFilesDirectory)#create the directory
    ftp = ftplib.FTP('ftp.ncbi.nlm.nih.gov')#set up the ftp connection to NCBI
    ftp.login('anonymous', email)#login with username of anonymous and the email given earlier in the program
    #Awk commands and more details can be found at https://www.ncbi.nlm.nih.gov/genome/doc/ftpfaq/#asmsumfiles
    ftp.cwd("/genomes/refseq/bacteria/")#change the ftp directory to the bacteria genome download locations in refseq
    print("Downloading assembly_summary.txt and executing awk commands")#print the progress of the program
    os.system(ftp.retrbinary("RETR assembly_summary.txt", open(str(currentDirectory) + str(prepDirectoryName) + "assembly_summary.txt", 'wb').write))#download the assembly summary file
    os.system("awk -F \"\t\" \'$12==\"Complete Genome\" && $11==\"latest\"{print $20}\' assembly_summary.txt > " + str(prepDirectoryName + "ftpdirpaths"))#download ftpdirpaths
    os.system("awk \'BEGIN{FS=OFS=\"/\";filesuffix=\"genomic.fna.gz\"}{ftpdir=$0;asm=$10;file=asm\"_\"filesuffix;print file}\' " + prepDirectoryName + "ftpfilepaths" +  " > " + str(ftpfilepathsAwk))#download ftpfilepaths
    print("Downloading .fna.gz files")#print progress of the program
    with open(ftpDirPathsModFilename, "w") as ftpDirPathMod:#clear the ftpDirPathMod file if it exists
      ftpDirPathMod.write('')#write nothing to clear the file
    with open(ftpDirPathsFilename, "rw+") as ftpDirPath:#open the ftpDirpaths file
      for dirPathStringLine in ftpDirPath:#iterate through all of the lines in the ftpDirpaths file
        with open(ftpDirPathsModFilename, "a") as ftpDirPathMod:#open the newly created and cleared ftpDirpathsMod file in append mode 
          ftpDirPathMod.write(str(dirPathStringLine[26:]))#delete the ftp:// url 
          ftpDirPathMod.close()#close the modded ftpDirpathsMod file
      ftpDirPath.close()#close the ftoDirpath file
    with open(ftpDirPathsModFilename, "rw+") as ftpDirPath:#open the ftpdirpathsmod file that contains all of the modded directories to use in ftplib
      for dirPathStringLine in ftpDirPath:#iterate through all of the directories in ftpdirpathsmod
        dirList.append(str(dirPathStringLine.strip()))#add the dir name to dir list and clear the extra space to avoid garbage in strings(will get 500: become more creative error if not included)
        numDirs =+ 1#increment the number of directories in the ftpdirpathsmod file
    with open(ftpFilePathsFilename, "rw+") as ftpFilePath:#open the ftpfilepaths file to get the ftp file paths for ftplib
      for filePathStringLine in ftpFilePath:#iterate through all the files
        fileList.append(str(filePathStringLine.strip()))#add the file name to file list and clear the extra space to avoid garbage in strings(will get 500: become more creative error if not included)
        numFiles =+1#increment the number of files found in the ftpfilepaths file
    if numDirs != numFiles:#if the number of files found do not equal the number of directories found in ftpfilepaths and ftpDirPathsMod nanme
      print(str("Error, numDirs != numFiles"))#print an error, something went wrong
    for index, value in enumerate(dirList):#iterate through the list of directories
      ftp.cwd(str(dirList[index]))#change the ftp directory location 
      print(str(dirList[index]) + str(fileList[index]))#print file to be downloaded next
      ftp.retrbinary("RETR " + fileList[index], open(str(fnaFilesDirectoryName + "/" + fileList[index]), 'wb').write)#download the files to tree/inputDirectory/fnaFiles
    print("Download of files complete")#print progress of program

#Step 2: Decompress the fna.gz files from NCBI
#This will decompress all files that end in .fna.gz with gunzip
#Parameter inputDirectoryParam: the directory containing all of the respecive .fna.gz files to decompress
class Decompress():
  def run(self, inputDirectoryParam):
    print("Decompressing the files located in " + inputDirectoryParam)
    ext = ".fna.gz"#extension of .fna.gz
    for root, dir, files in os.walk(inputDirectoryParam, topdown=True):#traverse the directory containing the files of type .fna.gz
      for file in files:#check all files
        if file.endswith(ext):#if the file ends with .fna.gz
          print(str("gunzip -d " + str(inputDirectoryParam) + str(file)))#print progress of the program
          os.system(str("gunzip -d " + str(inputDirectoryParam) + str(file)))#decompress the file with gunzip
    print("Finished decompressing the .fna files")

#Step 3: Remove the first line and rename each file
#This will delete the first line and reanme the file according to the information contained in the fna file >NC000 Examplii Exli will rename to Examplii_Exli.fna
#This will override duplicate fnas with the same name(delete and add only new fna file)
#Parameter inputDirectoryParam: the directory containing all of the respective fna files to rename
class DeleteFirstLineAndRename():
  def run(self, inputDirectoryParam):
    print("Deleting the first lines and renaming the .fna files located in " + inputDirectoryParam)
    ext = ".fna"#extension of files to delete the first line and rename
    for root, dir, files in os.walk(inputDirectoryParam, topdown=True):#traverse input directory tree to rename 
      for file in files:
        if file.endswith(ext):#check if fna file
          with open(str(inputDirectoryParam) + str(file), "rw+") as currentFile:#open the file for reading and writing
            firstLineSplitList = currentFile.readline().strip().split()#split the first line that contains the genus and species inforamtion to rename the fna file
            #print(firstLineSplitList)
            firstLineSplitListString1 = str(firstLineSplitList[1])#Genus
            firstLineSplitListString2 = str(firstLineSplitList[2])#Species
            #'Nostoc_azollae' and [Cellbrivio],etc. modifications
            if(str(firstLineSplitListString1[:1]) == "[" or firstLineSplitListString1[:1] == "\'" or firstLineSplitListString1[:1] == "_"):#check first char
              firstLineSplitListString1 = firstLineSplitListString1[1:]#if ] , _  or \, delete
              if(str(firstLineSplitListString1[-1:]) == "]" or firstLineSplitListString1[-1:] == "\'" or firstLineSplitListString1[:1] == "_"):#check first char
               firstLineSplitListString1 = firstLineSplitListString1[:-1]#if [ , _ or \, delete
            if(str(firstLineSplitListString2[:1]) == "[" or firstLineSplitListString2[:1] == "\'" or firstLineSplitListString2[:1] == "_'"):#check last char
              firstLineSplitListString2 = firstLineSplitListString2[1:]#if ] , _ or \, delete
              if(str(firstLineSplitListString2[-1:]) == "]" or firstLineSplitListString2[-1:] == "\'" or firstLineSplitListString2[:1] == "_'"):#check first char
               firstLineSplitListString2 = firstLineSplitListString2[:-1]#if [ , _ or \, delete
            print(str(firstLineSplitListString1) + "_" + str(firstLineSplitListString2))#print current fna rename
            newFileNameString = str(firstLineSplitListString1) + "_" + str(firstLineSplitListString2)
            os.system("sed -i '' '1d' " + str(inputDirectoryParam) + str(file))#remove first line in place execution
            os.rename(str(inputDirectoryParam) + str(file), str(inputDirectoryParam) + str(newFileNameString) + ".fna")#rename the file
    print("Completed deleting the first lines and renaming the .fna files")

#Step 4: Create the reverse compliment of the fna file and concatinate to the forward fna file
#TODO: Modify to become in place
#This will create a reverse compliment of the dna(fna) files location in the input directory parameter and concatinate it to the forward of the dna file into a new file located in the tree/outputDirectoryParam/complete/complete/ directory
#Anilyze in C will use the reverse compliment to compute ANI
#Parameter inputDirectoryParam is the location of all of the forward .fna files
class CreateReverseComplimentAndAppendToForward():
  def run(self, inputDirectoryParam):
    print("Creating reverse compliment and forward")#print the progress of the program
    ext = ".fna"#extension of file to reverse compliment and add to forward
    for root, dir, files in os.walk(inputDirectoryParam, topdown=True):#iterate through the input directory
      for f in files:#check all the files
        if f.endswith(ext):#if the file ends with .fna
          currentFile = open(str(inputDirectoryParam) + str(f), "r")#open the current file in read mode
          seq = Seq(str(currentFile.read()))#read the file and create a sequence out of the string
          currentFile.close()#close the file
          currentFile = open(str(inputDirectoryParam) + str(f), "a")#open the current fule in append mode
          currentFile.write(str(seq.reverse_complement()))#write the reverse compliment 
          currentFile.close()#close the file
    print("Create the reverse compliment and append to the forward")
        
#TODO: Create an in place algortihm and add U, N RNA to DNA conversions that are not A,C,G and T
#Step 5: Convert the forward and reverse complimented file to a custom binary code
#This will turn the forward fna file and the reverse complimented fna file into a custom binary code of A(00), C(01), G(10), T(11) 
#Reformat and rename list of fna files
#Parameter inputDirectoryParam: location of forward and reverse complimented concatinated fna files
class ConvertToBinary(): 
  def run(self, inputDirectoryParam):
    print("Converting the .fna files located in " + inputDirectoryParam + " to binary")#print the progress of the program
    ext = ".fna"#extension of the files to be converted to binary
    for root, dir, files in os.walk(inputDirectoryParam, topdown=True):#iterate through tree/outputDirectory/binary/
      for file in files:#iterate through the files located in tree/outputDirectory/binary/
        if file.endswith(ext):#if file ends in .fna
          currentFile = open(str(inputDirectoryParam) + str(file), "r")#if it does, then open the file to read. This should delete all lines
          binaryString = ""#clear the binary string
          lines = currentFile.readlines()#read all of the lines
          currentFile.close()
          currentFile = open(str(inputDirectoryParam) + str(file), "w")#open the file in write mode and write the lines that do not contain >           
          for line in lines:#for every line in the current file
            for character in line:#for every character in the current line
              if character == "A" or character == "a":#if the character is A or a then 
                binaryString += "00"#append 00
              elif character == "C" or character == "c":#if the character is C then
                binaryString += "01"#append 01
              elif character == "G" or character == "g":#if the charcter is g
                binaryString += "10"#append 10
              elif character == "T" or character == "t":#if the character is t
                binaryString += "11"#append 11
              else:#probably a new line and if it is not then throw an error
                if character != "\n":#if the remaining unknown character is not a newline then print an error
                  print("error: " + str(character) + " in " + str(fileMod) + " is not a newline, A, a, C, c, G, g, or T, t")
            currentFile.write(str(binaryString))#write the binary string
            currentFile.close()#close the file
    print("Finished converting the .fna files to binary")#print the progress of the program

#Step 6:
#This will delete all lines that contain >NC. This is done because certain complete .fna files have many of these lines that need to be deleted
#Parameter inputDirectoryParam: the directory containing all of the respective fna files to delete the >NC lines
class DeleteLineInfo():
  def run(self, inputDirectoryParam):
    print("Deleting > lines from files located in " + str(inputDirectoryParam))#print progress of the program 
    ext = ".fna"#entension of the files to delete the >NC information
    for root, dir, files in os.walk(inputDirectoryParam, topdown=True):#traverse the input tree to find files to delete the >NC lines from
      for file in files:#check all files
        if file.endswith(ext):#check if the file ends with .fna
          currentFile = open(str(inputDirectoryParam) + str(file), "r")#if it does, then open the file to read. This should delete all lines
          lines = currentFile.readlines()#read all of the lines
          currentFile.close()#close the .fna file
          currentFile = open(str(inputDirectoryParam) + str(file), "w")#open the file in write mode and write the lines that do not contain >
          for line in lines:#check all lines
            if line[:1] != ">":#if a line starts with > then do not include that line in the new write
              currentFile.write(line)#only write lines that do not start with > to the file
          currentFile.close()#close the file for the next file or completion
    print("Finished deletion of > lines from files located in " + str(inputDirectoryParam) + "complete")#print progress of the program

#Optional Step 7:
#This will delete all new lines in the program to be able to format it cleanly later. Anilyze C program needs a defined set number of characters with a newline character on each line
#Parameter inputDirectoryParam: the directory of the files that contain the files to delete the new lines of
#Parameter outputDirectoryParam: the output directory to otuput the new files that do not have new lines
class DeleteNewLines():
  def run(self, inputDirectoryParam, outputDirectoryParam):
    ext = ".fna"
    print("Deleting the new lines located in " + inputDirectoryParam + " and outputting to " + outputDirectoryParam + "deletedNewLines/")#print program progress
    os.system("mkdir " + outputDirectoryParam + "deletedNewLines/")#
    for root, dir, files in os.walk(inputDirectoryParam + "deletedNewLines/", topdown=True):#
      for f in files:#iterate through all of the files in the tree/output_directory/complete/mod
        if f.endswith(ext):#check if the file ends with .fna
          os.system("tr -d '\n' < " + ((os.path.join(root, f))) + " > " + outputDirectoryParam + "deletedNewLines/" + str(f))#remove all new lines and cat to /tree/output_directory/complete/mod2/
    print("Finished deleting new lines" + outputDirectoryParam + "deletedNewLines/")

#Step 8:
#This will modify the line length to 70. Anilyze in C needs a constant line length with new lines
#Paramter inputDirectoryParam: the directory of the files that contain the files to modify the line length to seventy
#Parameter outputDirectoryParam: the directory of the modifed line length files
class ModifyLineLengthToSeventy():
  def run(self, inputDirectoryParam, outputDirectoryParam):
    ext = ".fna"
    print("Modifying the line lengths of the files located in " + inputDirectoryParam + " to 70 " + outputDirectoryParam)
    for root, dir, files in os.walk(inputDirectoryParam, topdown=True):#
      for f in files:#iterate through all of the files in the tree/output_directory/complete/mod
        if f.endswith(ext):#check if the file ends with .fna
          os.system("grep -oE '.{1,70}' " + inputDirectoryParam + str(f) + " > " + outputDirectoryParam + str(f))#reformat the lines to lengths of 70 characters per line and cat to /tree/output/complete/mod2/
    print("Modifying the line lengths of the files located in " + inputDirectoryParam + " to 70")
#TODO: Complete this

#Step 9:
#This will delete the leftover files that were completed in progress
#Parameter inputDirectoryParam: the directory containing all of the respective 
class DeletePreviousFiles():
  def run(self, inputDirectoryParam):
    shutil.rmtree('')#remove the tree specified
    '''
    shutil.rmtree(directoryRC)
    shutil.rmtree(directoryCompleteMOD)
    shutil.rmtree(directoryCompleteMOD2)
    #shutil.rmtree(directoryCompleteMOD3)
    os.system("mkdir " + outputDirectoryParam + "complete")
    os.system("mkdir " + outputDirectoryParam + "complete/MOD")
    os.system("mkdir " + outputDirectoryParam + "complete/MOD2")
    os.system("mkdir " + outputDirectoryParam + "complete/complete")
    os.system("mkdir " + outputDirectoryParam + "rc")
    '''
#Step Other: This is used if user downloads fasta files from NCBI. This was made to download all 16S and split into individual files
#Parameter inputFileParam: The fasta file to split
#Parameter outputFileParam: The directory to output the .fna file to output to 
class SplitFasta():
  def run(self, inputFileParam, outputDirectoryParam):
    x = 0 # set the file count at 0, this is used for duplicate file names
    #"/Users/jon/desktop/split/split16S"
    os.system("mkdir " + outputDirecotryParam)#create directory of output directory if it doesnt exist
    firstLine = True#boolean if it is the first line or not
    fnaName = ''#the name of the fna file
    prevFileName = ''#previous fna fname
    newFileName = ''#the new file name to be saved as
    #'/Users/jon/Desktop/split/sequence.fasta'
    with open(inputFileParam) as file:#open the input fasta file
      for line in file:#iterate through every line in the input fasta file
        if line.strip() == '':#clear the space characters
          firstLine = True#the first line is current line
          x += 1#increment count to be used for duplicates
        else:#not first line
          if firstLine is True:#check if the current line is a new line with information or a dna sequence
            fnaList = line.strip().split()#get the line and split into a list
            fnaName = fnaList[1] + "_" + fnaList[2]#rename the file using the list
            newFileName = outputDirectoryParam + str(fnaName) + ".fna"#
            if str(newFileName) == str(prevFileName):#do not delete duplicates
              newFileName = outputDirectoryParam + str(fnaName) + str(x) + ".fna"#add number to the end
            else:#else it is not a duplicate
              prevFileName = newFileName#save previous
              newFileName = outputDirectoryParam + str(fnaName) + ".fna"#output the split file to a new fna file
          else: #if not the first line
            with open(newFileName, 'a') as newFile:#append the line to the file
              newFile.write(line.strip())#write the line without space or garbage characters
          firstLine = False#not first line
    file.close()#close the current file
#TODO: Check end of inputArg for /
def main(argv):
  inputArg = ''
  outputArg = ''
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
      sys.exit()
    elif opt in ("-tree_i", "--inDir"):
      split_i = False
      inputArg = arg
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
     split = SplitFasta()
     split.run(inputArg, outputArg)
  if i is True:
    print 'Input file is "', inputArg
    print 'Output file is "', outputArg
    downloadFiles = DownloadFiles()
    decompress = Decompress()
    deleteFirstLineAndRename  = DeleteFirstLineAndRename()
    deleteLineInfo = DeleteLineInfo()
    createReverseComplimentAndAppendToForward = CreateReverseComplimentAndAppendToForward()
    convertToBinary = ConvertToBinary()
    deleteNewLines = DeleteNewLines()
    modifyLineLengthToSeventy = ModifyLineLengthToSeventy()
    #splitFasta = SplitFasta():

    #downloadFiles.run(inputArg)
    #decompress.run(inputArg)
    #deleteFirstLineAndRename.run(inputArg)
    #deleteLineInfo.run(inputArg)
    #createReverseComplimentAndAppendToForward.run(inputArg)
    #convertToBinary.run(inputArg)
    #deleteNewLines.run(inputArg, outputArg)
    #modifyLineLengthToSeventy.run(inputArg, outputArg)
    #splitFasta.run()
#main  
if __name__=='__main__':
  main(sys.argv[1:])
