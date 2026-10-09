/* Utilidades de profiling compartidas por los ejercicios 1, 2 y 3.
 *
 * Método: se mide con un reloj monotónico (clock_gettime). Para tamaños
 * pequeños, donde una sola ejecución dura nanosegundos, se repite la función
 * hasta acumular al menos MIN_TOTAL segundos y se promedia por ejecución.
 *
 * Para tamaños cuya ejecución estimada supera el presupuesto de tiempo
 * (argumento 1, en segundos), no se ejecuta: el tiempo se estima como
 * (operaciones del modelo) x (ns/operación medidos en el último tamaño real)
 * y la fila se marca con medido = 0.
 */
#ifndef BENCH_H
#define BENCH_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MIN_TOTAL 0.05

static const long TAMANOS[] = {1, 10, 100, 1000, 10000, 100000, 1000000};
#define N_TAMANOS (sizeof(TAMANOS) / sizeof(TAMANOS[0]))

static double ahora(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

/* Corre la función bajo prueba para todos los tamaños e imprime un CSV:
 *   n,operaciones,segundos,medido
 * `funcion` es el programa del enunciado; `operaciones` es el conteo exacto
 * de iteraciones del ciclo más interno según el modelo teórico. */
static void correr(void (*funcion)(int), double (*operaciones)(long), int argc, char **argv) {
    double presupuesto = (argc > 1) ? atof(argv[1]) : 20.0;
    double ns_por_op = 0.0;

    printf("n,operaciones,segundos,medido\n");
    for (size_t t = 0; t < N_TAMANOS; t++) {
        long n = TAMANOS[t];
        double ops = operaciones(n);
        double estimado = ns_por_op * 1e-9 * ops;

        if (ns_por_op > 0.0 && estimado > presupuesto) {
            printf("%ld,%.0f,%.9f,0\n", n, ops, estimado);
            continue;
        }

        long reps = 0;
        double inicio = ahora(), total;
        do {
            funcion((int)n);
            reps++;
            total = ahora() - inicio;
        } while (total < MIN_TOTAL);

        double segundos = total / reps;
        if (ops > 0) ns_por_op = segundos * 1e9 / ops;
        printf("%ld,%.0f,%.9f,1\n", n, ops, segundos);
        fflush(stdout);
    }
}

#endif
