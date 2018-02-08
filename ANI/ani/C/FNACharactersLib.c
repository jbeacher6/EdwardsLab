#include <stdio.h>//Needed for FILE, fopen(), fclose() and fgets()
#include <string.h>//Needed for memcpy()
#include <stdlib.h>//Needed for EXIT statements and free()
#include "FNACharactersLib.h"

const int DATABUFFER = 8192;//Size of a single char line, can possibly be as low as 260 to reduce memory usage 
char** fnaCharactersOf(const char* fnaFileNameAndLocation, const int LINESIZE, const int numberOfLines) {
    FILE *fnaPointer;//pointer to the fna file
    const char* fnaName = fnaFileNameAndLocation; //name of the .fna file
    char singleCharLine[DATABUFFER];// firstLineOfChars[DATABUFFER];
    fnaPointer = fopen(fnaName, "r");//open the .fna file
    if(fnaPointer == NULL) {//if the pointer is null then 
        printf("%s", "Error(FNACharactersLib): fnaPointer is null\n");//print error 
        exit(EXIT_FAILURE);//exit program
    }
    char **fnaArrayCalloc = (char**) calloc(numberOfLines, sizeof(char*));
    if(fnaArrayCalloc == NULL) {//If the calloc operation was not successful
        printf("%s", "Error(FNACharactersLib: fnaArrayCalloc\n");//print error
        exit(EXIT_FAILURE);//exit the program
    }
    for(int i = 0; i < numberOfLines; i++) {//for the number of lines in the program
        fnaArrayCalloc[i] = (char *) calloc(LINESIZE, sizeof(char));//allocate space
   }
   int j = 0;//start
    while (fgets(singleCharLine, DATABUFFER, fnaPointer) != NULL) {
        memcpy(fnaArrayCalloc[j], &singleCharLine, LINESIZE);//copy
        j++;//next line
    }
    fclose(fnaPointer);//close the pointer to the file
    char **fnaCharCalloc = (char**) calloc(1, sizeof(char));//allocate space
    if(fnaCharCalloc == NULL) {//if allocating space was not successful 
        printf("%s", "Error(FNACharactersLib): fnaCharCalloc\n");//throw error
        exit(EXIT_FAILURE);//exit the program
    }
    fnaCharCalloc[0] = (char *) calloc(LINESIZE*numberOfLines, sizeof(char));//allocate space
    for (int k = 0; k < numberOfLines; k++) {//for number of lines
        memcpy(fnaCharCalloc[0] + LINESIZE*k, fnaArrayCalloc[k], LINESIZE);//copy
    }
    for(int l = 0; l < numberOfLines; l++) {//for number of lines
        free(fnaArrayCalloc[l]);//free the array
    }
    free(fnaArrayCalloc);//free the remaining pointers
    return (char**) fnaCharCalloc;//return the characters in the .fna file
}
