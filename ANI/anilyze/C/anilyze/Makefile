CC = gcc
CFLAGS  = -g -Wall
CFLAGS = -std=c99

default: anilyzeExeC

anilyzeExeC:  calculateANILib.o numberOfFilesLib.o numberOfLinesLib.o FNACharactersLib.o 
	$(CC) $(CFLAGS) anilyzeMain.c calculateANILib.o numberOfFilesLib.o numberOfLinesLib.o FNACharactersLib.o -o anilyzeExeC

calculateANILib.o: calculateANILib.c calculateANILib.h FNACharactersLib.h numberOfLinesLib.h
	$(CC) $(CFLAGS) -c calculateANILib.c

numberOfFilesLib.o:  numberOfFilesLib.c numberOfFilesLib.h
	$(CC) $(CFLAGS) -c numberOfFilesLib.c

numberOfLinesLib.o:  numberOfLinesLib.c numberOfLinesLib.h
	$(CC) $(CFLAGS) -c numberOfLinesLib.c

FNACharactersLib.o:  FNACharactersLib.c FNACharactersLib.h 
	$(CC) $(CFLAGS) -c FNACharactersLib.c

clean: 
	$(RM) anilyzeExeC *.o *~