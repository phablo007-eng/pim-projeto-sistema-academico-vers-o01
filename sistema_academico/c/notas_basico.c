#include "notas_basico.h"

int compute_basic_stats(const double* valores, size_t n, StatsBasico* out) {
    if (!valores || !out || n == 0) return 0;

    double soma = 0.0;
    double min = valores[0];
    double max = valores[0];

    for (size_t i = 0; i < n; ++i) {
        double x = valores[i];
        soma += x;
        if (x < min) min = x;
        if (x > max) max = x;
    }

    out->media = soma / (double)n;
    out->minimo = min;
    out->maximo = max;
    return 1;
}
