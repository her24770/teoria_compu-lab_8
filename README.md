# Laboratorio No. 8 — Análisis de complejidad

Teoría de la Computación — Universidad del Valle de Guatemala.

## Video de demostración

> TODO: pegar aquí el enlace del video (YouTube, no listado, máximo 10 minutos).

## Estructura

```
.
├── src/                      Programas en C (ejercicios 1, 2 y 3)
│   ├── bench.h               Utilidades de profiling compartidas
│   ├── ejercicio1.c          O(n² log n)
│   ├── ejercicio2.c          O(n)
│   └── ejercicio3.c          O(n²)
├── scripts/
│   ├── graficar.py           CSV -> gráficas (PNG) y tablas (Markdown)
│   ├── ejercicio5c.py        Verificación empírica del ejercicio 5c
│   └── generar_pdf.py        Genera el PDF de respuestas
├── resultados/               CSV, gráficas y tablas de las mediciones
├── respuestas/
│   └── Laboratorio_8_Respuestas.pdf   Procedimientos y respuestas (a, b, 4 y 5)
├── Makefile
└── requirements.txt
```

## Resumen de resultados

| Ejercicio | Complejidad |
|-----------|-------------|
| 1 | Θ(n² log n) |
| 2 | Θ(n) |
| 3 | Θ(n²) |
| 4 | Mejor Θ(1), promedio Θ(n), peor Θ(n) |
| 5 | a) Verdadero, b) Verdadero, c) Falso (A(n) = Θ(n³)) |

El desarrollo completo está en `respuestas/Laboratorio_8_Respuestas.pdf`.

## Requisitos

- Compilador de C (`cc`/`gcc`/`clang`) y `make`.
- Python 3 con las dependencias de `requirements.txt` (solo para gráficas y PDF).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Cómo ejecutar

```bash
# 1. Compilar los tres programas (quedan en bin/)
make

# 2. Correr el profiling y guardar los CSV en resultados/
make resultados            # presupuesto por defecto: 20 s por medición
make resultados BUDGET=60  # o uno distinto

# 3. Generar gráficas y tablas
python3 scripts/graficar.py

# 4. Verificar el ejercicio 5c y regenerar el PDF
python3 scripts/ejercicio5c.py | tee resultados/ejercicio5c.txt
python3 scripts/generar_pdf.py
```

También se puede correr un ejercicio por separado: `./bin/ejercicio1 60`
(el argumento es el presupuesto de tiempo por medición, en segundos).

## Método de profiling

- Reloj monotónico `clock_gettime(CLOCK_MONOTONIC)`, compilado con `-O0`.
- Para tamaños pequeños la función se repite hasta acumular 50 ms y se promedia.
- El `printf("Sequence\n")` de los ejercicios 2 y 3 se sustituye por un contador
  `volatile`, para medir el algoritmo y no la entrada/salida (con n = 10⁶ el
  ejercicio 3 imprimiría ~8×10¹⁰ líneas).
- Cada programa verifica por stderr que su contador coincide con la fórmula
  exacta de iteraciones (n = 100).
- **Valores estimados:** si el tiempo de un tamaño supera el presupuesto, no se
  ejecuta; se estima como (operaciones exactas) × (ns/operación del último
  tamaño medido) y la fila queda marcada con `medido = 0` / «estimado». En la
  corrida incluida solo el ejercicio 1 con n = 1,000,000 (~5×10¹² iteraciones,
  ≈ 49 min) se estimó; todo lo demás se midió.
