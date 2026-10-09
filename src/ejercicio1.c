/* Ejercicio 1: tres ciclos anidados, el último con k = k*2.
 * Complejidad esperada: Theta(n^2 log n). */
#include <math.h>
#include "bench.h"

static volatile long counter; /* volatile: evita que el compilador elimine los ciclos */

static void function(int n) {
    int i, j, k;
    counter = 0;
    for (i = n / 2; i <= n; i++) {
        for (j = 1; j + n / 2 <= n; j++) {
            for (k = 1; k <= n; k = k * 2) {
                counter++;
            }
        }
    }
}

/* Iteraciones exactas: (n - n/2 + 1) valores de i, (n - n/2) de j y
 * (floor(log2 n) + 1) de k. */
static double operaciones(long n) {
    double vi = (double)(n - n / 2 + 1);
    double vj = (double)(n - n / 2);
    double vk = floor(log2((double)n)) + 1.0;
    return vi * vj * vk;
}

int main(int argc, char **argv) {
    function(100);
    fprintf(stderr, "verificacion n=100: counter=%ld, esperado=%.0f\n", counter, operaciones(100));
    correr(function, operaciones, argc, argv);
    return 0;
}
