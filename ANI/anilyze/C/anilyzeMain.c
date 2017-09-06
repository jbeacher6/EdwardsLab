#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <libgen.h>
#include "numberOfLinesLib.h"
#include "FNACharactersLib.h"
#include "levenshteinDistanceLib.h"
#include "binaryDistanceLib.h"
//fna Files Directory Constant: fna files of forward and concatinated reverse complimented ncbi files
const int LINESIZE = 70;
const int fnaFilesDirectoryStringLengthBuffer = 302;
const int minimumFnaFileStringLength = 4;
const int fnaNameBufferSize = 4;
//const int amountOfFNAFilesBuffer = 15200;
const int nameLength = 300;

void calculateANI(const char fnaFilesDirectory[], const int KMERSIZE, const int FILESIMILARITYCONST, const int amountOfFNAFilesBuffer);

int main(int argc, char *argv[]) {
    if(argc >= 4) {
        //const char fnaFilesDirectoryConstant[fnaFilesDirectoryStringLengthBuffer] = {*argv[1]};
        const int kmerSizeConstant = atoi(argv[2]);
        const int fileSimConstant = atoi(argv[3]);
        const int amountOFFNAFilesBufferConstant = atoi(argv[4]);
        //printf("directory: %s kmerSize*2: %d\n fileSimilarityConstant: %d amountOfFNAFilesBufferConstant %d\n", argv[1], kmerSizeConstant, fileSimConstant, amountOfFNAFilesBufferConstant);
        printf("INSERT INTO anilyzeTable (Genus1, Species1, Genus2, Species2, Percentage) \nVALUES \n");
        calculateANI(argv[1], kmerSizeConstant, fileSimConstant, amountOFFNAFilesBufferConstant);
    }
    else {
        printf("Error, incorrect arguments entered\n ./a.out /tree/directoryOfBinaryFNAFiles/ kmerSize fileSimilarityConstant amountOfFNAFiles \n ./a.out /tree/directoryOfBinaryFNAFiles/ kmerSize fileSimilarityConstant > output.txt");
        exit(EXIT_FAILURE);
    }
    return 0;
}

