#include <pybind11/pybind11.h>
#include "operations.h"

namespace py = pybind11;

PYBIND11_MODULE(others, m) {
    m.doc() = "Module with multiple C++ functions";

    m.def("add", &add, "Add two numbers");
    m.def("sub", &sub, "Subtract two numbers");

}