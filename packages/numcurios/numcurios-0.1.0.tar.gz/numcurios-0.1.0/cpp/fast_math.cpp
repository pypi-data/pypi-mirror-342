#include <pybind11/pybind11.h>

bool is_prime(int n) {
    if (n <= 1) return false;
    for (int i = 2; i * i <= n; ++i) {
        if (n % i == 0) return false;
    }
    return true;
}

namespace py = pybind11;

PYBIND11_MODULE(fast_math, m) {
    m.doc() = "Быстрые числовые функции на C++ через pybind11";
    m.def("is_prime", &is_prime, "Проверка на простое число");
}
