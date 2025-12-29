from __future__ import annotations

import csv
from typing import Dict


def ensure_results_header(path: str) -> None:
    """
    Crea el archivo con header si no existe.
    Si existe, no lo modifica.
    """
    try:
        with open(path, "r", encoding="utf-8") as _:
            return
    except FileNotFoundError:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["user_id", "full_name", "quiz_points"])


def write_results(path: str, totals: Dict[str, int], user_names: Dict[str, str]) -> None:
    """
    Sobrescribe results.csv con los totales actuales.
    totals: {user_id: points}
    user_names: {user_id: full_name}
    """
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "full_name", "quiz_points"])

        for user_id, points in sorted(totals.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([user_id, user_names.get(user_id, "Unknown"), points])
