/* Ejercicio 2: el break corta el ciclo interno en su primera iteración.
 * Complejidad esperada: Theta(n).
 * El printf("Sequence\n") se reemplaza por un contador volatile para que el
 * tiempo medido sea el del algoritmo y no el de la entrada/salida. */
#include "bench.h"

static volatile long secuencias;

static void function(int n) {
    secuencias = 0;
    if (n <= 1) return;
    int i, j;
    for (i = 1; i <= n; i++) {
        for (j = 1; j <= n; j++) {
            secuencias++; /* printf("Sequence\n"); */
            break;
        }
    }
}

/* Una impresión por cada i en 1..n (si n > 1). */
static double operaciones(long n) {
    return n <= 1 ? 0.0 : (double)n;
}

int main(int argc, char **argv) {
    function(100);
    fprintf(stderr, "verificacion n=100: secuencias=%ld, esperado=%.0f\n", secuencias, operaciones(100));
    correr(function, operaciones, argc, argv);
    return 0;
}
