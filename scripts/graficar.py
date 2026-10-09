"""Lee resultados/ejercicioN.csv y genera, para cada ejercicio:
 - resultados/ejercicioN.png : tamaño de input vs. tiempo (escala lineal y log-log)
 - resultados/tablas.md      : tablas de resultados en Markdown
"""
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent.parent
RES = RAIZ / "resultados"
TITULOS = {
    1: "Ejercicio 1 — O(n² log n)",
    2: "Ejercicio 2 — O(n)",
    3: "Ejercicio 3 — O(n²)",
}


def leer(ej):
    with open(RES / f"ejercicio{ej}.csv") as f:
        return [
            (int(r["n"]), float(r["operaciones"]), float(r["segundos"]), r["medido"] == "1")
            for r in csv.DictReader(f)
        ]


def formato_tiempo(s):
    if s < 1e-6:
        return f"{s * 1e9:.1f} ns"
    if s < 1e-3:
        return f"{s * 1e6:.2f} µs"
    if s < 1:
        return f"{s * 1e3:.2f} ms"
    if s < 3600:
        return f"{s:.2f} s"
    return f"{s / 3600:.2f} h"


def graficar(ej, datos):
    ns = [d[0] for d in datos]
    ts = [d[2] for d in datos]
    medidos = [d[3] for d in datos]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, log in ((ax1, False), (ax2, True)):
        ax.plot(ns, ts, "-", color="#4C72B0", lw=1.5, zorder=1)
        for n, t, m in zip(ns, ts, medidos):
            ax.plot(n, t, "o" if m else "s", color="#4C72B0" if m else "#C44E52",
                    mfc="#4C72B0" if m else "white", ms=6, zorder=2)
        ax.set_xlabel("Tamaño de input n")
        ax.set_ylabel("Tiempo (s)")
        ax.grid(alpha=0.3)
        if log:
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_title("Escala log-log")
        else:
            ax.set_title("Escala lineal")
    if not all(medidos):
        ax2.plot([], [], "s", mfc="white", color="#C44E52", label="estimado (no ejecutado)")
        ax2.plot([], [], "o", color="#4C72B0", label="medido")
        ax2.legend(loc="upper left")
    fig.suptitle(TITULOS[ej])
    fig.tight_layout()
    fig.savefig(RES / f"ejercicio{ej}.png", dpi=150)
    plt.close(fig)


def tabla(ej, datos):
    lineas = [f"### {TITULOS[ej]}", "",
              "| n | Operaciones | Tiempo | Origen |", "|---:|---:|---:|:---|"]
    for n, ops, t, m in datos:
        lineas.append(f"| {n:,} | {ops:,.0f} | {formato_tiempo(t)} | {'medido' if m else 'estimado'} |")
    return "\n".join(lineas) + "\n"


def main():
    partes = []
    for ej in (1, 2, 3):
        datos = leer(ej)
        graficar(ej, datos)
        partes.append(tabla(ej, datos))
    (RES / "tablas.md").write_text("\n".join(partes))
    print("Gráficas y tablas generadas en", RES)


if __name__ == "__main__":
    main()
