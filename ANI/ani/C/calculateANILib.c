#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <libgen.h>
#include <math.h>
#include "FNACharactersLib.h"
#include "numberOfLinesLib.h"
#include "calculateANILib.h"
#include "uthash.h"

#define KMERLENGTHCONST 100
#define fnaNameBufferSize 4
#define LINESIZE 70
#define fnaFilesDirectoryStringLengthBuffer 302
#define minimumFnaFileStringLength 4
#define nameLength 300

//-------------------------------------------------------------------

struct f1_struct {
    int num;                    /* key */
    char kmer[KMERLENGTHCONST];
    UT_hash_handle hh;         /* makes this structure hashable */
};

struct f1_struct *kmers_f1 = NULL;

void add_f1(char *kmer) {
    struct f1_struct *s;
    HASH_FIND_STR(kmers_f1, kmer, s);  /* id already in the hash? */
    if (s == NULL) {
      s = (struct f1_struct*)malloc(sizeof(struct f1_struct));
      s->num = 0;
      strncpy(s->kmer, kmer, 10);
      //s->name = name;
      HASH_ADD_STR(kmers_f1, kmer, s);  /* id: name of key field */
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
    HASH_DEL(kmers_f1, s);  /* delete it (users advances to next) */
    free(s);                /* free it */
  }
}

//-------------------------------------------------------------------

struct f2_struct {
    int num;                    /* key */
    char kmer[KMERLENGTHCONST];
    UT_hash_handle hh;         /* makes this structure hashable */
};

struct f2_struct *kmers_f2 = NULL;

void add_f2(char *kmer) {
    struct f2_struct *s;
    HASH_FIND_STR(kmers_f2, kmer, s);  /* id already in the hash? */
    if (s == NULL) {
      s = (struct f2_struct*)malloc(sizeof(struct f2_struct));
      s->num = 0;
      strncpy(s->kmer, kmer, 10);
      //s->name = name;
      HASH_ADD_STR(kmers_f2, kmer, s);  /* id: name of key field */
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
    HASH_DEL(kmers_f2, s);  /* delete it (users advances to next) */
    free(s);                /* free it */
  }
}

//-------------------------------------------------------------------

struct rc2_struct {
    int num;                    /* key */
    char kmer[KMERLENGTHCONST];
    UT_hash_handle hh;         /* makes this structure hashable */
};

struct rc2_struct *kmers_rc2 = NULL;

void add_rc2(char *kmer) {
    struct rc2_struct *s;
    HASH_FIND_STR(kmers_rc2, kmer, s);  /* id already in the hash? */
    if (s == NULL) {
      s = (struct rc2_struct*)malloc(sizeof(struct rc2_struct));
      s->num = 0;
      strncpy(s->kmer, kmer, 10);
      //s->name = name;
      HASH_ADD_STR(kmers_rc2, kmer, s);  /* id: name of key field */
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
    HASH_DEL(kmers_rc2, s);  /* delete it (users advances to next) */
    free(s);                /* free it */
  }
}

//-------------------------------------------------------------------

