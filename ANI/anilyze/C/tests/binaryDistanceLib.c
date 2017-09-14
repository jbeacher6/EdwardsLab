#include <stdio.h>
#include "binaryDistanceLib.h"
/*
This library counts the distance between two strings that were previously converted to binary.
A levenshteinDistance(A,C,1) would calculate a distance of one.
binaryDistance(00,01,2) would return a distance of one.
Parameter string1: First string to compare 
Parameter string2: Second string to compare 
Parameter stringLength: The string lengths of string1 and string2(must be the same string length)
*/
int binaryDistance(char* string1, char* string2, int stringLength) {
    int distance = 0;
    //printf("stringLength: %d\n", stringLength);
    for(int i = 0; i < stringLength; i++) {//iterate each character in string length
        if(i%2 == 0) {//if the iteration of i is an even number. This is done to compare current with the next integer and also not create new binary letters
            //printf("%d", i);
            //printf("\n%d", string1[i] - '0' ^ string2[i] - '0');
            //printf("%d\n", string1[i+1] - '0' ^ string2[i+1] - '0');
            //<Integer between 0 and 9> - '0' will convert a string to an interger for integer values 0 and 1. <Integer between 0 and 9> - '0' is similar to atoi() function
            //00,01 will first be (00 XOR 01) to get 01. Then, the string will be split to form (0 XOR 1) + (0 & 1) = 1. This means A and C have a binary distance of one
            distance = distance + ((string1[i] - '0' ^ string2[i] - '0') ^ (string1[i+1] - '0' ^ string2[i+1] - '0')) + ((string1[i] - '0' ^ string2[i] - '0') & (string1[i+1] - '0' ^ string2[i+1] - '0'));
        }
    }
    //printf("\nANI: %d\n", ANI);
    return distance;//return the integer value of the distance
}
