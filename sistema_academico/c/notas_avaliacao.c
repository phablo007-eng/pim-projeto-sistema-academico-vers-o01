#include "notas_avaliacao.h"

int compute_final_grade(double p1, double p2, double threshold, ResultadoNota* out) {
    if (!out) return 0;
    double media = (p1 + p2) / 2.0;
    out->media = media;
    out->status_code = (media >= threshold) ? 1 : 0;
    return 1;
}
