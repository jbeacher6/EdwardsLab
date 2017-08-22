#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void binDistance(char* string1, char* string2) {
    int ANI = 0;
    for(int i = 0; i < strlen(string1); i++) {
        if(i%2 == 0) {
            //printf("%d", i);
            printf("\n%d", string1[i] - '0' ^ string2[i] - '0');
            printf("%d\n", string1[i+1] - '0' ^ string2[i+1] - '0');
            //ANI = ANI + (i ^ i2) + (i & i2);
            ANI = ANI + ((string1[i] - '0' ^ string2[i] - '0') ^ (string1[i+1] - '0' ^ string2[i+1] - '0')) + ((string1[i] - '0' ^ string2[i] - '0') & (string1[i+1] - '0' ^ string2[i+1] - '0'));
        }
    }
    //printf("\nANI: %d\n", ANI);
    return ANI;
}
