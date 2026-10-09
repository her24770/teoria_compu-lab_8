"""Verificación empírica del Ejercicio 5c: ¿es A(n) = Theta(n^2)?

Se cuenta el trabajo real de A(n): cada atupla[i:j] copia (j - i) elementos y
al añadirlo al set se calcula su hash, que recorre otros (j - i) elementos.
También se mide el tiempo con time.perf_counter.
"""
import time


def A(n):
    atupla = tuple(range(0, n))
    S = set()
    for i in range(0, n):
        for j in range(i + 1, n):
            S.add(atupla[i:j])
    return S


def trabajo(n):
    """Elementos copiados por todos los slices: suma de (j - i) para i < j < n."""
    return sum(j - i for i in range(n) for j in range(i + 1, n))


if __name__ == "__main__":
    print(f"{'n':>5} {'tiempo (s)':>12} {'trabajo':>12} {'t/n^2':>12} {'t/n^3':>12}")
    for n in (50, 100, 200, 400, 800):
        t0 = time.perf_counter()
        A(n)
        t = time.perf_counter() - t0
        print(f"{n:>5} {t:>12.4f} {trabajo(n):>12} {t / n**2:>12.3e} {t / n**3:>12.3e}")
