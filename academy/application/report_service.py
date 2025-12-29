from __future__ import annotations

import csv
from typing import Dict, List, Tuple

from academy.config import DATA_OUTPUT
from academy.infrastructure.storage.csv_results_repo import write_results
from academy.infrastructure.storage.txt_report_writer import write_report_txt


def _compute_quiz_totals_from_answers(answers_path: str) -> Dict[str, int]:
    totals: Dict[str, int] = {}

    try:
        with open(answers_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                # Formato esperado: user_id, question_id, choice_id, earned_points
                if len(row) != 4:
                    # Si hay filas corruptas, se ignoran (o puedes levantar ValueError)
                    continue
                user_id, _, _, pts = row
                totals[user_id] = totals.get(user_id, 0) + int(pts)
    except FileNotFoundError:
        # Si no hay respuestas aún, totales vacíos.
        return {}

    return totals


def export_results_and_report(users: Dict[str, object]) -> None:
    """
    users: dict por email -> User (como está en tu repo actual).
    Exporta:
      - data/output/results.csv
      - data/output/report.txt
    """
    answers_path = f"{DATA_OUTPUT}/answers.csv"
    results_path = f"{DATA_OUTPUT}/results.csv"
    report_path = f"{DATA_OUTPUT}/report.txt"

    totals = _compute_quiz_totals_from_answers(answers_path)

    # Mapa user_id -> full_name
    user_names: Dict[str, str] = {u.id: u.full_name for u in users.values()}

    # results.csv
    write_results(results_path, totals, user_names)

    # ranking para el TXT
    ranking_ids: List[Tuple[str, int]] = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    ranking_named: List[Tuple[str, int]] = [(user_names.get(uid, "Unknown"), pts) for uid, pts in ranking_ids]

    inactive_users = [u.full_name for u in users.values() if not u.is_active]

    # report.txt
    write_report_txt(report_path, ranking_named, inactive_users, top_n=3)