void calculateANI(const char fnaFilesDirectory[], const int KMERSIZE, const int FILESIMILARITYCONST, const int amountOfFNAFilesBuffer) {
    //printf("%s\n", *fnaFilesDirectory);
    //printf("%s\n", *fnaFilesDirectory2);
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
    char *ptr = NULL, *ptr2 = NULL, *ptr3 = NULL;
    char kmerArr[kmerSizeMod], kmerArr2[kmerSizeMod], kmerArr3[kmerSizeMod];
    //FILE *fnaPointer;
      for(int i = 0; i < fnaFileCount; i++) {
        for(int j = i; j < fnaFileCount; j++) {
            //printf("%s i \n", fnaArrayMalloc[i]);
            //printf("%s j \n", fnaArrayMalloc[j]);
            double fileSimilarityDouble = 0;
            int fileSimilarityInt = 0;
            float fileSimilarityFloatDecimal = 0;
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
            if(strcmp(fnaArrayMalloc[i], fnaArrayMalloc[j]) != 0) {
                fileSimilarityFloatDecimal = ((float) numCharsMin / (float) numCharsMax);
                fileSimilarityDouble = ((double) numCharsMin / (double) numCharsMax )*100;
                fileSimilarityInt = (int) fileSimilarityDouble;
                if(fileSimilarityFloatDecimal*100 > FILESIMILARITYCONST) {
                //printf("fileSimilarityInt:%d\n", fileSimilarityInt);
                //printf("fileSimilarityFloat: \n%f\n", fileSimilarityFloatDecimal*100);
                //printf("fileSimilarityConstant: \n%d\n", FILESIMILARITYCONST);
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
                    //int numCharsLeft = 0;
                    //int numKmersLeft = 0;
                    //int numEditDistanceValueLeft = 0;
                    int chr = 0;
                    int chr2 = 0;
                    int chr3 = 0;
                    int kmerCount = 0;
                    double total = 0; 
                    double difference = 0;
                    double similarity = 0;
                    double hundredSimilarity = 0;
                    if(file1Size < file2Size) {
                        minimumLines = numLines1;
                        maximumLines = numLines2;
                    } else {
                        minimumLines = numLines2;
                        maximumLines = numLines1;
                    }
                    int numCharsMin2 = numCharsMin;// - minimumLines;// - \n
                    int numCharsMax2 = numCharsMax;// - maximumLines;// - \n
                    //int numKmersMin = (numCharsMin2) - KMERSIZE;
                    //printf("numkmerMin: %d\n", numKmersMin);
                    int numKmersMax = (numCharsMax2) - KMERSIZE;
                    //printf("numCharsMin2: %d\n", numCharsMin2);
                    ptr=fna1Characters[0];
                    ptr2=fna2Characters[0];
                    int numCharsMinHalf = numCharsMin2 / 2;
                    ptr3=fna2Characters[0];
                    for(int i = 0; i < numCharsMinHalf; i++) {
                        if(i%2 == 0) {//account for binary
                            for(int j = 0; j < kmerSizeMod; j++) {
                                if(j == 0) {
                                    chr = i;
                                    chr2 = i;
                                    chr3 = i+numCharsMinHalf;
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
                            //int kmerANI = editDistance(kmerArr, kmerArr2, KMERSIZE, KMERSIZE);
                            int kmerANI = binaryDistance(kmerArr, kmerArr2, KMERSIZE);
                            /*
                            printf("kmerArr:  %s\n", kmerArr);
                            printf("kmerArr2: %s\n", kmerArr2);
                            printf("kmerANI: %d\n", kmerANI);*/
                            int kmerANI2 = binaryDistance(kmerArr, kmerArr3, KMERSIZE);
                            /*
                            printf("kmerArr:  %s\n", kmerArr);
                            printf("kmerArr3: %s\n", kmerArr3);
                            printf("kmerANI: %d\n", kmerANI2);*/
                            
                            if(kmerANI < kmerANI2) {
                                finalANI = finalANI + kmerANI;
                            } else {
                                finalANI = finalANI + kmerANI2;
                            }
                            
                            //finalANI = finalANI + kmerANI + kmerANI2;
                            kmerCount++;
                            //printf("kmerCount: %d\n", kmerCount);
                            }
                        }
                    total = (numKmersMax/2)*(KMERSIZE/2);//account for binary
                    //printf("numKmersMax: %d\n", numKmersMax/2);//account for binary
                    difference = finalANI/total;
                    similarity = 1 - difference;
                    hundredSimilarity = similarity*100;
                    //hundredSimilarity = similarity*fileSimilarityFloatDecimal*100;
					printf("   ('");
                    int g1_str = '/';
                    int s1_str = '_';
                    int f1_str = '.';
                    char *ptr_g1 = NULL;
                    char *ptr_s1 = NULL;
                    char *ptr_f1 = NULL;
                    int g1_start = 1;
                    int s1_start = 1;
                    int g2_start = 1;
                    int s2_start = 1;
                    ptr_g1 = strrchr(fnaArrayMalloc[i], g1_str);
                    ptr_s1 = strrchr(fnaArrayMalloc[i], s1_str);
                    ptr_f1 = strrchr(fnaArrayMalloc[i], f1_str);
                    //Genus1
                    while(ptr_g1 != ptr_s1) {
                       if(g1_start == 1) {
         				  ptr_g1++;
                       	  g1_start = 0;
                       }	
                       printf("%c", *ptr_g1);
                       ptr_g1++;
                    }
                    printf("','");
                    //Species1
                    while(ptr_s1 != ptr_f1) {
                    	if(s1_start == 1) {
                    		ptr_s1++;
                    		s1_start = 0;
                    	}
                       	printf("%c", *ptr_s1);
                       	ptr_s1++;
                    }
                    printf("','");
                    int g2_str = '/';
                    int s2_str = '_';
                    int f2_str = '.';
                    char *ptr_g2 = NULL;
                    char *ptr_s2 = NULL;
                    char *ptr_f2 = NULL;
                    ptr_g2 = strrchr(fnaArrayMalloc[j], g2_str);
                    ptr_s2 = strrchr(fnaArrayMalloc[j], s2_str);
                    ptr_f2 = strrchr(fnaArrayMalloc[j], f2_str);
                    //Genus2
                    while(ptr_g2 != ptr_s2) {
                       if(g2_start == 1) {
                    		ptr_g2++;
                    		g2_start = 0;
                    	}
                       printf("%c", *ptr_g2);
                       ptr_g2++;
                    }
                    printf("','");
                    //Species2 
                    while(ptr_s2 != ptr_f2) {
                    	if(s2_start == 1) {
                    		ptr_s2++;
                    		s2_start = 0;
                    	}
                    	printf("%c", *ptr_s2);
                    	ptr_s2++;
                    }
                    printf("','%f'),", hundredSimilarity);
                    printf("\n");
                    free(fna1Characters);
                    free(fna2Characters);
                    //return finalANI;
                    finalANI = 0;
                }
                /*
                else {
                    printf("\n %s %s File Similarity too low, similarity: %d\n", fnaArrayMalloc[i], fnaArrayMalloc[j], fileSimilarityInt);
                }*/ 
            }
        } 
    } 
    //printf("('','','','','');\n\n");
}
