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
def downloadFiles(inputDirectoryParam, testParam):
  print("downloadFiles running")#print progress of program
  currentDirectoryPath = str(os.getcwd())
  email = 'jonbeacher@gmail.com'#email to login with refseq to 
  prepDirectoryName = "prep"#name of the directory that will contain ftpDirPaths, ftpDirPathsMod, ftpFilePaths and assembly_summary.txt files
  fnaFilesDirectoryName = "fnaFiles"
  fnaFilesDirectoryPath = str(currentDirectoryPath) + "/" + str(fnaFilesDirectoryName) #name of the directory that will contain all of the .fna.gz files from refseq
  prepDirectoryPath = str(currentDirectoryPath) + "/" + str(prepDirectoryName) + "/"
  ftpDirPathsPathAndFilename = str(prepDirectoryPath) + "ftpDirPaths"#name of the file that will contain a list of all the file paths used to download using ftp
  ftpDirPathsModPathAndFilename = str(prepDirectoryPath) + "ftpDirPathsMod"#name of the modded file that will contain a list of all the modded directory paths used to download using ftplib
  ftpFilePathsPathAndFilename = str(prepDirectoryPath) + "ftpFilePaths"#name of the file that will contain a list of all the file paths used to download using ftplib
  mkdirCommandFnaFilesDirectory = "mkdir " + str(fnaFilesDirectoryName)#create directory of the .fna.gz files download location
  mkdirCommandPrepFilesDirectory = "mkdir " + str(prepDirectoryName) #create directory of the ftpDirPaths, ftpDirPathsMod, ftpFilePaths and assembly_summary.txt files
  numDirs = 0#number of directories contained in the ftpDirPathsMod file
  numFiles = 0#number of directories contained in the ftpFilePaths file
  dirList = []#python list containing the name of the directories used to download using ftp from ftpDirPathsMod
  fileList = []#python list containing the name of the files used to download using ftp from ftoFilePaths
  print("Creating output directories")#print the progress of the program
  if not os.path.exists(fnaFilesDirectoryPath):#check if the directory that will contain all of the .fna.gz files exists
    os.system(mkdirCommandFnaFilesDirectory)#if it does not exist, create the directory
  else:#the directory already exists and this program will delete the contents of the directory
    os.system("rm -r " + fnaFilesDirectoryName)#remove the contents of the directory
    os.system(mkdirCommandFnaFilesDirectory)#create the directory that will contain all of the .fna.gz files
  if not os.path.exists(prepDirectoryPath):#check if the directory that will contain the ftpDirPaths, ftpDirPathsMod, ftpFilePaths and assembly_summary.txt files
    os.system(mkdirCommandPrepFilesDirectory)#if the directory does not exist, then create it
  else:#the directory has already been created and will be deleted
    os.system("rm -r " + prepDirectoryPath)#remove the directory
    os.system(mkdirCommandPrepFilesDirectory)#create the directory
  ftp = ftplib.FTP('ftp.ncbi.nlm.nih.gov')#set up the ftp connection to NCBI
  ftp.login('anonymous', email)#login with username of anonymous and the email given earlier in the program
  #Awk commands and more details can be found at https://www.ncbi.nlm.nih.gov/genome/doc/ftpfaq/#asmsumfiles
  ftp.cwd("/genomes/refseq/bacteria/")#change the ftp directory to the bacteria genome download locations in refseq
  print("Downloading assembly_summary.txt and executing awk commands")#print the progress of the program
  os.system(ftp.retrbinary("RETR assembly_summary.txt", open(prepDirectoryPath + "assembly_summary.txt", 'wb').write))#download the assembly summary file
  os.system("awk -F \"\t\" \'$12==\"Complete Genome\" && $11==\"latest\"{print $20}\' " + prepDirectoryPath + "assembly_summary.txt > " + prepDirectoryPath + "ftpdirpaths")#download ftpdirpaths
  os.system("awk \'BEGIN{FS=OFS=\"/\";filesuffix=\"genomic.fna.gz\"}{ftpdir=$0;asm=$10;file=asm\"_\"filesuffix;print file}\' " + prepDirectoryPath + "ftpdirpaths" +  " > " + prepDirectoryPath + "ftpfilepaths") #download ftpfilepaths
  print("Downloading .fna.gz files")#print progress of the program
  with open(ftpDirPathsModPathAndFilename, "w") as ftpDirPathMod:#clear the ftpDirPathMod file if it exists
    ftpDirPathMod.write('')#write nothing to clear the file
  with open(ftpDirPathsPathAndFilename, "r") as ftpDirPath:#open the ftpDirpaths file
    for dirPathStringLine in ftpDirPath:#iterate through all of the lines in the ftpDirpaths file
      with open(ftpDirPathsModPathAndFilename, "a") as ftpDirPathMod:#open the newly created and cleared ftpDirpathsMod file in append mode 
        ftpDirPathMod.write(str(dirPathStringLine[26:]))#delete the ftp:// url 
        ftpDirPathMod.close()#close the modded ftpDirpathsMod file
    ftpDirPath.close()#close the ftoDirpath file
  with open(ftpDirPathsModPathAndFilename, "r") as ftpDirPath:#open the ftpdirpathsmod file that contains all of the modded directories to use in ftplib
    for dirPathStringLine in ftpDirPath:#iterate through all of the directories in ftpdirpathsmod
      dirList.append(str(dirPathStringLine.strip()))#add the dir name to dir list and clear the extra space to avoid garbage in strings(will get 500: become more creative error if not included)
      numDirs =+ 1#increment the number of directories in the ftpdirpathsmod file
  with open(ftpFilePathsPathAndFilename, "r") as ftpFilePath:#open the ftpfilepaths file to get the ftp file paths for ftplib
    for filePathStringLine in ftpFilePath:#iterate through all the files
      fileList.append(str(filePathStringLine.strip()))#add the file name to file list and clear the extra space to avoid garbage in strings(will get 500: become more creative error if not included)
      numFiles =+1#increment the number of files found in the ftpfilepaths file
  if numDirs != numFiles:#if the number of files found do not equal the number of directories found in ftpfilepaths and ftpDirPathsMod nanme
    print(str("Error, numDirs != numFiles"))#print an error, something went wrong
  if testParam is True:
    ftp.cwd(str(dirList[0]))#change the ftp directory location 
    print(str(dirList[0]) + str(fileList[0]))#print file to be downloaded next
    ftp.retrbinary("RETR " + fileList[0], open(str(fnaFilesDirectoryPath + "/" + fileList[0]), 'wb').write)#download the files to tree/inputDirectory/fnaFiles  
  else:
    for index, value in enumerate(dirList):#iterate through the list of directories
      ftp.cwd(str(dirList[index]))#change the ftp directory location 
      print(str(dirList[index]) + str(fileList[index]))#print file to be downloaded next
      ftp.retrbinary("RETR " + fileList[index], open(str(fnaFilesDirectoryPath + "/" + fileList[index]), 'wb').write)#download the files to tree/inputDirectory/fnaFiles
  ftp.close()
  print("Download of files complete")#print progress of program

