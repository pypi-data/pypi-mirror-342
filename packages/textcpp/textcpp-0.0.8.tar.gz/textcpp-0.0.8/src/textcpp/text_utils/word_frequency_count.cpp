#include "operations.h"
#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <algorithm>

using namespace std;

int word_frequency_count(const string& path, string word) {
    ifstream MyReadFile(path);
    if (!MyReadFile) {
        cerr << "Error opening file: " << path << endl;
        return -1;  // Indicate error
    }

    // Normalize the target word to lowercase
    transform(word.begin(), word.end(), word.begin(), ::tolower);

    string line, current_word;
    int count = 0;

    while (getline(MyReadFile, line)) {
        stringstream ss(line);
        while (ss >> current_word) {
            // Normalize current word
            transform(current_word.begin(), current_word.end(), current_word.begin(), ::tolower);

            // Remove punctuation from current_word
            current_word.erase(remove_if(current_word.begin(), current_word.end(), ::ispunct), current_word.end());

            if (current_word == word) {
                count++;
            }
        }
    }

    MyReadFile.close();
    return count;
}
