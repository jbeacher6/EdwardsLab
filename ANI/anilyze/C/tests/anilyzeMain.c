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
#include "binaryDistanceLib.h"
#include "calculateANILib.h"
#include "numberOfFilesLib.h"

int main(int argc, char *argv[]) {
    if(argc >= 3) {
        const int kmerSizeConstantParam = atoi(argv[2]);
        const int fileSimConstantParam = atoi(argv[3]);
        printf("INSERT INTO anilyzeTable (Genus1, Species1, Genus2, Species2, Percentage) \nVALUES \n");
        calculateANI(argv[1], kmerSizeConstantParam, fileSimConstantParam, numberOfFiles(argv[1]));
    }
    else {
        printf("%s", "Error, ./anilyzeExeC <User/path/locationOfFormattedFiles> <kmerSizeInteger> <filePercentSimilarityConstantInteger>");
        printf("%s", "Example: ./anilyzeExeC /Users/jon/desktop/anilyze/C/tests/sampleTestFiles/ 4 1");
        printf("%s", "Please readme for more information on formattedFiles");
        exit(EXIT_FAILURE);
    }
    return 0;
}
