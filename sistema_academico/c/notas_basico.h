#ifndef NOTAS_BASICO_H
#define NOTAS_BASICO_H

#include <stddef.h>

#ifdef _WIN32
  #define CAPI __declspec(dllexport)
#else
  #define CAPI
#endif

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    double media;
    double minimo;
    double maximo;
} StatsBasico;

/*
 * Calcula média, mínimo e máximo de um vetor de doubles.
 * Retorna 1 (sucesso) ou 0 (erro: n==0 ou ponteiros nulos).
 */
CAPI int compute_basic_stats(const double* valores, size_t n, StatsBasico* out);

#ifdef __cplusplus
}
#endif

#endif /* NOTAS_BASICO_H */
