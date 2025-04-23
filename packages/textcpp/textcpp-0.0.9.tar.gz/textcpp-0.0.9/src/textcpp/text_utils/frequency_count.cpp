#include "operations.h"
#include <iostream>
#include <sstream>
#include <fstream>
#include <unordered_map>
#include <string>

using namespace std;

unordered_map<string, int> frequency_count(const string& path) {
    ifstream MyReadFile(path);
    unordered_map<string, int> word_freq;

    if (!MyReadFile) {
        cerr << "Error opening file: " << path << endl;
        return word_freq;  // Return empty map on error
    }

    string line, word;

    while (getline(MyReadFile, line)) {
        stringstream ss(line);
        while (ss >> word) {
            ++word_freq[word];
        }
    }

    MyReadFile.close();
    return word_freq;
}
