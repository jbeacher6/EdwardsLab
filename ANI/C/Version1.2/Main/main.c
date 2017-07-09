#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>

#include "numberOfLinesLib.h"
#include "FNACharactersLib.h"
#include "levenshteinDistanceLib.h"

const int LINESIZE = 70;
const int KMERSIZE = 2;
const int fnaFilesDirectoryStringLengthBuffer = 100 + 2;
const char fnaFilesDirectory[fnaFilesDirectoryStringLengthBuffer] = {"/Users/jon/Desktop/Version1336/Main/fna/"};
const int minimumFnaFileStringLength = 4;
const int fnaNameBufferSize = 4;
const int amountOfFNAFilesBuffer = 3200;
const int nameLength = 100;

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
    char *ptr, *ptr2;
    char tempArr[kmerSizeMod], tempArr2[kmerSizeMod];
    FILE *fnaPointer;
      for(int i = 0; i < fnaFileCount; i++) {
        for(int j = i; j < fnaFileCount; j++) {
            int numLines1 = numberOfLines(LINESIZE, fnaArrayMalloc[i]);        
            int numLines2 = numberOfLines(LINESIZE, fnaArrayMalloc[j]);
            char **fna1Characters = fnaCharactersOf(fnaArrayMalloc[i], LINESIZE, numLines1);
            char **fna2Characters = fnaCharactersOf(fnaArrayMalloc[j], LINESIZE, numLines2);
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
            double simularity = 0;
            double hundredSimularity = 0;
            ptr=fna1Characters[0];
            ptr2=fna2Characters[0];
            FILE *file1;
            file1 = fopen(fnaArrayMalloc[i], "rb");
            long file1Size = 0;
            if(file1 == NULL) {
                printf("file1 is null");
            }
            fseek(file1, 0, SEEK_END);
            file1Size = ftell(file1);
            fclose(file1);
            FILE *file2;
            file2 = fopen(fnaArrayMalloc[j], "rb");
            long file2Size = 0;
            if(file2 == NULL) {
                printf("file2 is null");
            }
            fseek(file2, 0, SEEK_END);
            file2Size = ftell(file2);
            fclose(file2);
            //future: filter if filesize*.25 for around 75% or above simularity matches only
            int numCharsMin = 0;
            int numCharsMax = 0;
            if(file1Size < file2Size) {
                numCharsMin = file1Size;
                minimumLines = numLines1;
                maximumLines = numLines2;
                numCharsMax = file2Size;
            } else {
                numCharsMin = file2Size;
                minimumLines = numLines2;
                maximumLines = numLines1;
                numCharsMax = file1Size;
            }
            int numCharsMin2 = numCharsMin - minimumLines;// - \n
			int numCharsMax2 = numCharsMax - maximumLines;// - \n
            int numKmersMin = (numCharsMin2 - 1) - KMERSIZE;
            int numKmersMax = (numCharsMax2 - 1) - KMERSIZE;
            for(int i = 0; i < numCharsMin2; i++) {
                for(int j = 0; j < kmerSizeMod; j++) {
                    if(j == 0) {
                        chr = i;
                        chr2 = i;
                    }
                    if(j==kmerSizeMod-1) {
                        tempArr[j] = '\0';
                    } else {
                        tempArr[j] = ptr[chr++];
                    }
                    if(j==kmerSizeMod-1) {
                        tempArr2[j] = '\0';
                    } else {
                        tempArr2[j] = ptr2[chr2++];
                    }
                }
                if(kmerCount == numKmersMin) {
					if(numCharsMax > numCharsMin) {
                        numCharsLeft = numCharsMax - numCharsMin;
                        numKmersLeft = (numCharsLeft - 1) - KMERSIZE;
                        numEditDistanceValueLeft = numKmersLeft*KMERSIZE;
                        finalANI = finalANI + numEditDistanceValueLeft;
                        break;
                    }
                    break;
                }
                int kmerANI = editDistance(tempArr, tempArr2, KMERSIZE, KMERSIZE);
                finalANI = finalANI + kmerANI;
                kmerCount++;
            }
            total = numKmersMax*KMERSIZE;
            difference = finalANI/total;
            simularity = 1 - difference;
            hundredSimularity = simularity*100;
            printf("\n %s %s ANI: %d\n", fnaArrayMalloc[i], fnaArrayMalloc[j], finalANI);
            printf("%s %s Simularity: %f\n", fnaArrayMalloc[i], fnaArrayMalloc[j], hundredSimularity);
            free(fna1Characters);
            free(fna2Characters);
            finalANI = 0;
        }
    }
}