#include "operations.h"
#include <iostream>
#include <sstream>
#include <fstream>

using namespace std;

int count_words(const string& input) {
    ifstream MyReadFile(input);

    if (MyReadFile) {
        // Input is a valid file path
        string line, word;
        int word_count = 0;

        while (getline(MyReadFile, line)) {
            stringstream ss(line);
            while (ss >> word) {
                word_count++;
            }
        }

        MyReadFile.close();
        return word_count;
    } else {
        // Input is not a file, treat as raw string
        stringstream ss(input);
        string word;
        int word_count = 0;

        while (ss >> word) {
            word_count++;
        }

        return word_count;
    }
}



// g++ src/mypackage/count_words.cpp -o test/count_words_test
// ./test/count_words_test

//int main() {
//    string test_file = "test/shakespeare.txt";
//    int words = count_words(test_file);
//
//    if (words >= 0) {
// cout << "Total words in file \"" << test_file << "\": " << words << endl;
//    } else {
//        cout << "Error reading file." << endl;
//    }
//
//    return 0;
//}