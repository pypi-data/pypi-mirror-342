#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "wadas_runtime/model.h"

using namespace wadas_runtime;

PYBIND11_MODULE(_core, m) {
    m.doc() = "Wadas Runtime Core Module";

    m.def("load_and_compile_model", &load_and_compile_model, "Compile Encrypted Model", py::arg("model_xml_path"),
          py::arg("model_bin_path") = py::str(), py::arg("device_name") = py::str("AUTO"),
          py::arg("config") = py::dict());
}