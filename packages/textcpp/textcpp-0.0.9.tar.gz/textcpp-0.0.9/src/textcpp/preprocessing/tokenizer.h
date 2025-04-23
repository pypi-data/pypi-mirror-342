#ifndef TOKENIZER_H
#define TOKENIZER_H

#include <vector>
#include <string>
#include <sstream>
#include <regex>

class Tokenizer {
public:
    virtual ~Tokenizer() = default;
    virtual std::vector<std::string> tokenize(const std::string& text) const = 0;
};

class SimpleTokenizer : public Tokenizer {
public:
    SimpleTokenizer() = default;

    std::vector<std::string> tokenize(const std::string& text) const override {
        std::vector<std::string> tokens;
        std::istringstream stream(text);
        std::string token;
        while (stream >> token) {
            tokens.push_back(token);
        }
        return tokens;
    }
};

class RegexTokenizer : public Tokenizer {
private:
    std::regex pattern;

public:
    RegexTokenizer(const std::string& regex_pattern) 
        : pattern(regex_pattern) {}

    std::vector<std::string> tokenize(const std::string& text) const override {
        std::vector<std::string> tokens;
        std::sregex_token_iterator iter(text.begin(), text.end(), pattern, -1);
        std::sregex_token_iterator end;

        for (; iter != end; ++iter) {
            if (!iter->str().empty()) {
                tokens.push_back(*iter);
            }
        }
        return tokens;
    }
};

#endif // TOKENIZER_H
