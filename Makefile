# RPA_SMART_NEWS — tarefas locais (GNU Make).
# Requer: make + Python 3.11+ no PATH (ou defina PYTHON para o do .venv).
# Windows: Git Bash, WSL, ou make instalado (ex.: choco install make).

.PHONY: install run test

PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) main.py

test:
	$(PYTHON) -m pytest
