"""Genera respuestas/Laboratorio_8_Respuestas.pdf con los procedimientos
(incisos a), los resultados (incisos b) y los ejercicios 4 y 5."""
import csv
from pathlib import Path

import matplotlib
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, PageBreak, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

RAIZ = Path(__file__).resolve().parent.parent
RES = RAIZ / "resultados"
SALIDA = RAIZ / "respuestas" / "Laboratorio_8_Respuestas.pdf"

fuentes = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
pdfmetrics.registerFont(TTFont("DV", str(fuentes / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DV-B", str(fuentes / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DV-M", str(fuentes / "DejaVuSansMono.ttf")))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV", boldItalic="DV-B")

base = getSampleStyleSheet()
CUERPO = ParagraphStyle("c", parent=base["BodyText"], fontName="DV", fontSize=9.5, leading=14)
H1 = ParagraphStyle("h1", parent=CUERPO, fontName="DV-B", fontSize=14, leading=18, spaceBefore=6, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=CUERPO, fontName="DV-B", fontSize=11, leading=15, spaceBefore=8, spaceAfter=3)
TITULO = ParagraphStyle("t", parent=H1, fontSize=17, leading=22, alignment=1)
CENTRO = ParagraphStyle("ce", parent=CUERPO, alignment=1)
CODIGO = ParagraphStyle("cod", parent=CUERPO, fontName="DV-M", fontSize=8.5, leading=11,
                        backColor=colors.HexColor("#F3F3F3"), borderPadding=5, spaceBefore=4, spaceAfter=8)

historia = []


def p(texto, estilo=CUERPO):
    historia.append(Paragraph(texto, estilo))


def codigo(texto):
    historia.append(Preformatted(texto.strip("\n"), CODIGO))


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


def tabla_resultados(ej):
    filas = [["n", "Operaciones", "Tiempo", "Origen"]]
    with open(RES / f"ejercicio{ej}.csv") as f:
        for r in csv.DictReader(f):
            filas.append([f"{int(r['n']):,}", f"{float(r['operaciones']):,.0f}",
                          formato_tiempo(float(r["segundos"])),
                          "medido" if r["medido"] == "1" else "estimado"])
    t = Table(filas, colWidths=[3 * cm, 5 * cm, 3.5 * cm, 3 * cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, 0), "DV-B", 9), ("FONT", (0, 1), (-1, -1), "DV", 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F1")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("ALIGN", (0, 0), (2, -1), "RIGHT"),
    ]))
    historia.append(t)
    historia.append(Spacer(1, 6))
    historia.append(Image(str(RES / f"ejercicio{ej}.png"), width=17 * cm, height=17 * cm * 4.2 / 11))


NOTA_PROFILING = (
    "<b>Método de profiling:</b> reloj monotónico <font name='DV-M'>clock_gettime(CLOCK_MONOTONIC)</font> en C "
    "(compilado con <font name='DV-M'>-O0</font>). Para tamaños pequeños la función se repite hasta acumular "
    "50 ms y se promedia. El <font name='DV-M'>printf</font> se sustituyó por un contador "
    "<font name='DV-M'>volatile</font> para medir el algoritmo y no la entrada/salida. Los contadores se "
    "verificaron contra las fórmulas exactas de iteraciones."
)

# ---------------------------------------------------------------- portada
p("Universidad del Valle de Guatemala<br/>Facultad de Ingeniería", CENTRO)
p("Laboratorio No. 8 — Respuestas", TITULO)
p("Teoría de la Computación — Análisis de complejidad", CENTRO)
historia.append(Spacer(1, 10))

