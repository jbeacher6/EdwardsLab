#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include "numberOfLinesLib.h"
#include "FNACharactersLib.h"
#include "levenshteinDistanceLib.h"
//This version computes the F1 vs F2 kmers and the F1 vs R2 kmers and adds the minimum of the individual kmers
const int LINESIZE = 70;
const int KMERSIZE = 2;
const int fnaFilesDirectoryStringLengthBuffer = 39 + 2;
const char fnaFilesDirectoryConstant[fnaFilesDirectoryStringLengthBuffer] = {"/Users/jon/desktop/version19/Main/fna5/"};
const char fnaFilesDirectoryConstantRC[fnaFilesDirectoryStringLengthBuffer] = {"/Users/jon/desktop/version19/Main/fna7/"};
const int minimumFnaFileStringLength = 4;
const int fnaNameBufferSize = 4;
const int amountOfFNAFilesBuffer = 3200;
const int nameLength = 100;
const int FILESIMILARITYCONST = 1;

void calculateANI(const char fnaFilesDirectory[], const char fnaFilesDirectory2[]);
char** createArrayOfFiles(const char fnaFilesDirectory[]);
int countFiles(const char fnaFilesDirectory[]);

int main() {
    calculateANI(fnaFilesDirectoryConstant, fnaFilesDirectoryConstantRC);
	return 0;
}

void calculateANI(const char fnaFilesDirectory[], const char fnaFilesDirectory2[]) {
    int fnaFileCount = 0;
    char** fnaArrayMalloc = createArrayOfFiles(fnaFilesDirectory);
    int fnaFileCount1 = countFiles(fnaFilesDirectory);

    char** fnaArrayMalloc2 = createArrayOfFiles(fnaFilesDirectory2);
    int fnaFileCount2 = countFiles(fnaFilesDirectory2);

    char** fnaArrayMalloc3 = createArrayOfFiles(fnaFilesDirectory);
    char** fnaArrayMalloc4 = createArrayOfFiles(fnaFilesDirectory2);
    if(fnaFileCount1 != fnaFileCount2) { 
        printf("%s", "Error: file counts do not match\n");
        exit(EXIT_FAILURE);
    }
    fnaFileCount = fnaFileCount1;
    //----------------------------------------------------------------------------
	const int kmerSizeMod = KMERSIZE+1;
    int finalANI = 0;
    char *ptr = NULL, *ptr2 = NULL, *ptr3 = NULL, *ptr4 = NULL;
    char kmerArr[kmerSizeMod], kmerArr2[kmerSizeMod], kmerArr3[kmerSizeMod], kmerArr4[kmerSizeMod];
    FILE *fnaPointer;
      for(int i = 0; i < fnaFileCount; i++) {
        for(int j = i; j < fnaFileCount; j++) {
        	//---------------------------------------F1 v F2----------------------
            //printf("%s i \n", fnaArrayMalloc[i]);
            //printf("%s j \n", fnaArrayMalloc[j]);
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
            //printf("\nnumCharsMin: \n%d\n", numCharsMax);
            //printf("\nnumCharsMax: \n%d\n", numCharsMin);
            double fileSimilarityDouble3 = 0;
            int fileSimilarityInt3 = 0;
            int numCharsMin2 = 0;
            int numCharsMax2 = 0;
            long long file1Size3 = 0;
            long long file2Size4 = 0;
            struct stat sa3;
            struct stat sb4;
            stat(fnaArrayMalloc3[i], &sa3);
            stat(fnaArrayMalloc4[j], &sb4);
            file1Size3 = sa3.st_size;
            file2Size4 = sb4.st_size;
            if(file1Size3 < file2Size4) {
                numCharsMin2 =  file1Size3;
                numCharsMax2 =  file2Size4;
            } else {
                numCharsMin2 = file1Size3;
                numCharsMax2 = file2Size4;
            }
            //------------F1 v F2---------------
            if(strcmp(fnaArrayMalloc[i], fnaArrayMalloc[j]) != 0) {
                fileSimilarityDouble = ((double) numCharsMin / (double) numCharsMax )*100;
                fileSimilarityInt = (int) fileSimilarityDouble;
                if(fileSimilarityInt > FILESIMILARITYCONST) {
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
 		    	//------------F1 v R2--------------
 				char **fna3Characters = NULL;
                fna3Characters = fnaCharactersOf(fnaArrayMalloc3[i], LINESIZE, numLines1);
                char **fna4Characters = NULL;
                fna4Characters = fnaCharactersOf(fnaArrayMalloc4[j], LINESIZE, numLines2);
                int chr3 = 0;
                int chr4 = 0;
                ptr3=fna3Characters[0];
                ptr4=fna4Characters[0];
               if(strcmp(fnaArrayMalloc3[i], fnaArrayMalloc4[j]) != 0) {
               		int numLines3 = numberOfLines(LINESIZE, fnaArrayMalloc3[i]);
                	int numLines4 = numberOfLines(LINESIZE, fnaArrayMalloc4[j]);    
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
                	//printf("numCharsMin2: %d\n", numCharsMin2);
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
                        	if(j==kmerSizeMod-1) {
                            	kmerArr3[j] = '\0';
                        	} else {
                            	kmerArr3[j] = ptr3[chr3++];
                        	}
                        	if(j==kmerSizeMod-1) {
                            	kmerArr4[j] = '\0';
                        	} else {
                            	kmerArr4[j] = ptr4[chr4++];
                        	}
                    	}
                    	if(strlen(kmerArr) != KMERSIZE) {
                        	break;
                    	}
                    	if(strlen(kmerArr2) != KMERSIZE) {
                        	break;
                    	}
                    	if(strlen(kmerArr3) != KMERSIZE) {
                        	break;
                    	}
                    	if(strlen(kmerArr4) != KMERSIZE) {
                        	break;
                    	}
                  	printf("\n %s %s\n", fnaArrayMalloc[i], fnaArrayMalloc[j]);
                    printf("kmerArr:  %s\n", kmerArr);
                    printf("kmerArr2: %s\n", kmerArr2);
                    int kmerANI12 = editDistance(kmerArr, kmerArr2, KMERSIZE, KMERSIZE);

                    printf("\n %s %s\n", fnaArrayMalloc3[i], fnaArrayMalloc4[j]);
                    printf("kmerArr:  %s\n", kmerArr3);
                    printf("kmerArr2: %s\n", kmerArr4);
                    int kmerANI34 = editDistance(kmerArr3, kmerArr4, KMERSIZE, KMERSIZE);
                    //printf("kmerANI: %d\n", kmerANI);
                    if(kmerANI12 < kmerANI34) {
                    	finalANI = finalANI + kmerANI12;
                    } else {
                    	finalANI = finalANI + kmerANI34;
                    }
                    kmerCount++;
                    //printf("kmerCount: %d\n", kmerCount);
                }
                //total = numKmersMax*KMERSIZE;
                //difference = finalANI/total;
                //similarity = 1 - difference;
                //hundredSimilarity = similarity*100;
                //printf("kmerCount: %d\n", kmerCount);
                printf("\n %s %s ANI: %d\n", fnaArrayMalloc[i], fnaArrayMalloc[j], finalANI);
                printf("\n %s %s ANI: %d\n", fnaArrayMalloc[i], fnaArrayMalloc[j], finalANI);
                //printf("%s %s Similarity: %f\n", fnaArrayMalloc[i], fnaArrayMalloc[j], hundredSimilarity);
                free(fna1Characters);
                free(fna2Characters);
                free(fna3Characters);
                free(fna4Characters);
                //return finalANI;
                }
            }
        }
    }
}
}

