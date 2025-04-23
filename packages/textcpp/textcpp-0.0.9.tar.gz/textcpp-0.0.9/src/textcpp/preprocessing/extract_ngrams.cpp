#include <sstream>
#include <fstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <stdexcept>
#include "tokenizer.h"




std::unordered_map<std::string, int> extract_ngrams(
    const std::string& input, 
    int n, 
    const Tokenizer& tokenizer, 
    bool is_file = false) 
{
    std::string text;

    if (is_file) {
        std::ifstream infile(input);
        if (!infile.is_open()) {
            throw std::runtime_error("Cannot open file: " + input);
        }
        std::string line;
        while (std::getline(infile, line)) {
            text += line + " ";
        }
        infile.close();
    } else {
        text = input;
    }

    std::vector<std::string> tokens = tokenizer.tokenize(text);
    std::unordered_map<std::string, int> ngram_counts;

    if (n <= 0 || tokens.size() < n) {
        return ngram_counts;
    }

    for (size_t i = 0; i + n <= tokens.size(); ++i) {
        std::string ngram = tokens[i];
        for (int j = 1; j < n; ++j) {
            ngram += " " + tokens[i + j];
        }
        ngram_counts[ngram]++;
    }
    return ngram_counts;
}