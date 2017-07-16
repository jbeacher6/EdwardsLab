#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include "numberOfLinesLib.h"
#include "FNACharactersLib.h"
#include "levenshteinDistanceLib.h"
//TODO: move out of main into functions or libraries. Currently fnaFilesDirectory has repeating boilerplate code
//------//
//F1 = Forward DNA File #1, F2 = Forward DNA File #2, RC2 = Reverse Compliment DNA File #2
//Size of each line in FNA file
const int LINESIZE = 70;
//Kmer Length
const int KMERSIZE = 2;
//Length of the string of the fna file directory
const int fnaFilesDirectoryStringLengthBuffer = 100 + 2;
//Forward DNA Files
///Example: Users/jon/desktop/version15/Main/fna10/
const char fnaFilesDirectory[fnaFilesDirectoryStringLengthBuffer] = {"/Users/jon/desktop/version15/Main/subFNA1/"};
//Reverse Compliment DNA Files
const char fnaFilesDirectory2[fnaFilesDirectoryStringLengthBuffer] = {"/Users/jon/desktop/version15/Main/subFNA2/"};
//Minimum length of the FNA file name
const int minimumFnaFileStringLength = 4;
//Size of ".fna"(4)
const int fnaNameBufferSize = 4;
//Amount of FNA Files exact number or a ceiling estimation, it can be over the amount but not under the actual amount
const int amountOfFNAFilesBuffer = 3200;
//Buffer for the max name length. A ceiling estimation, it can be over the amount but not under the actual amount
const int nameLength = 100;
//What percentage the files are similar in an integer value
const int FILESIMILARITYCONST = 0;
//
int main() {
    //--------------------------------------------------------------------------Forward DNA FNA Files---
    int fnaFileCount = 0;
    DIR *fnaFilesDirectoryPointer;
    struct dirent *direntFnaDirectory;
    fnaFilesDirectoryPointer = opendir(fnaFilesDirectory);
    char checkIfFNA[fnaNameBufferSize];
    char fnaString[fnaNameBufferSize] = "fna";
    int fnaFilesDirectoryStringLengthMinusOne = minimumFnaFileStringLength - 1;
    char** fnaArrayMalloc = (char**) malloc(amountOfFNAFilesBuffer*sizeof(char*));
    if(fnaArrayMalloc == NULL) { 
        printf("%s", "Error: kmersArrayMalloc\n");
        exit(EXIT_FAILURE);
    }
    for(int i = 0; i < amountOfFNAFilesBuffer; i++) {
        fnaArrayMalloc[i] = (char *) malloc(sizeof(char)*nameLength);
        if(fnaArrayMalloc[i] == NULL) { 
            printf("%s", "Error: kmersArrayMalloc\n");
            exit(EXIT_FAILURE);
        }
   }
    if(fnaFilesDirectoryPointer) {
        while ((direntFnaDirectory = readdir(fnaFilesDirectoryPointer)) != NULL) {
            int strlenString = strlen(direntFnaDirectory->d_name);
            if( strlenString > minimumFnaFileStringLength) {
                memcpy(checkIfFNA, &direntFnaDirectory->d_name[strlenString - fnaFilesDirectoryStringLengthMinusOne], fnaFilesDirectoryStringLengthMinusOne);
                if (strcmp(checkIfFNA,fnaString) == 0) {
                    int strlenString2 = strlen(fnaFilesDirectory);
                    memcpy(fnaArrayMalloc[fnaFileCount], fnaFilesDirectory, strlenString2);
                    memcpy(fnaArrayMalloc[fnaFileCount] + strlenString2, &direntFnaDirectory->d_name, strlenString);
                    fnaFileCount++;
                }
            }
        }
        closedir(fnaFilesDirectoryPointer);
    } else {
        printf("%s", "Error: fnaFilesDirectory[fnaFilesDirectoryStringLength] is null\n");
        exit(EXIT_FAILURE);
    }
    
    //------------------------------------------------------------------------Backward DNA FNA Files---
    int fnaFileCount2 = 0;
    DIR *fnaFilesDirectoryPointer2;
    struct dirent *direntFnaDirectory2;
    fnaFilesDirectoryPointer2 = opendir(fnaFilesDirectory2);
    char checkIfFNA2[fnaNameBufferSize];
    char fnaString2[fnaNameBufferSize] = "fna";
    int fnaFilesDirectoryStringLengthMinusOne2 = minimumFnaFileStringLength - 1;
    char** fnaArrayMalloc2 = (char**) malloc(amountOfFNAFilesBuffer*sizeof(char*));
    if(fnaArrayMalloc2 == NULL) { 
        printf("%s", "Error: kmersArrayMalloc2\n");
        exit(EXIT_FAILURE);
    }
    for(int i = 0; i < amountOfFNAFilesBuffer; i++) {
        fnaArrayMalloc2[i] = (char *) malloc(sizeof(char)*nameLength);
        if(fnaArrayMalloc2[i] == NULL) { 
            printf("%s", "Error: kmersArrayMalloc\n");
            exit(EXIT_FAILURE);
        }
   }
    if(fnaFilesDirectoryPointer2) {
        while ((direntFnaDirectory2 = readdir(fnaFilesDirectoryPointer2)) != NULL) {
            int strlenString2 = strlen(direntFnaDirectory2->d_name);
            if(strlenString2 > minimumFnaFileStringLength) {
                memcpy(checkIfFNA2, &direntFnaDirectory2->d_name[strlenString2 - fnaFilesDirectoryStringLengthMinusOne2], fnaFilesDirectoryStringLengthMinusOne2);
                if (strcmp(checkIfFNA,fnaString) == 0) {
                    int strlenString2 = strlen(fnaFilesDirectory2);
                    memcpy(fnaArrayMalloc2[fnaFileCount2], fnaFilesDirectory2, strlenString2);
                    memcpy(fnaArrayMalloc2[fnaFileCount2] + strlenString2, &direntFnaDirectory2->d_name, strlenString2);
                    fnaFileCount2++;
                }
            }
        }
        closedir(fnaFilesDirectoryPointer2);
    } else {
        printf("%s", "Error: fnaFilesDirectory2[fnaFilesDirectoryStringLength] is null\n");
        exit(EXIT_FAILURE);
    }
    //--------------------------------------------------------------------------F1 vs F2 & F1 vs RC2---
    //Modification to the kmer to add the null terminator \n to avoid garbage values
    const int kmerSizeMod = KMERSIZE+1;
    //(F1 vs F2) + (F1 vs RC2)
    int finalANI = 0;
    //Pointer to F1, F2 and RC2
    char *ptr = NULL, *ptr2 = NULL, *ptr3 = NULL;
    //Kmers of F1, F2 and RC2
    char kmerArr[kmerSizeMod], kmerArr2[kmerSizeMod], kmerArr3[kmerSizeMod];
    //Cycle through the list of all fna files(Forward and Reverse should be the same size)
      for(int i = 0; i < fnaFileCount; i++) {
        //printf("%s \n", fnaArrayMalloc[i]);
        //printf("%s \n", fnaArrayMalloc2[i]);
        //Go through list of fna files without repeats (j=i)
        for(int j = i; j < fnaFileCount; j++) {
            //Double of file similarity percentage(based on # characters, not number of kmers)
            double fileSimilarityDouble = 0;
            //Double of file similarity percentage(based on # characters, not number of kmers)
            int fileSimilarityInt = 0;
            //Number of characters in each file (number of bytes is the number of characters)
            int numCharsMin = 0;
            int numCharsMax = 0;
            //FileSize in each file
            long long file1Size = 0;
            long long file2Size = 0;
            //query filesSize with stat
            struct stat sa;
            struct stat sb;
            stat(fnaArrayMalloc[i], &sa);
            stat(fnaArrayMalloc[j], &sb);
            //Get stat fileSize and save
            file1Size = sa.st_size;
            file2Size = sb.st_size;
            //Check which file has the least amount of characters
            if(file1Size < file2Size) {
                numCharsMin =  file1Size;
                numCharsMax =  file2Size;
            } else {
                numCharsMin = file2Size;
                numCharsMax = file1Size;
            }
            //printf("\nnumCharsMin: \n%d\n", numCharsMax);
            //printf("\nnumCharsMax: \n%d\n", numCharsMin);
            //Calculate which files are similar to eachtother. This is done to filter out low similarity files before computing
            fileSimilarityDouble = ((double) numCharsMin / (double) numCharsMax )*100;
            //Calculate which files are similar to eachtother. This is done to filter out low similarity files before computing
            fileSimilarityInt = (int) fileSimilarityDouble;
            //
            //printf("fileSimilarityInt: %d\n", fileSimilarityInt);
            //printf("FILESIMILARITYCONST: %d\n", FILESIMILARITYCONST);
            if(fileSimilarityInt > FILESIMILARITYCONST) {//&& file1Size != file2Size to omit same files
                int numLines1 = numberOfLines(LINESIZE, fnaArrayMalloc[i]);
                int numLines2 = numberOfLines(LINESIZE, fnaArrayMalloc[j]);
                //printf("\nnumLines1: \n%d\n", numLines1);
                //printf("\nnumLines2: \n%d\n", numLines2); 
                //F1 Characters, set the pointer to null to omit garbage values and for proper resetting 
                char **fna1Characters = NULL;
                //call fnacharacters from fnaArrayMalloc
                fna1Characters = fnaCharactersOf(fnaArrayMalloc[i], LINESIZE, numLines1);
                //F2, set the pointer to null to omit garbage values and for proper resetting 
                char **fna2Characters = NULL;
                //call fnacharacters from fnaArrayMalloc
                fna2Characters = fnaCharactersOf(fnaArrayMalloc[j], LINESIZE, numLines2);
                //RC2, set the pointer to null to omit garbage values and for proper resetting 
                char **fna3Characters = NULL;
                //call fnacharacters from fnaArraymMalloc and assign it to j
                fna3Characters = fnaCharactersOf(fnaArrayMalloc2[j], LINESIZE, numLines2);
                //char **fna3Characters = NULL;
                //fna3Characters = fnaCharactersOf(fnaArrayMalloc[j], LINESIZE, numLines3);
                //minimum number of lines in the fna files
                int minimumLines = 0;
                //maximum number of lines in the fna files
                int maximumLines = 0;
                //number of chars left in the count
                int numCharsLeft = 0;
                //number of preset kmer prediction left(# kmers prediction)
                int numKmersLeft = 0;
                //?
                int numEditDistanceValueLeft = 0;
                //character integer count of F1
                int chr = 0;
                //character integer count of F2
                int chr2 = 0;
                //character integer count of RC2
                int chr3 = 0;
                //count of the current amount of kmers being computed
                int kmerCount = 0;
                //count of the total number of ?
                double total = 0;
                //the difference of ?
                double difference = 0;
                //the difference of similarity 
                double similarity = 0;
                //the difference of hundred similarity
                double hundredSimilarity = 0;
                //get pointer to fna files(F1, F2, RC2)
                //pointer to F1
                ptr=fna1Characters[0];
                //pointer to F2
                ptr2=fna2Characters[0];
                //pointer to F3
                ptr3=fna3Characters[0];
                //check for the minimum filesize
                if(file1Size < file2Size) {
                    minimumLines = numLines1;
                    maximumLines = numLines2;
                } else {
                    minimumLines = numLines2;
                    maximumLines = numLines1;
                }
                //Get the number of chars without the null pointer at the end of the line
                int numCharsMin2 = numCharsMin;// - minimumLines;// - \n
                //Get the number of chars without the null pointer at the end of the line
                int numCharsMax2 = numCharsMax;// - maximumLines;// - \n
                //Get the number of chars without the null pointer at the end of the line
                int numKmersMin = (numCharsMin2) - KMERSIZE;
                //printf("numkmerMin: %d\n", numKmersMin);
                int numKmersMax = (numCharsMax2) - KMERSIZE;
                //printf("numCharsMin2: %d\n", numCharsMin2);
                //int boolean1 = 0;
                //Cycle through the number of characters in the file without the null pointers
                for(int i = 0; i < numCharsMax2; i++) {
                    //Cycle through and add kmers to temporary kmerArrays, including the \n
                    for(int j = 0; j < kmerSizeMod; j++) {
                        //reset count if starting out
                        if(j == 0) {
                            //reset chr1 of f1
                            chr = i;
                            //reset ch2 of f2
                            chr2 = i;
                            //reset ch3 of rc2
                            chr3 = i;
                        }
                        //if reached the end of the kmer
                        if(j==kmerSizeMod-1) {
                            //add null string the the end of the kmer
                            kmerArr[j] = '\0';
                        } else {
                            //else move forward one char
                            kmerArr[j] = ptr[chr++];
                        }
                        //if reached the end of the kmer
                        if(j==kmerSizeMod-1) {
                            //add null string the the end of the kmer
                            kmerArr2[j] = '\0';
                        } else {
                            //else move forward one char
                            kmerArr2[j] = ptr2[chr2++];
                        }
                        //if reached the end of the kmer
                        if(j==kmerSizeMod-1) {
                            //add null string the the end of the kmer
                            kmerArr3[j] = '\0';
                        } else {
                            //else move forward one char
                            kmerArr3[j] = ptr3[chr3++];
                        }                        
                    }
                    //check if the kmer array of F1 is equal to the kmersize
                    if(strlen(kmerArr) != KMERSIZE) {
                        //break if equal, reached the end of the file. done to avoid garbage values
                        break;
                    }
                    //check if the kmer array of F2 is equal to the kmersize
                    if(strlen(kmerArr2) != KMERSIZE) {
                        //break if equal, reached the end of the file. done to avoid garbage values
                        break;
                    }
                    //check if the kmer array of RC2 is equal to the kmersize
                    if(strlen(kmerArr3) != KMERSIZE) {
                        //break if equal, reached the end of the file. done to avoid garbage values
                        break;
                    }
                    //printf("kmerArr: %s\n", kmerArr);
                    //printf("kmerArr2: %s\n", kmerArr2);
                    /*
                    if(strlen(kmerArr) == 1 && strlen(kmerArr) == 1) {
                        break;
                    }*/
                    /*
                    if(kmerCount == numKmersMin) {
                        
					   if(numCharsMax > numCharsMin) {
                            numCharsLeft = numCharsMax - numCharsMin;
                            numKmersLeft = (numCharsLeft - 1) - KMERSIZE;
                            numEditDistanceValueLeft = numKmersLeft*KMERSIZE;
                            finalANI = finalANI + numEditDistanceValueLeft;
                            break;
                        }
                        break;
                    }*/
                    //printf("kmerArr:  %s\n", kmerArr);
                    //printf("kmerArr2: %s\n", kmerArr2);
                    //Store calculated kmerANI value from the editDistance of F1 kmer and F2 kmer
                    int kmerANI = editDistance(kmerArr, kmerArr2, KMERSIZE, KMERSIZE);
                    //printf("\n %s %s ANI: %d\n", fnaArrayMalloc[i], fnaArrayMalloc[j], kmerANI);
                    //Store the calculated kmerANI value from the editDistance of F1 kmer and RC2 kmer
                    int kmerANI2 = editDistance(kmerArr, kmerArr3, KMERSIZE, KMERSIZE);
                    //printf("\n %s %s ANI: %d\n", fnaArrayMalloc[i], fnaArrayMalloc2[j], finalANI);
                    //printf("kmerANI: %d\n", kmerANI);
                    //Store the finalANI value 
                    finalANI = finalANI + kmerANI + kmerANI2;
                    //Update the kmerCount
                    kmerCount++;
                    //printf("kmerCount: %d\n", kmerCount);
                }
                //Multiply max number of kmers by kmersize to determine the maximum edit distance calculation for further calculations for regions of non-simularity
                total = numKmersMax*KMERSIZE;
                //Find the difference between both
                difference = finalANI/total;
                //Find the simularity by subtracting by one
                similarity = 1 - difference;
                //Turn into a readable integer value
                hundredSimilarity = similarity*100;
                //
                //printf("kmerCount: %d\n", kmerCount);
                //
                //print final ani values
                printf("\n %s %s %s ANI: %d\n", fnaArrayMalloc[i], fnaArrayMalloc[j], fnaArrayMalloc2[j], finalANI);
                //Final Simularity 
                printf("%s %s %s Similarity: %f\n", fnaArrayMalloc[i], fnaArrayMalloc[j], fnaArrayMalloc2[j], hundredSimilarity);
                //free malloc to prevent sfault 11
                free(fna1Characters);
                //free malloc to prevent sfault 11
                free(fna2Characters);
                //free malloc to prevent sfault 11
                free(fna3Characters);
                //reset final ani to zero for next comparisions
                finalANI = 0;
            }
            /*
            else {
                printf("\n %s %s File Similarity too low, similarity: %d\n", fnaArrayMalloc[i], fnaArrayMalloc[j], fileSimilarityInt);
            }*/
        }
    }
//--------------------------------
}