#Step 2: Decompress the fna.gz files from NCBI
#This will decompress all files that end in .fna.gz with gunzip
#Parameter inputDirectoryParam: the directory containing all of the respecive .fna.gz files to decompress
def decompress(inputDirectoryParam):
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
def deleteFirstLineAndRename(inputDirectoryParam):
  print("Deleting the first lines and renaming the .fna files located in " + inputDirectoryParam)
  ext = ".fna"#extension of files to delete the first line and rename
  for root, dir, files in os.walk(inputDirectoryParam, topdown=True):#traverse input directory tree to rename 
    for file in files:
      if file.endswith(ext):#check if fna file
        with open(str(inputDirectoryParam) + str(file), "r") as currentFile:#open the file for reading and writing
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

#Step ?: Rename each file
#This will rename the .fna files by deleting the [] or '' characters in the .fna files
#This will override duplicate fna files
#Parameter inputDirectoryParam: the directory containing all of the respective fna files to rename
def modifyFileNames(inputDirectoryParam):
  print("Modifying the names of the .fna files located in " + inputDirectoryParam)
  ext = ".fna"#extension of files to delete the first line and rename
  for root, dir, files in os.walk(inputDirectoryParam, topdown=True):#traverse input directory tree to rename 
    for file in files:
      if file.endswith(ext):#check if fna file
        with open(str(inputDirectoryParam) + str(file), "r") as currentFile:#open the file for reading and writing
          firstLineSplitList = os.path.basename(file).strip()
          print(firstLineSplitList)
          firstLineSplitListString1 = str(firstLineSplitList)#Genus
          #'Nostoc_azollae' and [Cellbrivio],etc. modifications
          if(str(firstLineSplitListString1[:1]) == "[" or firstLineSplitListString1[:1] == "\'" or firstLineSplitListString1[:1] == "_"):#check first char
            firstLineSplitListString1 = firstLineSplitListString1[1:]#if ] , _  or \, delete
            if(str(firstLineSplitListString1[-1:]) == "]" or firstLineSplitListString1[-1:] == "\'" or firstLineSplitListString1[:1] == "_"):#check first char
              firstLineSplitListString1 = firstLineSplitListString1[:-1]#if [ , _ or \, delete
          newFileNameString = str(firstLineSplitListString1)
          os.rename(str(inputDirectoryParam) + str(file), str(inputDirectoryParam) + str(newFileNameString))#rename the file
  print("Completed modfying the .fna file names")

