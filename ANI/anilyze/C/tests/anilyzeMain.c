#include <stdio.h>//Library used for input and output
#include <stdlib.h>//Library used for atoi()
#include "calculateANILib.h"//
#include "numberOfFilesLib.h"//
/*
The main of the program will start by getting the arguments from the command line to retrieve the formatted files, the kmer 
size and percent file similarity threshold. Once the arguments have been entered, the program will run calculateANI. 
The calculate ANI library relies on numberOfLinesLib, FNACharactersLib, binaryDistanceLib and numberOfFilesLib.
Param int argc will get the number of arguments specified. There should be a total of four command line arguments 
The first argument is ./anilyzeExceC , the second is the location of the formatted files, the third argument will be 
the file similarity threshold. 
Argument 1: <User/path/locationOfFormattedFiles> : This is the formatted files from the Anilyze python program. 
The reference is ./README (not ./C/tests/README) for <User/path/locationOfFormattedFiles> for the setup files scripts.
Argument 2: <kmerSizeInteger> : This is the kmer integer size to input into the program. For example, a k-mer isze of ten would be 10.
Argument 3: <filePercentSimilarityThresholdConstantInteger> : This is the percent similarity threshold to limit file comparisons. 
If one file has one million bytes but the other has two bytes, limiting this comparison can be done by inputting a valid integer greater 
than one to specify a one percent file similarity threshold. 
*/
int main(int argc, char *argv[]) {//the main that will get the arguments detailed above
    if(argc == 4) {//verify that the number of arguments is 4
        const int kmerSizeConstantParam = atoi(argv[2])*2;//The program will multiply the kmer size by two to have a valid binary kmer size
        const int fileSimilarityThresholdConstantParam = atoi(argv[3]);//Get the percent size threshold
        printf("INSERT INTO anilyzeTable (Genus1, Species1, Genus2, Species2, Percentage) \nVALUES \n");//SQL insert statement for futher analysis
        calculateANI(argv[1], kmerSizeConstantParam, fileSimilarityThresholdConstantParam, numberOfFiles(argv[1]));//call calculateANILib with arguments
    }
    else {//the number of arguments was not correct and print a help section for valid input
        printf("%s", "Error, ./anilyzeExeC <User/path/locationOfFormattedFiles> <kmerSizeInteger> <filePercentSimilarityThresholdConstantInteger>");//display help
        printf("%s", "Example: ./anilyzeExeC /Users/jon/desktop/anilyze/C/tests/sampleTestFiles/ 4 1");//Sample execution 
        printf("%s", "Please ./README for more information on formattedFiles");//display on how to format the files before running ./aniluzeExeC
        exit(EXIT_FAILURE);//quit the program
    }
    return 0;//return valid
}