double ani_f1_f2_rc2_lev2_print(int kmerSizeParam) {
    double kmerLength = (double) kmerSizeParam;
    double kmerCount = 0;
    double totalANI = 0;
    double finalANI = 0;
    double currentANI = kmerLength;
    double worstCaseANI = 0;
    struct f1_struct *f1;
    struct f2_struct *f2;
    struct rc2_struct *rc2;
    rc2 = kmers_rc2;
    printf("\n\nF1: count\n");
    printf("F2: count\n");
    printf("RC2: count\n\n");
    int found = 0;

    for(f1=kmers_f1; f1 != NULL; f1=(struct f1_struct*)(f1->hh.next)) {
      HASH_FIND_STR(kmers_f2, f1->kmer, f2);
      if(f2 == NULL) {//f2 not available
        HASH_FIND_STR(kmers_rc2, f1->kmer, rc2);
        if(rc2 == NULL) {//rc2 not available
        } else {//rc2 available
          found = 1;
          currentANI = kmerLength*(abs(f1->num - rc2->num));
          totalANI = currentANI + totalANI;
          worstCaseANI = f1->num*kmerLength + worstCaseANI;
          printf("rc2 found\n");
          printf("f1: %f\n", currentANI);
          printf("%s : %d\n", f1->kmer, f1->num);
          //printf("%s : %d\n", f2->kmer, f2->num);
          printf("%s : %d\n", rc2->kmer, rc2->num);//printf("\n");
        }
      } else {//f2 available
        found = 1;
        currentANI = kmerLength*(abs(f1->num - f2->num));
        totalANI = currentANI + totalANI;
        worstCaseANI = f1->num*kmerLength + worstCaseANI;

        printf("f2 found\n");
        printf("currentANI: %f\n", currentANI);
        printf("%s : %d\n", f1->kmer, f1->num);
        printf("%s : %d\n", f2->kmer, f2->num);
        //printf("%s : %d\n", rc2->kmer, rc2->num);//printf("\n");
      }
    kmerCount++;
    found = 0;
    printf("kmerCount: %f\n", kmerCount);
    printf("currentANI: %f\n", currentANI);
    printf("totalANI: %f\n", totalANI);
    currentANI = kmerLength;
    printf("\n");
    printf("\n");
  }


  printf("totalANI: %f\n", totalANI);
  printf("worstCaseANI: %f\n", worstCaseANI);
  printf("%f\n", totalANI);
  printf("%f\n", worstCaseANI);


  printf("ANI1: %f\n", 100 - (totalANI/(worstCaseANI)*100));
  finalANI = 100 - (totalANI/(worstCaseANI)*100);
  delete_free_f1();
  delete_free_f2();
  delete_free_rc2();
  return finalANI;
}

//-------------------------------------------------------------------

