VENV := .venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

.PHONY: help install install-dev check-csv generar generar-por-pais test clean

help:
	@echo "Targets disponibles:"
	@echo "  make install            - crea el entorno virtual e instala dependencias"
	@echo "  make install-dev        - instala ademas las dependencias de desarrollo (pytest)"
	@echo "  make generar CSV=<ruta>          - genera el .xls de envios internacionales (fichero unico)"
	@echo "  make generar-por-pais CSV=<ruta> - genera un .xls por pais de envio"
	@echo "  make test               - ejecuta la suite de tests con pytest"
	@echo "  make clean              - borra el entorno virtual y los __pycache__"

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip -q
	$(PIP) install -r requirements.txt -q
	touch $(VENV)/bin/activate

install: $(VENV)/bin/activate

$(VENV)/.dev-installed: requirements-dev.txt $(VENV)/bin/activate
	$(PIP) install -r requirements-dev.txt -q
	touch $(VENV)/.dev-installed

install-dev: $(VENV)/.dev-installed

check-csv:
	@test -n "$(CSV)" || { echo "Error: indica el CSV de pedidos, p. ej. make $(MAKECMDGOALS) CSV=data/orders-square.csv"; exit 1; }

generar: install check-csv
	$(PYTHON) scripts/generar_formato_unico.py "$(CSV)"

generar-por-pais: install check-csv
	$(PYTHON) scripts/generar_formato_unico.py "$(CSV)" --agrupar-por-pais

test: install-dev
	$(PYTHON) -m pytest

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
