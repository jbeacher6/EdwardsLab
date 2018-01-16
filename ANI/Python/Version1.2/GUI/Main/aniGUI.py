from __future__ import division
import Tkinter, Tkconstants, tkFileDialog
from Tkinter import *
import os
from collections import OrderedDict
import sys
import subprocess
import fileinput
import shutil
import datetime
from datetime import datetime
import csv
'''
This class will concatinate many .fna files into one .fna file
Example:
user/directory1/file1.ext
user/directory1/file2.ext
Will turn directory1 into
user/directory1/directory1.ext
Where directory1 is the result of cat file1.ext file2.ext > dictionary1.ext
If there is more than one .fna file, it will leave it untouched
Example:
user/directory2/file.ext will remain unchanged, where dictionary2 has only file.ext
'''
class ConcatinatingFNAFiles():
  def run(self):
    directory = TkANI.allFnaDirectoryLocationString
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
            rmFirstLineCommand = "sed -i '' '1d' " + catFileTo
            os.system(rmFirstLineCommand)
      if uniqueFiles:
        string1 = ''.join(listOfFNAfiles)

        catCommand = "cat " + string1 + " > " + newFNAfileName2
        os.system(catCommand)
        '''
        mkdirCommand = "mkdir" + " " + TkANI.percentDirectoryLocationString
        os.system(mkdirCommand)
        '''
        rmNewLinesCommand = "tr -d '\n' < " + newFNAfileName2 + " > " + newFNAfileName3
        os.system(rmNewLinesCommand)

        grepLinesCommand = "grep -oE '.{1,70}' " + newFNAfileName3 + " > " + TkANI.percentDirectoryLocationString + "/" + base + ext
        os.system(grepLinesCommand)

        rmCommand = "rm " + string1
        os.system(rmCommand)

        rmCommand2 = "rm " + newFNAfileName2
        os.system(rmCommand2)

        rmCommand3 = "rm " + newFNAfileName3
        os.system(rmCommand3)

        listOfFNAfiles = []
        catCommand = None
        newFNAfileName = None
        string1 = None
    listOfDirectoriesWithMultipleFNAfilesNoRepeats = None
    print("ConcatinatingFNAFiles complete")

'''
This class programmically moves(cuts[os.rename] or copies[catCommand]) files to another location
Example Input:
Users/all.fna/directory1/directory1.fna
Users/all.fna/directory2/directory2.fna
Example Output:
Users/newDirectory/directory1.fna
Users/newDirectory/directory2.fna
This class is intended and has only been tested after running classes:
concatinatingFNAFiles(): and class ChangeFilesToDirectoryName(): 

Current bug: Will throw an os error if ran twice(Errno 21: Is a directory:)
A string output is thrown if this bug is reproduced so the program doesn't crash
'''
class CopyFiles():
  def run(self, moveFilesToDirectoryParam):
    if(moveFilesToDirectoryParam == ""):
      print(str("Error: Cannot copy, one of the directory entry is nil"))
      return
    directory = TkANI.allFnaDirectoryLocationString
    # moveToDirectory = TkANI.blastDirectoryLocationString
    moveToDirectory = moveFilesToDirectoryParam
    if os.path.exists(moveToDirectory):
      rmCommand = "rm " + moveToDirectory
      print(rmCommand)
      # print(str("Error: " + moveFilesToDirectoryParam + " already exists, please delete and try again"))
      return
    else:
      print("Copying files to " + str(moveFilesToDirectoryParam))
      shutil.copytree(directory, moveToDirectory)
    print("Copying Blast files completed!")