double ani_f1_f2_rc2_accurate(int kmerSizeParam) {
    double kmerLength = (double) kmerSizeParam;
    double kmerCount = 0;
    double totalANI = 0;
    double finalANI = 0;
    double currentANI = kmerLength;
    double worstCaseANI = 0;
    struct f1_struct *f1;
    struct f2_struct *f2;
    struct rc2_struct *rc2;
    rc2 = kmers_rc2;
    for(f1=kmers_f1; f1 != NULL; f1=(struct f1_struct*)(f1->hh.next)) {
      HASH_FIND_STR(kmers_f2, f1->kmer, f2);
      if(f2 == NULL) {//f2 not available
        HASH_FIND_STR(kmers_rc2, f1->kmer, rc2);
        if(rc2 == NULL) {//rc2 not available
        } else {//rc2 available
          currentANI = kmerLength*(abs(f1->num - rc2->num));
          totalANI = currentANI + totalANI;
          worstCaseANI = f1->num*kmerLength + worstCaseANI;
        }
      } else {//f2 available
        currentANI = kmerLength*(abs(f1->num - f2->num));
        totalANI = currentANI + totalANI;
        worstCaseANI = f1->num*kmerLength + worstCaseANI;
      }
    kmerCount++;
  }
  finalANI = 100 - (totalANI/(worstCaseANI)*100);
  delete_free_f1();
  delete_free_f2();
  delete_free_rc2();
  return finalANI;
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
    char** fnaArrayCalloc = (char**) calloc(amountOfFNAFilesBuffer, sizeof(char*));
    if(fnaArrayCalloc == NULL) { 
        printf("%s", "Error: kmersArrayCalloc\n");
        exit(EXIT_FAILURE);
    }
    for(int i = 0; i < amountOfFNAFilesBuffer; i++) {
        fnaArrayCalloc[i] = (char *) calloc(nameLength, sizeof(char));
        if(fnaArrayCalloc[i] == NULL) { 
            printf("%s", "Error: kmersArrayCalloc\n");
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
                    memcpy(fnaArrayCalloc[fnaFileCount], fnaFilesDirectory, strlenString2);
                    memcpy(fnaArrayCalloc[fnaFileCount] + strlenString2, &direntFnaDirectory->d_name, strlenString);
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
            stat(fnaArrayCalloc[i], &sa);
            stat(fnaArrayCalloc[j], &sb);
            file1Size = sa.st_size;
            file2Size = sb.st_size;
            if(file1Size < file2Size) {
                numCharsMin =  file1Size;
                numCharsMax =  file2Size;
            } else {
                numCharsMin = file2Size;
                numCharsMax = file1Size;
            }
            if(strcmp(fnaArrayCalloc[i], fnaArrayCalloc[j]) != 0) {
                fileSimilarityFloatDecimal = ((float) numCharsMin / (float) numCharsMax);
                fileSimilarityDouble = ((double) numCharsMin / (double) numCharsMax )*100;
                //fileSimilarityInt = (int) fileSimilarityDouble;
                if(fileSimilarityFloatDecimal*100 > FILESIMILARITYCONST) {
                    int numLines1 = numberOfLines(LINESIZE, fnaArrayCalloc[i]);
                    int numLines2 = numberOfLines(LINESIZE, fnaArrayCalloc[j]);
                    char **fna1Characters = NULL;
                    fna1Characters = fnaCharactersOf(fnaArrayCalloc[i], LINESIZE, numLines1);
                    char **fna2Characters = NULL;
                    fna2Characters = fnaCharactersOf(fnaArrayCalloc[j], LINESIZE, numLines2);
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
                        //print_f1();
                        //ani_f1_f2_rc2_lev_print(KMERSIZE);
                        //ani_f1_f2_rc2_lev(KMERSIZE);
                        //ani_f1_f2_rc2_binary(KMERSIZE);
                        //ani_f1_f2_rc2_binary_print(KMERSIZE);
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
                    ptr_g1 = strrchr(fnaArrayCalloc[i], g1_str);
                    ptr_s1 = strrchr(fnaArrayCalloc[i], s1_str);
                    ptr_f1 = strrchr(fnaArrayCalloc[i], f1_str);
                    FILE *f = fopen("ani.txt", "a");
                    if (f == NULL) {
                      printf("Error opening ani.txt\n");
                      exit(1);
                    }
                    fprintf(f, "('");
                    while(ptr_g1 != ptr_s1) {
                       if(g1_start == 1) {
                          ptr_g1++;
                          g1_start = 0;
                       }    
                       fprintf(f, "%c", *ptr_g1);
                       ptr_g1++;
                    }
                    fprintf(f, "','");
                    while(ptr_s1 != ptr_f1) {
                        if(s1_start == 1) {
                            ptr_s1++;
                            s1_start = 0;
                        }
                        printf("%c", *ptr_s1);
                        ptr_s1++;
                    }
                    fprintf(f, "','");
                    int g2_str = '/';
                    int s2_str = '_';
                    int f2_str = '.';
                    char *ptr_g2 = NULL;
                    char *ptr_s2 = NULL;
                    char *ptr_f2 = NULL;
                    ptr_g2 = strrchr(fnaArrayCalloc[j], g2_str);
                    ptr_s2 = strrchr(fnaArrayCalloc[j], s2_str);
                    ptr_f2 = strrchr(fnaArrayCalloc[j], f2_str);
                    while(ptr_g2 != ptr_s2) {
                       if(g2_start == 1) {
                            ptr_g2++;
                            g2_start = 0;
                        }
                       fprintf(f, "%c", *ptr_g2);
                       ptr_g2++;
                    }
                    fprintf(f, "','");
                    while(ptr_s2 != ptr_f2) {
                        if(s2_start == 1) {
                            ptr_s2++;
                            s2_start = 0;
                        }
                        fprintf(f, "%c", *ptr_s2);
                        ptr_s2++;
                    }
                   
                    fprintf(f, "','%d','%f'),\n", KMERSIZE, ani_f1_f2_rc2_accurate(KMERSIZE));
                    fclose(f);
                    //printf("','%d','%f'),", KMERSIZE, ani_f1_f2_rc2_accurate(KMERSIZE));
                    //printf("\n");
                    free(fna1Characters[0]);
		                free(fna1Characters);
    		            free(fna2Characters[0]);
            	      free(fna2Characters);
            	      free(kmers_f1);
            	      free(kmers_f2);
            	      free(kmers_rc2);
		            }
            }
        } 
    }
    for(int i = 0; i < amountOfFNAFilesBuffer; i++) {
        free(fnaArrayCalloc[i]);
        }
    free(fnaArrayCalloc);
}
