#include <sstream>
#include <fstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <stdexcept>

// Simple tokenizer: splits text by whitespace
std::vector<std::string> simple_tokenize(const std::string& text) {
    std::vector<std::string> tokens;
    std::istringstream stream(text);
    std::string token;
    while (stream >> token) {
        tokens.push_back(token);
    }
    return tokens;
}

// Core n-gram extraction from text
std::unordered_map<std::string, int> extract_ngrams_from_text(const std::string& text, int n) {
    std::vector<std::string> tokens = simple_tokenize(text);
    std::unordered_map<std::string, int> ngram_counts;

    if (n <= 0 || tokens.size() < n) {
        return ngram_counts;  // Return empty if n is invalid
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

// Handle both text input or file path
std::unordered_map<std::string, int> extract_ngrams(const std::string& input, int n, bool is_file = false) {
    if (is_file) {
        std::ifstream infile(input);
        if (!infile.is_open()) {
            throw std::runtime_error("Cannot open file: " + input);
        }
        std::string line, text;
        while (std::getline(infile, line)) {
            text += line + " ";
        }
        infile.close();
        return extract_ngrams_from_text(text, n);
    } else {
        return extract_ngrams_from_text(input, n);
    }
}
