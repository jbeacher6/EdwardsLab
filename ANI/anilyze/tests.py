from anilyze import downloadFiles
from anilyze import decompress
from anilyze import deleteFirstLineAndRename
from anilyze import deleteLineInfo
from anilyze import createReverseComplimentAndAppendToForward
from anilyze import convertToBinary
from anilyze import modifyLineLengthToSeventy
from anilyze import splitFastaForComplete
import os
import filecmp
import ftplib#library used to download files using ftp
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
    downloadFiles(os.getcwd() + "/tests/fnaFiles/", True)
    self.assertEqual(str(hashlib.md5(open(str(os.getcwd() + "/fnaFiles/GCF_000010525.1_ASM1052v1_genomic.fna.gz"), "rb").read()).hexdigest()), "417d852fbfbb7a37e23fd6d6d4f9d60d")

  def testDecompress(self):
    downloadFiles(os.getcwd() + "/tests/fnaFiles/", True)
    decompress(str(os.getcwd()) + "/tests/fnaFiles/")
    string = str(os.getcwd()+ "/tests/fnaFiles/GCF_000010525.1_ASM1052v1_genomic.fna") 
    self.assertTrue(os.path.isfile(string))

  def setupTestDeleteFirstLineAndRename(self):
    self.createDirectory(str(os.getcwd()) + "/tests/fnaFiles")
    testFile = open(str(os.getcwd()) + "/tests/fnaFiles/testDeleteFirstLineAndRename.fna", "w")
    testFile.write(">NC00 Example Bacterii\nACGT\n")
    testFile.close()
    self.createDirectory(str(os.getcwd()) + "/tests/correct")
    correctFile = open(str(os.getcwd()) + "/tests/correct/" + "Example_Bacterii.fna", "w")
    correctFile.write("ACGT\n")
    correctFile.close()
  
  def testDeleteFirstLineAndRename(self):
    self.setupTestDeleteFirstLineAndRename()
    currentDirectory = str(os.getcwd())
    deleteFirstLineAndRename(str(os.getcwd()) + "/tests/fnaFiles/")
    #self.assertTrue(os.path.exists(currentDirectory + "/fnaFiles/Example_Bacterii.fna"))
    self.assertTrue(filecmp.cmp(str(os.getcwd()) + "/tests/fnaFiles/Example_Bacterii.fna", str(os.getcwd()) + "/correct/Example_Bacterii.fna", shallow=False))
  
  def setupDeleteLineInfo(self):
    self.createDirectory(str(os.getcwd()) + "/tests/fnaFiles")
    testFile = open(str(os.getcwd()) + "/tests/fnaFiles/Example_Bacterii.fna", "w")
    testFile.write(">NC00 Example Bacterii\nAAAA\n>NC01 Example Bacterii\nCCCC\n>NC02 Example Bacterii\nGGGG\n>NC03 Example Bacterii\nTTTT\n")
    testFile.close()
    self.createDirectory(str(os.getcwd()) + "/tests/correct")
    correctFile = open(str(os.getcwd()) + "/tests/correct/" + "Example_Bacterii.fna", "w")
    correctFile.write("AAAA\nCCCC\nGGGG\nTTTT\n")
    correctFile.close()

  def testDeleteLineInfo(self):
    self.setupDeleteLineInfo()
    deleteLineInfo(str(os.getcwd()) + "/tests/fnaFiles/")
    self.assertTrue(filecmp.cmp(str(os.getcwd()) + "/tests/fnaFiles/Example_Bacterii.fna", str(os.getcwd()) + "/correct/Example_Bacterii.fna", shallow=False))

  def setupTestCreateReverseComplimentAndAppendToForward(self):
    self.createDirectory(str(os.getcwd()) + "/tests/fnaFiles")
    testFile = open(str(os.getcwd()) + "/tests/fnaFiles/testCreateReverseComplimentAndAppendToForward.fna", "w")
    testFile.write("GCAT")
    testFile.close()
    self.createDirectory(str(os.getcwd()) + "/tests/correct")
    correctFile = open(str(os.getcwd()) + "/tests/correct/testCreateReverseComplimentAndAppendToForward.fna", "w")
    correctFile.write("GCATATGC")
    correctFile.close()

  def testCreateReverseComplimentAndAppendToForward(self):
    self.setupTestCreateReverseComplimentAndAppendToForward()
    createReverseComplimentAndAppendToForward(str(os.getcwd()) + "/tests/fnaFiles/")
    self.assertTrue(filecmp.cmp(str(os.getcwd())+ "/tests/fnaFiles/testCreateReverseComplimentAndAppendToForward.fna", str(os.getcwd()) + "/correct/testCreateReverseComplimentAndAppendToForward.fna", shallow=False))
  
  def setupTestConvertToBinary(self):
    self.createDirectory(str(os.getcwd()) + "/tests/fnaFiles")
    testFile = open(str(os.getcwd()) + "/tests/fnaFiles/testConvertToBinary.fna", "w")
    testFile.write("ACGT")
    testFile.close()
    self.createDirectory(str(os.getcwd()) + "/tests/correct")
    correctFile = open(str(os.getcwd()) + "/tests/correct/testConvertToBinary.fna", "w")
    correctFile.write("00011011")
    correctFile.close()

  def testConvertToBinary(self):
    self.setupTestConvertToBinary()
    currentDirectory = str(os.getcwd())
    convertToBinary(str(os.getcwd()) + "/tests/fnaFiles/")
    self.assertTrue(filecmp.cmp(str(os.getcwd())+ "/tests/fnaFiles/testConvertToBinary.fna", str(os.getcwd()) + "/tests/correct/testConvertToBinary.fna", shallow=False))
  
  def setupModifyLineLengthToSeventy(self):
    self.createDirectory(str(os.getcwd()) + "/tests/fnaFiles/")
    testFile = open(str(os.getcwd()) + "/fnaFiles/testModifyLineLengthToSeventy.fna", "w")
    testFile.write("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n")
    testFile.close()
    self.createDirectory(str(os.getcwd()) + "/tests/correct/")
    correctFile = open(str(os.getcwd()) + "/tests/correct/testModifyLineLengthToSeventy.fna", "w")
    correctFile.write("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAA\n")
    correctFile.close()

  def testModifyLineLengthToSeventy(self):
    self.setupModifyLineLengthToSeventy()
    modifyLineLengthToSeventy(str(os.getcwd())+ "/tests/fnaFiles/", str(os.getcwd()) + "/tests/fnaFiles/")
    self.assertTrue(filecmp.cmp(str(os.getcwd()) + "/tests/fnaFiles/correctlyFormatted/testModifyLineLengthToSeventy.fna", str(os.getcwd()) + "/tests/correct/testModifyLineLengthToSeventy.fna", shallow=False))
  
  def setupSplitFastaForComplete(self):
    self.createDirectory(str(os.getcwd()) + "/tests/testFiles/")
    testFile = open(str(os.getcwd()) + "/testFiles/testSplitFastaForComplete.fasta", "w")
    testFile.write(">NR00 Example Bacterium 16S partial sequence\nCCC\n\n>NR01 Example Bacterii 16S complete sequence\nGGG\n\n>NR02 Example Bacterii 16S complete sequence\nTTT\n")
    testFile.close()
    self.createDirectory(str(os.getcwd()) + "/tests/correct/")
    correctFile = open(str(os.getcwd()) + "/tests/correct/Example_Bacterii.fna", "w")
    correctFile.write("GGG")
    correctFile.close()
    correctFile2 = open(str(os.getcwd()) + "/tests/correct/Example_Bacterii_2.fna", "w")
    correctFile2.write("TTT")
    correctFile2.close()

  def testSplitFastaForComplete(self):
    self.setupSplitFastaForComplete()
    splitFastaForComplete(str(os.getcwd()) + "/tests/testFiles/")
    self.assertTrue(filecmp.cmp(str(os.getcwd()) + "/tests/testFiles/Example_Bacterii.fna", str(os.getcwd()) + "/tests/correct/Example_Bacterii.fna", shallow=False))
    self.assertTrue(filecmp.cmp(str(os.getcwd()) + "/tests/testFiles/Example_Bacterii_2.fna", str(os.getcwd()) + "/tests/correct/Example_Bacterii_2.fna", shallow=False))    
#main  
if __name__=='__main__':
  unittest.main()

