from anilyze import downloadFiles
from anilyze import decompress
from anilyze import deleteFirstLineAndRename
from anilyze import deleteLineInfo
from anilyze import createReverseComplimentAndAppendToForward
from anilyze import convertToBinary
from anilyze import modifyLineLengthToSeventy
import sys
import getopt
import os
import filecmp
import ftplib#library used to download files using ftp
import os#library used to execute system commands
import sys#library used to execute system commands
#test
import unittest
import md5
import hashlib
import filecmp

class AnilyzeTest(unittest.TestCase):
  def createDirectory(self, directoryName):
    if not os.path.exists(directoryName):
      os.system("mkdir " + str(directoryName))
    else:
      os.system("rm -r " + str(directoryName))
      os.system("mkdir " + str(directoryName))
  
  def testDownloadFiles(self):
    downloadFiles(os.getcwd() + "/fnaFiles/", True)
    self.assertEqual(str(hashlib.md5(open(str(os.getcwd() + "/fnaFiles/GCF_000010525.1_ASM1052v1_genomic.fna.gz"), "rb").read()).hexdigest()), "417d852fbfbb7a37e23fd6d6d4f9d60d")

  def testDecompress(self):
    downloadFiles(os.getcwd() + "/fnaFiles/", True)
    decompress(str(os.getcwd()) + "/fnaFiles/")
    string = str(os.getcwd()+ "/fnaFiles/GCF_000010525.1_ASM1052v1_genomic.fna") 
    self.assertTrue(os.path.isfile(string))

  def setupTestDeleteFirstLineAndRename(self):
    self.createDirectory(str(os.getcwd()) + "/fnaFiles")
    testFile = open(str(os.getcwd()) + "/fnaFiles/testDeleteFirstLineAndRename.fna", "w")
    testFile.write(">NC00 Example Bacterii\nACGT\n")
    testFile.close()
    self.createDirectory(str(os.getcwd()) + "/correct")
    correctFile = open(str(os.getcwd()) + "/correct/" + "Example_Bacterii.fna", "w")
    correctFile.write("ACGT\n")
    correctFile.close()
  
  def testDeleteFirstLineAndRename(self):
    self.setupTestDeleteFirstLineAndRename()
    currentDirectory = str(os.getcwd())
    deleteFirstLineAndRename(currentDirectory + "/fnaFiles/")
    #self.assertTrue(os.path.exists(currentDirectory + "/fnaFiles/Example_Bacterii.fna"))
    self.assertTrue(filecmp.cmp(currentDirectory + "/fnaFiles/Example_Bacterii.fna", currentDirectory + "/correct/Example_Bacterii.fna", shallow=False))
  
  def setupDeleteLineInfo(self):
    self.createDirectory(str(os.getcwd()) + "/fnaFiles")
    currentDirectory = os.getcwd()
    testFile = open(str(os.getcwd()) + "/fnaFiles/Example_Bacterii.fna", "w")
    testFile.write(">NC00 Example Bacterii\nAAAA\n>NC01 Example Bacterii\nCCCC\n>NC02 Example Bacterii\nGGGG\n>NC03 Example Bacterii\nTTTT\n")
    testFile.close()
    self.createDirectory(str(os.getcwd()) + "/correct")
    correctFile = open(str(os.getcwd()) + "/correct/" + "Example_Bacterii.fna", "w")
    correctFile.write("AAAA\nCCCC\nGGGG\nTTTT\n")
    correctFile.close()

  def testDeleteLineInfo(self):
    self.setupDeleteLineInfo()
    currentDirectory = os.getcwd()
    deleteLineInfo(str(os.getcwd()) + "/fnaFiles/")
    self.assertTrue(filecmp.cmp(currentDirectory + "/fnaFiles/Example_Bacterii.fna", currentDirectory + "/correct/Example_Bacterii.fna", shallow=False))
  def setupTestCreateReverseComplimentAndAppendToForward(self):
    self.createDirectory(str(os.getcwd()) + "/fnaFiles")
    testFile = open(str(os.getcwd()) + "/fnaFiles/testCreateReverseComplimentAndAppendToForward.fna", "w")
    testFile.write("GCAT")
    testFile.close()
    self.createDirectory(str(os.getcwd()) + "/correct")
    correctFile = open(str(os.getcwd()) + "/correct/testCreateReverseComplimentAndAppendToForward.fna", "w")
    correctFile.write("GCATATGC")
    correctFile.close()

  def testCreateReverseComplimentAndAppendToForward(self):
    self.setupTestCreateReverseComplimentAndAppendToForward()
    currentDirectory = os.getcwd()
    createReverseComplimentAndAppendToForward(str(os.getcwd()) + "/fnaFiles/")
    self.assertTrue(filecmp.cmp(currentDirectory + "/fnaFiles/testCreateReverseComplimentAndAppendToForward.fna", currentDirectory + "/correct/testCreateReverseComplimentAndAppendToForward.fna", shallow=False))
  #
  
  def setupTestConvertToBinary(self):
    self.createDirectory(str(os.getcwd()) + "/fnaFiles")
    testFile = open(str(os.getcwd()) + "/fnaFiles/testConvertToBinary.fna", "w")
    testFile.write("ACGT")
    testFile.close()
    self.createDirectory(str(os.getcwd()) + "/correct")
    correctFile = open(str(os.getcwd()) + "/correct/testConvertToBinary.fna", "w")
    correctFile.write("00011011")
    correctFile.close()

  def testConvertToBinary(self):
    self.setupTestConvertToBinary()
    currentDirectory = str(os.getcwd())
    convertToBinary(currentDirectory + "/fnaFiles/")
    self.assertTrue(filecmp.cmp(currentDirectory + "/fnaFiles/testConvertToBinary.fna", currentDirectory + "/correct/testConvertToBinary.fna", shallow=False))
  
  def setupModifyLineLengthToSeventy(self):
    self.createDirectory(str(os.getcwd()) + "/fnaFiles")
    testFile = open(str(os.getcwd()) + "/fnaFiles/testModifyLineLengthToSeventy.fna", "w")
    testFile.write("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    testFile.close()
    self.createDirectory(str(os.getcwd()) + "/correct")
    correctFile = open(str(os.getcwd()) + "/correct/testModifyLineLengthToSeventy.fna", "w")
    correctFile.write("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAA")
    correctFile.close()

  def testModifyLineLengthToSeventy(self):
    currentDirectory = os.getcwd()
    self.setupModifyLineLengthToSeventy()
    modifyLineLengthToSeventy(currentDirectory + "/fnaFiles/", currentDirectory)
    self.assertTrue(filecmp.cmp(currentDirectory + "/fnaFiles/testModifyLineLengthToSeventy.fna", currentDirectory + "/correct/testModifyLineLengthToSeventy.fna", shallow=False))
#main  
if __name__=='__main__':
  unittest.main()

