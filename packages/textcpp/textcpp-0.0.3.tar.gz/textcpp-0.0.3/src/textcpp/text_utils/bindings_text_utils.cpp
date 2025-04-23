#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "operations.h"

namespace py = pybind11;

PYBIND11_MODULE(text_utils, m) {
    m.doc() = "Module with multiple C++ functions";
    m.def("count_words", &count_words, "count words in text file");
    m.def("frequency_count", &frequency_count, "make frequency word count from file");
}