# ---------------------------------------------------------------- ejercicio 1
p("Ejercicio No. 1", H1)
codigo("""
void function (int n) {
    int i, j, k, counter = 0;
    for (i = n/2; i <= n; i++) {
        for (j = 1; j+n/2 <= n; j++) {
            for (k = 1; k <= n; k = k*2) {
                counter++;
            }
        }
    }
}""")
p("a) Complejidad de tiempo", H2)
p("Se analiza cada ciclo de afuera hacia adentro:")
p("• <b>Ciclo i:</b> va de n/2 a n con paso 1, así que ejecuta n − n/2 + 1 = n/2 + 1 iteraciones → Θ(n).")
p("• <b>Ciclo j:</b> la condición j + n/2 ≤ n equivale a j ≤ n/2, y j parte de 1, así que ejecuta n/2 "
  "iteraciones → Θ(n).")
p("• <b>Ciclo k:</b> k se duplica en cada paso (1, 2, 4, 8, …). Tras m iteraciones vale 2<super>m</super>; el "
  "ciclo termina cuando 2<super>m</super> &gt; n, es decir, m = ⌊log<sub>2</sub> n⌋ + 1 iteraciones → Θ(log n).")
p("Los ciclos son independientes (ninguna cota depende de la variable de otro ciclo), por lo que el trabajo se "
  "multiplica:")
p("T(n) = (n/2 + 1) · (n/2) · (⌊log<sub>2</sub> n⌋ + 1) = (n²/4 + n/2) · (⌊log<sub>2</sub> n⌋ + 1)")
p("El término dominante es (n²/4) · log n; se descartan constantes y términos de menor orden:")
p("<b>T(n) = O(n² log n)</b>, y de hecho Θ(n² log n), porque la expresión también está acotada por debajo.")
p("b) Profiling", H2)
p(NOTA_PROFILING)
p("<b>Nota:</b> con n = 1,000,000 el programa realiza ≈ 5×10<super>12</super> iteraciones (unos 49 minutos). "
  "Esa fila se <b>estimó</b> como (operaciones exactas) × (ns por operación medidos en n = 100,000) en lugar de "
  "ejecutarla; está marcada como «estimado» en la tabla y con un cuadro vacío en la gráfica.")
tabla_resultados(1)
p("<b>Análisis:</b> en escala log-log la curva tiene pendiente ≈ 2 con una ligera curvatura hacia arriba, lo "
  "esperado para n² log n. Cada vez que n se multiplica por 10, el tiempo se multiplica por ≈ 120–140 "
  "(algo más de 100 por el factor log n), consistente con n² · log n.")
historia.append(PageBreak())

# ---------------------------------------------------------------- ejercicio 2
p("Ejercicio No. 2", H1)
codigo("""
void function (int n) {
    if (n <= 1) return;
    int i, j;
    for (i = 1; i <= n; i++) {
        for (j = 1; j <= n; j++) {
            printf ("Sequence\\n");
            break;
        }
    }
}""")
p("a) Complejidad de tiempo", H2)
p("• La instrucción <font name='DV-M'>if (n &lt;= 1) return;</font> es O(1).")
p("• <b>Ciclo i:</b> ejecuta n iteraciones → Θ(n).")
p("• <b>Ciclo j:</b> aunque su condición permitiría n iteraciones, el <font name='DV-M'>break</font> lo "
  "interrumpe al final de la <b>primera</b> iteración. Hace exactamente 1 iteración (un printf y el break), "
  "es decir, O(1).")
p("Como el ciclo interno cuesta O(1) por cada valor de i:")
p("T(n) = Σ<sub>i=1</sub><super>n</super> O(1) = n · c")
p("<b>T(n) = O(n)</b> (y Θ(n) para n &gt; 1). Es lineal y no cuadrático, pese a haber dos ciclos anidados.")
p("b) Profiling", H2)
p(NOTA_PROFILING)
tabla_resultados(2)
p("<b>Análisis:</b> el tiempo crece ≈ 10 veces por cada 10 veces que crece n: comportamiento lineal. Para "
  "n = 1 no hay trabajo (retorna de inmediato); el tiempo medido en esa fila es solo el costo de la llamada y "
  "del reloj.")
historia.append(PageBreak())

