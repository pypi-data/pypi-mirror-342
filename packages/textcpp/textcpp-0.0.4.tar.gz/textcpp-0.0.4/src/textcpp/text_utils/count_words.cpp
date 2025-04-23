#include "operations.h"
#include <iostream>
#include <sstream>
#include <fstream>

using namespace std;

int count_words(string path) {
    ifstream MyReadFile(path);
    if (!MyReadFile) {
        cerr << "Error opening file: " << path << endl;
        return -1;  // error indicator
    }

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