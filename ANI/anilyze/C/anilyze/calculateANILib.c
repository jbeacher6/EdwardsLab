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
#include "calculateANILib.h"
#include "uthash.h"

#define KMERLENGTHCONST 60
#define fnaNameBufferSize 4
#define LINESIZE 70
#define fnaFilesDirectoryStringLengthBuffer 302
#define minimumFnaFileStringLength 4
#define nameLength 300

//const int LINESIZE = 70;
//const int fnaFilesDirectoryStringLengthBuffer = 302;
//const int minimumFnaFileStringLength = 4;
//const int fnaNameBufferSize = 4;
//const int nameLength = 300;
//const int KMERLENGTHCONST = 60;

//-------------------------------------------------------------------

struct f1_struct {
    int num;                   
    char kmer[KMERLENGTHCONST];
    UT_hash_handle hh;         
};

struct f1_struct *kmers_f1 = NULL;

void add_f1(char *kmer) {
    struct f1_struct *s;
    HASH_FIND_STR(kmers_f1, kmer, s);  
    if (s == NULL) {
      s = (struct f1_struct*)malloc(sizeof(struct f1_struct));
      s->num = 0;
      strncpy(s->kmer, kmer, KMERLENGTHCONST);
      HASH_ADD_STR(kmers_f1, kmer, s);  
    }
    s->num++;
    strcpy(s->kmer, kmer);
}

void print_f1() {
    struct f1_struct *s;
    printf("\nf1\n");
    for(s=kmers_f1; s != NULL; s=(struct f1_struct*)(s->hh.next)) {
        printf("%s : %d\n", s->kmer, s->num);
    }
}

void delete_free_f1() {
  struct f1_struct *s, *tmp;
  HASH_ITER(hh, kmers_f1, s, tmp) {
    HASH_DEL(kmers_f1, s);  
    free(s);               
  }
}

//-------------------------------------------------------------------

struct f2_struct {
    int num;                 
    char kmer[KMERLENGTHCONST];
    UT_hash_handle hh;       
};

struct f2_struct *kmers_f2 = NULL;

void add_f2(char *kmer) {
    struct f2_struct *s;
    HASH_FIND_STR(kmers_f2, kmer, s);  
    if (s == NULL) {
      s = (struct f2_struct*)malloc(sizeof(struct f2_struct));
      s->num = 0;
      strncpy(s->kmer, kmer, KMERLENGTHCONST);
      HASH_ADD_STR(kmers_f2, kmer, s);  
    }
    s->num++;
    strcpy(s->kmer, kmer);
}

void print_f2() {
    struct f2_struct *s;
    printf("\nf2\n");
    for(s=kmers_f2; s != NULL; s=(struct f2_struct*)(s->hh.next)) {
        printf("%s : %d\n", s->kmer, s->num);
    }
}

void delete_free_f2() {
  struct f2_struct *s, *tmp;
  HASH_ITER(hh, kmers_f2, s, tmp) {
    HASH_DEL(kmers_f2, s);
    free(s);               
  }
}

//-------------------------------------------------------------------

struct rc2_struct {
    int num;                   
    char kmer[KMERLENGTHCONST];
    UT_hash_handle hh;
};

struct rc2_struct *kmers_rc2 = NULL;

void add_rc2(char *kmer) {
    struct rc2_struct *s;
    HASH_FIND_STR(kmers_rc2, kmer, s);  
    if (s == NULL) {
      s = (struct rc2_struct*)malloc(sizeof(struct rc2_struct));
      s->num = 0;
      strncpy(s->kmer, kmer, KMERLENGTHCONST);
      HASH_ADD_STR(kmers_rc2, kmer, s);  
    }
    s->num++;
    strcpy(s->kmer, kmer);
}

void print_rc2() {
    struct rc2_struct *s;
    printf("\nrc2\n");
    for(s=kmers_rc2; s != NULL; s=(struct rc2_struct*)(s->hh.next)) {
        printf("%s : %d\n", s->kmer, s->num);
    }
}

void delete_free_rc2() {
  struct rc2_struct *s, *tmp;
  HASH_ITER(hh, kmers_rc2, s, tmp) {
    HASH_DEL(kmers_rc2, s);
    free(s);
  }
}

//-------------------------------------------------------------------

