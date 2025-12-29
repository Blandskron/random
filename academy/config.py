from __future__ import annotations
from pathlib import Path

# Tus constantes (tal cual)
DATA_INPUT = "data/input"
DATA_OUTPUT = "data/output"

# Raíz del proyecto: sube 1 nivel desde academy/ hasta donde está main.py
BASE_DIR = Path(__file__).resolve().parent.parent

# Rutas absolutas estables (derivadas de tus strings)
INPUT_DIR = (BASE_DIR / DATA_INPUT).resolve()
OUTPUT_DIR = (BASE_DIR / DATA_OUTPUT).resolve()

USERS_CSV = INPUT_DIR / "users.csv"
QUESTIONS_CSV = INPUT_DIR / "questions.csv"
CHOICES_CSV = INPUT_DIR / "choices.csv"

ANSWERS_CSV = OUTPUT_DIR / "answers.csv"
RESULTS_CSV = OUTPUT_DIR / "results.csv"
REPORT_TXT = OUTPUT_DIR / "report.txt"
