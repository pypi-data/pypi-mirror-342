#ifndef OPERATIONS_H
#define OPERATIONS_H

#include <string>
#include <unordered_map>
#include "preprocessing/tokenizer.h"

// Forward declaration
class SimpleTokenizer;

int add(int a, int b);
int sub(int a, int b);
int count_words(const std::string& input);
std::unordered_map<std::string, int>  frequency_count(const std::string& path);
int  word_frequency_count(const std::string& path, std::string word);

std::unordered_map<std::string, int> extract_ngrams(
    const std::string& input, 
    int n, 
    const Tokenizer& tokenizer, 
    bool is_file = false);


#endif