# ---------------------------------------------------------------- ejercicio 3
p("Ejercicio No. 3", H1)
codigo("""
void function (int n) {
    int i, j;
    for (i=1; i<=n/3; i++) {
        for (j=1; j<=n; j+=4) {
            printf("Sequence\\n");
        }
    }
}""")
p("a) Complejidad de tiempo", H2)
p("• <b>Ciclo i:</b> va de 1 a n/3 con paso 1 → ⌊n/3⌋ iteraciones.")
p("• <b>Ciclo j:</b> va de 1 a n con paso 4 (j = 1, 5, 9, …) → ⌈n/4⌉ iteraciones.")
p("Las cotas son independientes, así que se multiplican:")
p("T(n) = ⌊n/3⌋ · ⌈n/4⌉ ≈ (n/3) · (n/4) = n²/12")
p("Se descarta la constante 1/12: <b>T(n) = O(n²)</b> (y Θ(n²)).")
p("b) Profiling", H2)
p(NOTA_PROFILING)
tabla_resultados(3)
p("<b>Análisis:</b> cada vez que n se multiplica por 10, el tiempo se multiplica por ≈ 100, como corresponde a "
  "un comportamiento cuadrático (pendiente 2 en escala log-log).")
historia.append(PageBreak())

# ---------------------------------------------------------------- ejercicio 4
p("Ejercicio No. 4 — Búsqueda Lineal", H1)
codigo("""
LinearSearch(A, n, x):
    for i = 0 to n-1:
        if A[i] == x:
            return i
    return -1""")
p("Se cuenta el número de comparaciones <font name='DV-M'>A[i] == x</font> como operación dominante. "
  "Cada comparación es O(1).")
p("Mejor caso", H2)
p("El elemento buscado está en la primera posición (A[0] = x). Se hace 1 sola comparación: "
  "T(n) = 1 → <b>Θ(1)</b> (O(1)).")
p("Peor caso", H2)
p("El elemento está en la última posición o no está en el arreglo. Se comparan los n elementos: "
  "T(n) = n → <b>Θ(n)</b> (O(n)).")
p("Caso promedio", H2)
p("Se asume que x está en el arreglo y que su posición es equiprobable: la probabilidad de que esté en la "
  "posición k (k = 1, …, n) es 1/n, y encontrarlo en esa posición cuesta k comparaciones. Entonces:")
p("T<sub>prom</sub>(n) = Σ<sub>k=1</sub><super>n</super> k · (1/n) = (1/n) · n(n+1)/2 = (n+1)/2")
p("Es decir, ≈ n/2 comparaciones: <b>Θ(n)</b>.")
p("Si además se considera que x puede no estar con probabilidad q (costo n), el promedio es "
  "(1−q)(n+1)/2 + q·n, que sigue siendo lineal en n. Por lo tanto el caso promedio también es Θ(n).")
p("<b>Resumen:</b> mejor caso Θ(1), caso promedio Θ(n), peor caso Θ(n).")

# ---------------------------------------------------------------- ejercicio 5
p("Ejercicio No. 5", H1)
p("a) Si f(n) = Θ(g(n)) y g(n) = Θ(h(n)), entonces h(n) = Θ(f(n)). — VERDADERO", H2)
p("Θ es una relación de equivalencia (reflexiva, simétrica y transitiva). Por definición, f = Θ(g) significa "
  "que existen c<sub>1</sub>, c<sub>2</sub> &gt; 0 y n<sub>0</sub> tales que "
  "c<sub>1</sub>g(n) ≤ f(n) ≤ c<sub>2</sub>g(n) para n ≥ n<sub>0</sub>; análogamente "
  "d<sub>1</sub>h(n) ≤ g(n) ≤ d<sub>2</sub>h(n) para n ≥ n<sub>1</sub>.")
p("Combinando, para n ≥ máx(n<sub>0</sub>, n<sub>1</sub>): "
  "c<sub>1</sub>d<sub>1</sub>·h(n) ≤ f(n) ≤ c<sub>2</sub>d<sub>2</sub>·h(n), luego f = Θ(h) (transitividad). "
  "Despejando, (1/(c<sub>2</sub>d<sub>2</sub>))·f(n) ≤ h(n) ≤ (1/(c<sub>1</sub>d<sub>1</sub>))·f(n), "
  "así que h = Θ(f) (simetría).")