class ReformatTextFileForConversion():
  roundToPowerOfN = 0
  genome1 = ""
  species1 = ""
  genome2 = ""
  species2 = ""
  percent2 = .42
  percent3 = 42
  
  def run(self):
    with open(str(TkANI.percentDirectoryLocationString) + "/outputANIFile.txt") as infile:
      reader = csv.reader(infile)
      reformattedANIFile = open(str(TkANI.percentDirectoryLocationString) + "/reformattedOutputANIFile.txt", "w")
      for line in enumerate(reader):
        x = line[1][0].split("_")
        for i, j in enumerate(x):
          if i == 1:
            self.genome1 = x[i]
          if i == 3:
            self.species1 = x[i]
          if i == 10:
            self.genome2 = x[i]
          if i == 11:
            self.species2 = x[i]
          if i == 14:
            try: 
              float(x[i])
              self.percent2 = round(float(x[i]), self.roundToPowerOfN)
              self.percent3 = int(self.percent2)
            except:
              pass
          if i == 15:
            try:
              float(x[i])
              self.percent2 = round(float(x[i]), self.roundToPowerOfN)
              self.percent3 = int(self.percent2)
            except:
              pass
          if i == 16:
            try:
              float(x[i])
              self.percent2 = round(float(x[i]), self.roundToPowerOfN)
              self.percent3 = int(self.percent2)
            except:
              pass
          if i == 17:
            try:
              float(x[i])
              self.percent2 = round(float(x[i]), self.roundToPowerOfN)
              self.percent3 = int(self.percent2)
            except:
              pass
          if i == 18:
            try:
              float(x[i])
              self.percent2 = round(float(x[i]), self.roundToPowerOfN)
              self.percent3 = int(self.percent2)
            except:
              pass
        print(str(self.genome1 + " " + self.species1 + " " + self.genome2 + " " + self.species2 + " " + str(self.percent3)))
        writeString = str(self.genome1 + " " + self.species1 + " " + self.genome2 + " " + self.species2 + " " + str(self.percent3) + "\n")
        reformattedANIFile.write(writeString)
      reformattedANIFile.close()
      print("ReformatTextFileForConversion(): completed!")  

class RemoveDuplicates():
  def run(self):
    listOfLines = []
    y = ""
    list2 = ""
    with open(str(TkANI.percentDirectoryLocationString) + "/reformattedOutputANIFile.txt") as infile:
      reader = csv.reader(infile)
      reformattedANIFile = open(str(TkANI.percentDirectoryLocationString) + "/removedDuplicatesOutputANIFile2.txt", "w")
      for line in enumerate(reader):
        x = line[1][0].split(" ")
        for i, j in enumerate(x):
          if(i == 0):
            y = ""
          y = y + " " + str(j)
          if(i == 4):
            listOfLines.append(y)
      list2 = list(OrderedDict.fromkeys(listOfLines))
      for i, j in enumerate(list2):
        writeString = str(j) + "\n"
        reformattedANIFile.write(writeString)
      # print(list2)
      reformattedANIFile.close()
    print("RemoveDuplicates(): completed!")

'''
This class formats the text file outputted from BlastANI(): and MummersANI(): to JSON seed. This is done to be able to input into an iOS project for Core Data or another project utilizing JSON to read the data
This class is intended and will only be tested after running classes:
class ConcatinatingFNAFiles(): , class ChangeFilesToDirectoryName():, class CdFiles():
and
Class AllDeltaFilesMummer(): and class MummersANI(): 
and / or 
class AllOutFilesBlast(); and class BlastANI():
'''
class CreateJSONseed():
  def run(self):
    print("not complete")
'''
This class formats the text file outputted from BlastANI(): and MummersANI(): to SQL lite statement. This is done to enable an Android application or another project utilizing SQL lite to read the data
This class is intended and will only be tested after running classes:
class ConcatinatingFNAFiles(): , class ChangeFilesToDirectoryName():, class CdFiles():
'''
class CreateSQLliteCreationStatement():
  def run(self):
    print("not complete")
