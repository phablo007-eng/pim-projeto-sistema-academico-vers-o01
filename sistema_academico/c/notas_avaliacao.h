#ifndef NOTAS_AVALIACAO_H
#define NOTAS_AVALIACAO_H

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
    int status_code; /* 1=aprovado, 0=reprovado */
} ResultadoNota;

/*
 * Calcula a média entre p1 e p2, compara com threshold e define status_code.
 * Retorna 1 no sucesso; 0 se ponteiro out nulo.
 */
CAPI int compute_final_grade(double p1, double p2, double threshold, ResultadoNota* out);

#ifdef __cplusplus
}
#endif

#endif /* NOTAS_AVALIACAO_H */