p("b) Si f(n) = O(g(n)) y g(n) = O(h(n)), entonces h(n) = Ω(f(n)). — VERDADERO", H2)
p("Por definición, f = O(g) significa f(n) ≤ c·g(n) para n ≥ n<sub>0</sub>, y g = O(h) significa "
  "g(n) ≤ d·h(n) para n ≥ n<sub>1</sub>. Entonces, para n ≥ máx(n<sub>0</sub>, n<sub>1</sub>): "
  "f(n) ≤ c·d·h(n), o sea f = O(h) (transitividad de O).")
p("Además, h = Ω(f) significa exactamente que existe una constante positiva e tal que h(n) ≥ e·f(n) "
  "para n grande. Tomando e = 1/(c·d) se obtiene h(n) ≥ f(n)/(c·d). Por lo tanto h(n) = Ω(f(n)).")
p("c) f(n) = Θ(n²), con f(n) el tiempo de ejecución de A(n). — FALSO", H2)
codigo("""
def A(n):
    atupla = tuple(range(0, n))
    S = set()
    for i in range(0, n):
        for j in range(i + 1, n):
            S.add(atupla[i:j])""")
p("El error es suponer que cada iteración del ciclo interno cuesta O(1). Hay n(n−1)/2 pares (i, j), pero en "
  "cada uno se hacen dos operaciones cuyo costo depende del tamaño de la rebanada:")
p("• <font name='DV-M'>atupla[i:j]</font> crea una tupla nueva copiando j − i elementos → Θ(j − i).")
p("• <font name='DV-M'>S.add(...)</font> calcula el hash de la tupla, que recorre sus j − i elementos "
  "→ Θ(j − i). Si hay colisión, la comparación de igualdad también es proporcional a su longitud.")
p("El costo total es:")
p("f(n) = Σ<sub>i=0</sub><super>n−1</super> Σ<sub>j=i+1</sub><super>n−1</super> Θ(j − i)")
p("Con d = j − i, para cada d hay n − d pares, de modo que:")
p("Σ<sub>d=1</sub><super>n−1</super> (n − d)·d = n · n(n−1)/2 − (n−1)n(2n−1)/6 = (n³ − n)/6 = Θ(n³)")
p("Por lo tanto f(n) = Θ(n³), y como n³ crece estrictamente más rápido que n², <b>f(n) ≠ Θ(n²)</b>. "
  "El enunciado es falso.")
p("<b>Verificación empírica</b> (<font name='DV-M'>scripts/ejercicio5c.py</font>): el trabajo contado "
  "coincide con (n³ − n)/6 (p. ej. n = 800 → 85,333,200) y la razón tiempo/n³ se estabiliza en ≈ 1.45×10"
  "<super>−9</super>, mientras que tiempo/n² crece sin parar (de 1.1×10<super>−7</super> a "
  "1.2×10<super>−6</super>).")
filas = [["n", "tiempo (s)", "trabajo", "t / n²", "t / n³"]]
for linea in (RES / "ejercicio5c.txt").read_text().splitlines()[1:]:
    filas.append(linea.split())
t = Table(filas, colWidths=[2 * cm, 3 * cm, 3.5 * cm, 3 * cm, 3 * cm])
t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "DV-B", 9), ("FONT", (0, 1), (-1, -1), "DV", 9),
                       ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F1")),
                       ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("ALIGN", (0, 0), (-1, -1), "RIGHT")]))
historia.append(t)

SALIDA.parent.mkdir(exist_ok=True)
SimpleDocTemplate(str(SALIDA), pagesize=letter, leftMargin=2 * cm, rightMargin=2 * cm,
                  topMargin=2 * cm, bottomMargin=2 * cm,
                  title="Laboratorio No. 8 — Respuestas").build(historia)
print("PDF generado en", SALIDA)
