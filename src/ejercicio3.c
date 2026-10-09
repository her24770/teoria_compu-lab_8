/* Ejercicio 3: ciclo externo hasta n/3 y ciclo interno con paso 4.
 * Complejidad esperada: Theta(n^2).
 * El printf("Sequence\n") se reemplaza por un contador volatile para que el
 * tiempo medido sea el del algoritmo y no el de la entrada/salida. */
#include "bench.h"

static volatile long secuencias;

static void function(int n) {
    int i, j;
    secuencias = 0;
    for (i = 1; i <= n / 3; i++) {
        for (j = 1; j <= n; j += 4) {
            secuencias++; /* printf("Sequence\n"); */
        }
    }
}

/* floor(n/3) valores de i y ceil(n/4) = (n+3)/4 valores de j. */
static double operaciones(long n) {
    return (double)(n / 3) * (double)((n + 3) / 4);
}

int main(int argc, char **argv) {
    function(100);
    fprintf(stderr, "verificacion n=100: secuencias=%ld, esperado=%.0f\n", secuencias, operaciones(100));
    correr(function, operaciones, argc, argv);
    return 0;
}