char** createArrayOfFiles(const char fnaFilesDirectory[]) {
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
                    //printf("%s\n", get_filename_ext(direntFnaDirectory->d_name));
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
    return fnaArrayMalloc;
}

int countFiles(const char fnaFilesDirectory[]) {
	int fnaFileCount = 0;
    DIR *fnaFilesDirectoryPointer;
    struct dirent *direntFnaDirectory;
    fnaFilesDirectoryPointer = opendir(fnaFilesDirectory);
    char checkIfFNA[fnaNameBufferSize];
    char fnaString[fnaNameBufferSize] = "fna";
    int fnaFilesDirectoryStringLengthMinusOne = minimumFnaFileStringLength - 1;
    if(fnaFilesDirectoryPointer) {
        while ((direntFnaDirectory = readdir(fnaFilesDirectoryPointer)) != NULL) {
            int strlenString = strlen(direntFnaDirectory->d_name);
            if( strlenString > minimumFnaFileStringLength) {
                memcpy(checkIfFNA, &direntFnaDirectory->d_name[strlenString - fnaFilesDirectoryStringLengthMinusOne], fnaFilesDirectoryStringLengthMinusOne);
                if (strcmp(checkIfFNA,fnaString) == 0) {
                    fnaFileCount++;
                }
            }
        }
        closedir(fnaFilesDirectoryPointer);
    } else {
        printf("%s", "Error: fnaFilesDirectory[fnaFilesDirectoryStringLength] is null\n");
        exit(EXIT_FAILURE);
    }
    if(fnaFileCount == 0) { 
    	printf("%s", "Error: fnaFileCount is 0\n");
        exit(EXIT_FAILURE);
    }
    return fnaFileCount;
}
