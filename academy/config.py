from __future__ import annotations

import os
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


def _load_env_file_if_exists() -> None:
    """
    Loader .env minimalista (sin dependencia).
    Lee BASE_DIR/.env si existe.
    Soporta líneas:
      KEY=VALUE
      KEY="VALUE"
      KEY='VALUE'
    Ignora comentarios y líneas vacías.
    """
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        return

    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip("'").strip('"')
            # No sobreescribir si ya está definido en el entorno
            os.environ.setdefault(k, v)
    except Exception:
        # Si el .env está malo, no rompemos el programa
        return


_load_env_file_if_exists()

# --- OpenAI (env) ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# Por defecto usa GPT-5.2 (puedes cambiarlo en .env sin tocar código)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2").strip()

def _to_float(value: str, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default

def _to_int(value: str, default: int) -> int:
    try:
        return int(value)
    except Exception:
        return default

OPENAI_TEMPERATURE = _to_float(os.getenv("OPENAI_TEMPERATURE", "0.4"), 0.4)
OPENAI_MAX_OUTPUT_TOKENS = _to_int(os.getenv("OPENAI_MAX_OUTPUT_TOKENS", "800"), 800)
OPENAI_TIMEOUT_SECONDS = _to_int(os.getenv("OPENAI_TIMEOUT_SECONDS", "60"), 60)
