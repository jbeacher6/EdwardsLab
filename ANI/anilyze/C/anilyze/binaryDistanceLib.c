#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "binaryDistanceLib.h"

int binaryDistance(char* string1, char* string2, int stringLength) {
    int distance = 0;
    for(int i = 0; i < stringLength; i++) {
        if(i%2 == 0) {
            distance = distance + ((string1[i] - '0' ^ string2[i] - '0') ^ (string1[i+1] - '0' ^ string2[i+1] - '0')) + ((string1[i] - '0' ^ string2[i] - '0') & (string1[i+1] - '0' ^ string2[i+1] - '0'));
        }
    }
    return distance;
}
