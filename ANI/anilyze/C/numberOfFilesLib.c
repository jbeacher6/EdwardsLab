#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <dirent.h>
#include "numberOfFilesLib.h"

int numberOfFiles(const char fnaFilesDirectory[]) {
    DIR *fnaFilesDirectoryPointer;
    struct dirent *direntFnaDirectory;
    fnaFilesDirectoryPointer = opendir(fnaFilesDirectory);
    int fnaFileCount = 0;
    if(fnaFilesDirectoryPointer) {
        while ((direntFnaDirectory = readdir(fnaFilesDirectoryPointer)) != NULL) {
            fnaFileCount++;   
            }
        closedir(fnaFilesDirectoryPointer);
    } else {
        printf("%s", "Error:(numberOfFiles): fnaFilesDirectory[] is null\n");
        exit(EXIT_FAILURE);
    }
    return fnaFileCount; 
}