#Step 4: Create the reverse compliment of the fna file and concatinate to the forward fna file
#TODO: Modify to become in place
#This will create a reverse compliment of the dna(fna) files location in the input directory parameter and concatinate it to the forward of the dna file into a new file located in the tree/outputDirectoryParam/complete/complete/ directory
#Anilyze in C will use the reverse compliment to compute ANI
#Parameter inputDirectoryParam is the location of all of the forward .fna files
def createReverseComplimentAndAppendToForward(inputDirectoryParam):
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
def convertToBinary(inputDirectoryParam):
  print("Converting the .fna files located in " + inputDirectoryParam + " to binary")#print the progress of the program
  ext = ".fna"#extension of the files to be converted to binary
  for root, dir, files in os.walk(inputDirectoryParam, topdown=True):#iterate through tree/outputDirectory/binary/
    for file in files:#iterate through the files located in tree/outputDirectory/binary/
      if file.endswith(ext):#if file ends in .fna
        currentFile = open(str(inputDirectoryParam) + str(file), "r")#if it does, then open the file to read. This should delete all lines
        lines = currentFile.readlines()#read all of the lines
        currentFile.close()
        binaryString = ""#clear the binary string
        currentFile2 = open(str(inputDirectoryParam) + str(file), "w")#open the file in write mode and write the lines that do not contain >           
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
                print("error: " + str(character) + " in " + str(file) + " is not a newline, A, a, C, c, G, g, or T, t")
        currentFile2.write(str(binaryString))#write the binary string
        currentFile2.close()#close the file
  print("Finished converting the .fna files to binary")#print the progress of the program

#Step 6:
#This will delete all lines that contain >NC. This is done because certain complete .fna files have many of these lines that need to be deleted
#Parameter inputDirectoryParam: the directory containing all of the respective fna files to delete the >NC lines
def deleteLineInfo(inputDirectoryParam):
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

#Step 7:
#This will modify the line length to 70. Anilyze in C needs a constant line length with new lines
#Paramter inputDirectoryParam: the directory of the files that contain the files to modify the line length to seventy
#Parameter outputDirectoryParam: the directory of the modifed line length files
def modifyLineLengthToSeventy(inputDirectoryParam, outputDirectoryParam):
  ext = ".fna"
  print("Modifying the line lengths of the files located in " + inputDirectoryParam + " to 70 >" + outputDirectoryParam + "correctlyFormatted/")
  os.system("mkdir " + outputDirectoryParam + "/correctlyFormatted")#
  if not os.path.exists(outputDirectoryParam):
    os.system("mkdir " + str(outputDirectoryParam))
  for root, dir, files in os.walk(inputDirectoryParam, topdown=True):#
    for f in files:#iterate through all of the files in the tree/output_directory/complete/mod
      if f.endswith(ext):#check if the file ends with .fna
        #print("grep -oE '.{1,70}' " + inputDirectoryParam + str(f) + " > " + outputDirectoryParam + "/Seventy" + str(f))
        os.system("grep -oE '.{1,70}' " + inputDirectoryParam + str(f) + " > " + outputDirectoryParam + "correctlyFormatted/" + str(f))#reformat the lines to lengths of 70 characters per line and cat to /tree/output/complete/mod2/
  print("Completed modifying the line lengths of the files located in " + inputDirectoryParam + " to 70")

