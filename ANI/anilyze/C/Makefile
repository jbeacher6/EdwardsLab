CC = gcc
CFLAGS  = -g -Wall

default: anilyzeExceC

anilyzeExceC:  numberOfLinesLib.o FNACharactersLib.o binaryDistanceLib.o 
	$(CC) $(CFLAGS) anilyzeMain.c numberOfLinesLib.o FNACharactersLib.o binaryDistanceLib.o -o anilyzeExceC

numberOfLines.o:  numberOfLinesLib.c numberOfLinesLib.h
	$(CC) $(CFLAGS) -c numberOfLinesLib.c

FNACharactersLib.o:  FNACharactersLib.c FNACharactersLib.h 
	$(CC) $(CFLAGS) -c FNACharactersLib.c

binaryDistanceLib.o:  binaryDistanceLib.c binaryDistanceLib.h 
	$(CC) $(CFLAGS) -c binaryDistanceLib.c

clean: 
	$(RM) anilyzeExceC *.o *~