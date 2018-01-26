#ifndef _CALCULATEANILIB_H_
#define _CALCULATEANILIB_H_

void calculateANI(const char fnaFilesDirectory[], const int KMERSIZE, const int FILESIMILARITYCONST, const int amountOfFNAFilesBuffer);

void add_f1(char *kmer);

void add_f2(char *kmer);

void add_rc2(char *kmer);

void print_f1();

void delete_free_f1();

void print_f2();

void delete_free_f2();

void print_rc2();

void delete_free_rc2();

double f1_query_f2_rc2_print(const int KMERSIZE);

double f1_query_f2_rc2(const int KMERSIZE);

double f1_query_f2_rc2_single(const int KMERSIZE);

#endif