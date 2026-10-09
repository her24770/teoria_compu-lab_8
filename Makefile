CC      ?= cc
CFLAGS  ?= -O0 -Wall -Wextra
BIN     = bin
BUDGET ?= 20

EJ = ejercicio1 ejercicio2 ejercicio3

all: $(EJ:%=$(BIN)/%)

$(BIN)/%: src/%.c src/bench.h | $(BIN)
	$(CC) $(CFLAGS) $< -o $@ -lm

$(BIN):
	mkdir -p $(BIN)

# Corre los tres programas y deja un CSV por ejercicio en resultados/
resultados: all
	mkdir -p resultados
	for e in $(EJ); do $(BIN)/$$e $(BUDGET) > resultados/$$e.csv; done

clean:
	rm -rf $(BIN)