double f1_query_f2_rc2(const int KMERSIZE) {
    int ANI = 0;
    int worstANI = 0;
    struct f1_struct *f1;
    struct f2_struct *f2;
    struct rc2_struct *rc2;
    rc2 = kmers_rc2;
    for(f1=kmers_f1; f1 != NULL; f1=(struct f1_struct*)(f1->hh.next)) {
      HASH_FIND_STR(kmers_f2, f1->kmer, f2);
      if(f2 == NULL) {
        ANI = ANI + KMERSIZE*(f1->num);
        worstANI = worstANI + KMERSIZE*(f1->num);
      } else {
        worstANI = worstANI + KMERSIZE*(f1->num);
      }
      HASH_FIND_STR(kmers_rc2, f1->kmer, rc2);
      if(rc2 == NULL) {
        ANI = ANI + KMERSIZE*(f1->num);
        worstANI = worstANI + KMERSIZE*(f1->num);
      } else {
        worstANI = worstANI + KMERSIZE*(f1->num);
      }
  }
  delete_free_f1();
  delete_free_f2();
  delete_free_rc2();
  return 100 - (((double) ANI / ((double) worstANI * (double) ANI))*100);
}

double f1_query_f2_rc2_print(const int KMERSIZE) {
    int ANI = 0;
    int worstANI = 0;
    struct f1_struct *f1;
    struct f2_struct *f2;
    struct rc2_struct *rc2;
    rc2 = kmers_rc2;
    for(f1=kmers_f1; f1 != NULL; f1=(struct f1_struct*)(f1->hh.next)) {
      HASH_FIND_STR(kmers_f2, f1->kmer, f2);
      if(f2 == NULL) {
        printf("%s not in f2\n", f1->kmer);
        ANI = ANI + KMERSIZE*(f1->num);
        worstANI = worstANI + KMERSIZE*(f1->num);
        printf("ANI: %d\n", ANI);
        printf("worstANI: %d\n", worstANI);
        printf("\n");  
      } else {
        printf("%s in f2\n", f1->kmer);
        worstANI = worstANI + KMERSIZE*(f1->num);
        printf("ANI: %d\n", ANI);
        printf("worstANI: %d\n", worstANI);
        printf("\n");  
      }
      HASH_FIND_STR(kmers_rc2, f1->kmer, rc2);
      if(rc2 == NULL) {
        printf("%s not in rc2\n", f1->kmer);
        ANI = ANI + KMERSIZE*(f1->num);
        worstANI = worstANI + KMERSIZE*(f1->num);
        printf("ANI: %d\n", ANI);
        printf("worstANI: %d\n", worstANI);
        printf("\n"); 
      } else {
        printf("%s in f2\n", f1->kmer);
        worstANI = worstANI + KMERSIZE*(f1->num);
        printf("ANI: %d\n", ANI);
        printf("worstANI: %d\n", worstANI);
        printf("\n"); 
      }
  }
  printf("ANI: %d\n", ANI);
  printf("worstANI: %d\n", worstANI);
  delete_free_f1();
  delete_free_f2();
  delete_free_rc2();
  return 100 - (((double) ANI / ((double) worstANI * (double) ANI))*100);
}

//-------------------------------------------------------------------

void calculateANI(const char fnaFilesDirectory[], const int KMERSIZE, const int FILESIMILARITYCONST, const int amountOfFNAFilesBuffer) {
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
    char *ptr = NULL, *ptr2 = NULL, *ptr3 = NULL;
    char kmerArr[kmerSizeMod], kmerArr2[kmerSizeMod], kmerArr3[kmerSizeMod];
      for(int i = 0; i < fnaFileCount; i++) {
        for(int j = i; j < fnaFileCount; j++) {
            double fileSimilarityDouble = 0;
            //int fileSimilarityInt = 0;
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
                //fileSimilarityInt = (int) fileSimilarityDouble;
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
                    double hundredSimilarity = 0;
                    if(file1Size < file2Size) {
                        minimumLines = numLines1;
                        maximumLines = numLines2;
                    } else {
                        minimumLines = numLines2;
                        maximumLines = numLines1;
                    }
                    int numCharsMin2 = numCharsMin;
                    ptr=fna1Characters[0];
                    ptr2=fna2Characters[0];
                    int numCharsMinHalf = numCharsMin2 / 2;
                    ptr3=fna2Characters[0];
                    for(int i = 0; i < numCharsMinHalf; i++) {
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
                            add_f1(kmerArr);
                            add_f2(kmerArr2);
                            add_rc2(kmerArr3);
                        }
                        f1_query_f2_rc2(KMERSIZE);
                        //f1_query_f2_rc2_print(KMERSIZE);
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
                    printf("(");
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
                    printf("','%d','%f'),", KMERSIZE, hundredSimilarity);
                    printf("\n");
                    free(fna1Characters);
                    free(fna2Characters);
                }
            }
        } 
    }
}
