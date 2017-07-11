#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include "numberOfLinesLib.h"
#include "FNACharactersLib.h"
#include "levenshteinDistanceLib.h"
const int LINESIZE = 70;
const int KMERSIZE = 100;
const int fnaFilesDirectoryStringLengthBuffer = 100 + 2;
const char fnaFilesDirectory[fnaFilesDirectoryStringLengthBuffer] = {"/Users/jon/Desktop/Version13/Main/fna4/"};
const int minimumFnaFileStringLength = 4;
const int fnaNameBufferSize = 4;
const int amountOfFNAFilesBuffer = 3200;
const int nameLength = 100;
const int FILESIMILARITYCONST = 75;

int main() {
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
    const int kmerSizeMod = KMERSIZE+1;
    int finalANI = 0;
    char *ptr = NULL, *ptr2 = NULL;
    char kmerArr[kmerSizeMod], kmerArr2[kmerSizeMod];
    FILE *fnaPointer;
      for(int i = 0; i < fnaFileCount; i++) {
        for(int j = i; j < fnaFileCount; j++) {
            double fileSimilarityDouble = 0;
            int fileSimilarityInt = 0;
            int numCharsMin = 0;
            int numCharsMax = 0;
            long long file1Size = 0;
            long long file2Size = 0;
            struct stat sa;
            struct stat sb;
            stat(fnaArrayMalloc[i], &sa);
            stat(fnaArrayMalloc[j], &sb);
            file1Size = sa.st_size;
            file2Size = sb.st_size;
            if(file1Size < file2Size) {
                numCharsMin =  file1Size;
                numCharsMax =  file2Size;
            } else {
                numCharsMin = file2Size;
                numCharsMax = file1Size;
            }
            printf("\nnumCharsMin: \n%d\n", numCharsMax);
            printf("\nnumCharsMax: \n%d\n", numCharsMin);
            fileSimilarityDouble = ((double) numCharsMin / (double) numCharsMax )*100;
            fileSimilarityInt = (int) fileSimilarityDouble;
            if(fileSimilarityInt > FILESIMILARITYCONST && file1Size != file2Size ) {//&& file1Size != file2Size to omit same files
                int numLines1 = numberOfLines(LINESIZE, fnaArrayMalloc[i]);
                int numLines2 = numberOfLines(LINESIZE, fnaArrayMalloc[j]);
                //printf("\nnumLines1: \n%d\n", numLines1);
                //printf("\nnumLines2: \n%d\n", numLines2);  
                char **fna1Characters = NULL;
                fna1Characters = fnaCharactersOf(fnaArrayMalloc[i], LINESIZE, numLines1);
                char **fna2Characters = NULL;
                fna2Characters = fnaCharactersOf(fnaArrayMalloc[j], LINESIZE, numLines2);
                int minimumLines = 0;
                int maximumLines = 0;
                int numCharsLeft = 0;
                int numKmersLeft = 0;
                int numEditDistanceValueLeft = 0;
                int chr = 0;
                int chr2 = 0;
                int kmerCount = 0;
                double total = 0; 
                double difference = 0;
                double similarity = 0;
                double hundredSimilarity = 0;
                ptr=fna1Characters[0];
                ptr2=fna2Characters[0];
                if(file1Size < file2Size) {
                    minimumLines = numLines1;
                    maximumLines = numLines2;
                } else {
                    minimumLines = numLines2;
                    maximumLines = numLines1;
                }
                int numCharsMin2 = numCharsMin;// - minimumLines;// - \n
                int numCharsMax2 = numCharsMax;// - maximumLines;// - \n
                int numKmersMin = (numCharsMin2) - KMERSIZE;
                //printf("numkmerMin: %d\n", numKmersMin);
                int numKmersMax = (numCharsMax2) - KMERSIZE;
                printf("numCharsMin2: %d\n", numCharsMin2);

                for(int i = 0; i < numCharsMax2; i++) {
                    for(int j = 0; j < kmerSizeMod; j++) {
                        if(j == 0) {
                            chr = i;
                            chr2 = i;
                        }
                        if(j==kmerSizeMod-1) {
                            kmerArr[j] = '\0';
                        } else {
                            kmerArr[j] = ptr[chr++];
                        }
                        if(j==kmerSizeMod-1) {
                            kmerArr2[j] = '\0';
                        } else {
                            kmerArr2[j] = ptr2[chr2++];
                        }
                    }
                    if(strlen(kmerArr) != KMERSIZE) {
                        break;
                    }
                    if(strlen(kmerArr2) != KMERSIZE) {
                        break;
                    }
                    //printf("kmerArr: %s\n", kmerArr);
                    //printf("kmerArr2: %s\n", kmerArr2);
                    /*
                    if(strlen(kmerArr) == 1 && strlen(kmerArr) == 1) {
                        break;
                    }*/
                    if(kmerCount == numKmersMin) {
                        /*
					   if(numCharsMax > numCharsMin) {
                            numCharsLeft = numCharsMax - numCharsMin;
                            numKmersLeft = (numCharsLeft - 1) - KMERSIZE;
                            numEditDistanceValueLeft = numKmersLeft*KMERSIZE;
                            finalANI = finalANI + numEditDistanceValueLeft;
                            break;
                        }*/
                        break;
                    }
                    printf("kmerArr:  %s\n", kmerArr);
                    printf("kmerArr2: %s\n", kmerArr2);
                    int kmerANI = editDistance(kmerArr, kmerArr2, KMERSIZE, KMERSIZE);
                    printf("kmerANI: %d\n", kmerANI);
                    finalANI = finalANI + kmerANI;
                    kmerCount++;
                    printf("kmerCount: %d\n", kmerCount);
                }
                total = numKmersMax*KMERSIZE;
                difference = finalANI/total;
                similarity = 1 - difference;
                hundredSimilarity = similarity*100;
                //printf("kmerCount: %d\n", kmerCount);
                printf("\n %s %s ANI: %d\n", fnaArrayMalloc[i], fnaArrayMalloc[j], finalANI);
                printf("%s %s Similarity: %f\n", fnaArrayMalloc[i], fnaArrayMalloc[j], hundredSimilarity);
                free(fna1Characters);
                free(fna2Characters);
                finalANI = 0;
            }
            /*
            else {
                printf("\n %s %s File Similarity too low, similarity: %d\n", fnaArrayMalloc[i], fnaArrayMalloc[j], fileSimilarityInt);
            }*/
        }
    }
}