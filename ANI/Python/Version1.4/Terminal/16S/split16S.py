import os
x = 0
newDirName = "/Users/jon/desktop/split/split16S"
os.system("mkdir " + newDirName)
firstLine = True
fnaName = ''
prevFileName = ''
newFileName = ''
with open('/Users/jon/Desktop/split/sequence.fasta') as file:
   for line in file:
      if line.strip() == '':
         firstLine = True
         x += 1
      else:
         if firstLine is True:
           fnaList = line.strip().split()
           fnaName = fnaList[1] + "_" + fnaList[2]
           newFileName = "/Users/jon/desktop/split/split16S/" + str(fnaName) + ".fna"
           if str(newFileName) == str(prevFileName):
              newFileName = "/Users/jon/desktop/split/split16S/" + str(fnaName) + str(x) + ".fna"
           else:
              prevFileName = newFileName
              newFileName = "/Users/jon/desktop/split/split16S/" + str(fnaName) + ".fna"
         else: 
           with open(newFileName, 'a') as newFile:
              newFile.write(line.strip())
         firstLine = False
   file.close()