'''
This class is the GUI class for the application
When the user presses run, it will gather the inputs and execute def run(self):, which calls instances of other classes
To start this GUI, the user should have Python 2.7 installed and run python thisFileName.py and a Tkinter generated GUI should appear
'''
class TkANI(Tkinter.Frame):
  # Directory Location Vars
  allFnaDirectoryLocationString = ""
  percentDirectoryLocationString = ""
  def __init__(self, root):
    # Initialize classes GUI will use
    self.concatinatingFNAFiles = ConcatinatingFNAFiles()
    self.copyFilesInstance = CopyFiles()
    self.reformatTextFileForConversion = ReformatTextFileForConversion()
    self.removeDuplicates = RemoveDuplicates()
  	# GUI inits
    Tkinter.Frame.__init__(self, root)
    self.configure(background='black')
    yPaddingAmount = 2
    xPaddingAmount = 2
    entryHexColor = "#B20000"
    entryWidth = 45
    buttonWidth = 45
    readMeButtonWidth = 15
    runButtonWidth = 91
    checkBoxWidth = 37
    # Checkbox Value Variables
    self.completeCheckboxValue = IntVar()
    self.cdAllCheckboxValue = IntVar()
    self.sqlLiteCheckboxValue = IntVar()
    self.jsonCheckboxValue = IntVar()
     # Defining query directory buttons
    Tkinter.Button(self, text='Location Of all.fna Directory', command=self.askAllFnaDirectory, width=buttonWidth).grid(row=1, column=1, pady=(yPaddingAmount, yPaddingAmount))
    Tkinter.Button(self, text='Percent ANI Output Results Directory', command=self.askPercentANIOutputDirectory, width=buttonWidth).grid(row=2, column=1, pady=(yPaddingAmount, yPaddingAmount))
     # Define run button
    Tkinter.Button(self, text='Run', command=self.run, width=runButtonWidth).grid(row=3, column=1, columnspan=2, pady=(yPaddingAmount, yPaddingAmount))
     # Define directory text entries
    self.allFnaEntry = Tkinter.Entry(self, bg=entryHexColor, fg="white", width=entryWidth)
    self.allFnaEntry.grid(row=1, column=2, padx=(xPaddingAmount, xPaddingAmount))
    self.percentEntry = Tkinter.Entry(self, bg=entryHexColor, fg="white", width=entryWidth)
    self.percentEntry.grid(row=2, column=2, padx=(xPaddingAmount, xPaddingAmount))
    '''
    Define checkboxes
    1 is an enabled checkbox, 0 is an enabled checkbox
    '''
    self.completeCheckbox = Tkinter.Checkbutton(self, variable=self.completeCheckboxValue, onvalue=1, offvalue=0, text ='Reformat, rename and concatenate', width=checkBoxWidth)
    self.completeCheckbox.grid(row=1, column=3)
    self.sqlLiteCheckbox = Tkinter.Checkbutton(self, variable=self.sqlLiteCheckboxValue, onvalue=1, offvalue=0, text ='Create output for SQLite', width=checkBoxWidth)
    self.sqlLiteCheckbox.grid(row=2, column=3)
    self.jsonCheckbox = Tkinter.Checkbutton(self, variable=self.jsonCheckboxValue, onvalue=1, offvalue=0, text ='Create output for JSON', width=checkBoxWidth)
    self.jsonCheckbox.grid(row=3, column=3)
    # Set checkbox default values
    self.completeCheckboxValue.set(1)
    self.sqlLiteCheckboxValue.set(0)
    self.jsonCheckboxValue.set(0)
    # Remove for generic program
    self.allFnaEntry.insert(0, str("/Users/jon/Desktop/allFNA"))
    self.percentEntry.insert(0, str("/Users/jon/Desktop/allFNA/1Complete"))
   # Queries directory containing files respective to BLAST
  def askAllFnaDirectory(self):
     askAllFnaDirectoryLocation = tkFileDialog.askdirectory()
     if askAllFnaDirectoryLocation:
        self.allFnaEntry.delete(0, 'end')
        self.allFnaEntry.insert(0, str(askAllFnaDirectoryLocation))
     return
   #  Queries directory containing files to dump output files
  def askPercentANIOutputDirectory(self):
     percentANIDirectoryLocation = tkFileDialog.askdirectory()
     if percentANIDirectoryLocation:
        self.percentEntry.delete(0, 'end')
        self.percentEntry.insert(0, str(percentANIDirectoryLocation))
     return
   # Print all the values to be saved from the 
  def printTkValues(self):
   print(str(TkANI.allFnaDirectoryLocationString))
   print(str(TkANI.percentDirectoryLocationString))
   # Save entry values to be read from other classes
  def saveTkValues(self):
   TkANI.allFnaDirectoryLocationString = self.allFnaEntry.get()
   TkANI.percentDirectoryLocationString = self.percentEntry.get()
  '''
  Main Buddy
  '''
   # Main from the GUI
  def run(self):
    print("Program started running at time: " + str(datetime.now()))
    self.saveTkValues()
    if self.completeCheckboxValue.get() == 1:
      self.concatinatingFNAFiles.run()
    if self.sqlLiteCheckboxValue.get() == 1:
      print("s1")
      self.reformatTextFileForConversion.run()
    if self.jsonCheckboxValue.get() == 1:
      print("j1")
    print("Program completed at time: " + str(datetime.now()))

if __name__=='__main__':
   root = Tkinter.Tk()
   root.title("SDSU Blast and MUMMer Average Nucleotide Algorithms GUI v1.0")
   TkANI(root).pack()
   root.mainloop()
