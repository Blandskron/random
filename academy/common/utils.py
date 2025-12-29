from __future__ import annotations
from pathlib import Path

def ensure_dirs(*dirs: Path) -> None:
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

def ask_int(prompt: str) -> int:
    try:
        return int(input(prompt))
    except ValueError:
        raise ValueError("Debe ingresar un número")