#Step 8:
#This will delete the leftover files that were completed in progress
#Parameter inputDirectoryParam: the directory containing all of the respective 
def deletePreviousFiles(inputDirectoryParam):
  shutil.rmtree(inputDirectoryParam)#remove the tree specified

#Step Other: This is used if user downloads fasta files from NCBI. This was made to download all 16S and split into individual files
#Parameter inputFileParam: The fasta file to split
#Parameter outputFileParam: The directory to output the .fna file to output to 
def splitFasta(inputFileParam):
  x = 0 # set the file count at 0, this is used for duplicate file names
  #"/Users/jon/desktop/split/split16S"
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
          newFileName = inputDirectoryParam + str(fnaName) + ".fna"#
          if str(newFileName) == str(prevFileName):#do not delete duplicates
            newFileName = inputDirectoryParam + str(fnaName) + str(x) + ".fna"#add number to the end
          else:#else it is not a duplicate
            prevFileName = newFileName#save previous
            newFileName = inputDirectoryParam + str(fnaName) + ".fna"#output the split file to a new fna file
        else: #if not the first line
          with open(newFileName, 'a') as newFile:#append the line to the file
            newFile.write(line.strip())#write the line without space or garbage characters
        firstLine = False#not first line
  file.close()#close the current file
#TODO: Check end of inputArg for /

#Step Other: This is used if user downloads fasta files from NCBI. This was made to download all 16S and split into individual files
#Parameter inputFileParam: The fasta file to split
#Parameter outputFileParam: The directory to output the .fna file to output to 
def splitFastaForComplete(inputDirectoryParam):
  x = 0 # set the file count at 0, this is used for duplicate file names
  #"/Users/jon/desktop/split/split16S"
  firstLine = True#boolean if it is the first line or not
  complete = False
  fnaName = ''#the name of the fna file
  prevFileName = ''#previous fna fname
  newFileName = ''#the new file name to be saved as
  #'/Users/jon/Desktop/split/sequence.fasta'
  ext = ".fasta"#extension of the files to be converted to binary
  #print(inputDirectoryParam)
  for root, dir, files in os.walk(inputDirectoryParam, topdown=True):#iterate through tree/outputDirectory/binary/
    for currentFile in files:
      if currentFile.endswith(ext):
        #print(str(currentFile))
        with open(inputDirectoryParam + currentFile) as file:#open the input fasta file
          for line in file:#iterate through every line in the input fasta file
            #print(line.strip())
            if line.strip() == '':#clear the space characters
              firstLine = True#the first line is current line
              x += 1#increment count to be used for duplicates
            else:#not first line
              if firstLine is True:#check if the current line is a new line with information or a dna sequence
                fnaList = line.strip().split()#get the line and split into a list
                #print(fnaList)
                for index, value in enumerate(fnaList):#iterate through the list of directories
                  #print(str(fnaList[index]))
                  if str(fnaList[index]) == "complete":
                    #print("complete")
                    fnaName = fnaList[1] + "_" + fnaList[2]#rename the file using the list
                    newFileName = inputDirectoryParam + str(fnaName) + ".fna"#
                    if str(newFileName) == str(prevFileName):#do not delete duplicates
                      newFileName = inputDirectoryParam + str(fnaName) + "_" + str(x) + ".fna"#add number to the end
                    else:#else it is not a duplicate
                      prevFileName = newFileName#save previous
                      newFileName = inputDirectoryParam + str(fnaName) + ".fna"#output the split file to a new fna file
                    complete = True
                  elif str(fnaList[index]) == "incomplete" or str(fnaList[index]) == "partial":
                    #print("partial")
                    complete = False
              else: #if not the first line
                pass
                if complete is True:
                  with open(newFileName, 'a') as newFile:#append the line to the file
                    newFile.write(line.strip())#write the line without space or garbage characters
              firstLine = False#not first line            
    file.close()#close the current file