#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <libgen.h>
#include "FNACharactersLib.h"
#include "numberOfLinesLib.h"
#include "binaryDistanceLib.h"
#include "calculateANILib.h"
const int LINESIZE = 70;
const int fnaFilesDirectoryStringLengthBuffer = 302;
const int minimumFnaFileStringLength = 4;
const int nameLength = 300;

void calculateANI(const char fnaFilesDirectory[], const int KMERSIZE, const int FILESIMILARITYCONST, const int ANIPERCENTAGETHRESHOLDCONST, const int amountOfFNAFilesBuffer) {
    int fnaFileCount = 0;
    DIR *fnaFilesDirectoryPointer;
    struct dirent *direntFnaDirectory;
    fnaFilesDirectoryPointer = opendir(fnaFilesDirectory);
    char checkIfFNA[4];
    char fnaString[4] = "fna";
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
                //if (strcmp(checkIfFNA,fnaString) == 0) {
                    int strlenString2 = strlen(fnaFilesDirectory);
                    memcpy(fnaArrayMalloc[fnaFileCount], fnaFilesDirectory, strlenString2);
                    memcpy(fnaArrayMalloc[fnaFileCount] + strlenString2, &direntFnaDirectory->d_name, strlenString);
                    fnaFileCount++;
                //}
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
      for(int i = 0; i < fnaFileCount; i++) {
        for(int j = i; j < fnaFileCount; j++) {
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
            if(strcmp(fnaArrayMalloc[i], fnaArrayMalloc[j]) != 0) {
                fileSimilarityFloatDecimal = ((float) numCharsMin / (float) numCharsMax);
                fileSimilarityDouble = ((double) numCharsMin / (double) numCharsMax )*100;
                fileSimilarityInt = (int) fileSimilarityDouble;
                if(fileSimilarityFloatDecimal*100 > FILESIMILARITYCONST) {
                    int numLines1 = numberOfLines(LINESIZE, fnaArrayMalloc[i]);
                    int numLines2 = numberOfLines(LINESIZE, fnaArrayMalloc[j]);
                    char **fna1Characters = NULL;
                    fna1Characters = fnaCharactersOf(fnaArrayMalloc[i], LINESIZE, numLines1);
                    char **fna2Characters = NULL;
                    fna2Characters = fnaCharactersOf(fnaArrayMalloc[j], LINESIZE, numLines2);
                    int minimumLines = 0;
                    int maximumLines = 0;
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
                    int numKmersMax = (numCharsMax2) - KMERSIZE;
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
                            int kmerANI = binaryDistance(kmerArr, kmerArr2, KMERSIZE);
                            int kmerANI2 = binaryDistance(kmerArr, kmerArr3, KMERSIZE);
                            if(kmerANI < kmerANI2) {
                                finalANI = finalANI + kmerANI;
                            } else {
                                finalANI = finalANI + kmerANI2;
                            }
                            kmerCount++;
                            }
                        }
                    total = (numKmersMax/2)*(KMERSIZE/2);//account for binary
                    difference = finalANI/total;
                    similarity = 1 - difference;
                    hundredSimilarity = similarity*100;
                    if((int) hundredSimilarity > ANIPERCENTAGETHRESHOLDCONST) {
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
                    while(ptr_g1 != ptr_s1) {
                       if(g1_start == 1) {
                          ptr_g1++;
                          g1_start = 0;
                       }    
                       printf("%c", *ptr_g1);
                       ptr_g1++;
                    }
                    printf("','");
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
                    while(ptr_g2 != ptr_s2) {
                       if(g2_start == 1) {
                            ptr_g2++;
                            g2_start = 0;
                        }
                       printf("%c", *ptr_g2);
                       ptr_g2++;
                    }
                    printf("','");
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
                    }
                    free(fna1Characters);
                    free(fna2Characters);
                    finalANI = 0;
                }
            }
        } 
    } //printf("('','','','','');\n\n");
}
