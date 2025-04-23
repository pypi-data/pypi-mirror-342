#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "operations.h"

namespace py = pybind11;

PYBIND11_MODULE(preprocessing, m) {
    m.doc() = "Preprocessing";
    m.def("extract_ngrams", &extract_ngrams, "extract n-grams from text");
    }

