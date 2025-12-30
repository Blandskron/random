from __future__ import annotations

import csv
from typing import Dict, List

from academy.config import ANSWERS_CSV
from academy.domain.quiz.models import Question, Choice


def _safe_select_index(max_len: int) -> int:
    while True:
        raw = input("Opción: ").strip()
        try:
            n = int(raw)
        except ValueError:
            print("❌ Ingresa un número válido.")
            continue

        idx = n - 1
        if 0 <= idx < max_len:
            return idx

        print(f"❌ Opción fuera de rango. Debe ser 1..{max_len}")


def run_quiz(user, questions: Dict[str, Question], choices: Dict[str, List[Choice]]) -> None:
    total = 0
    answers_path = str(ANSWERS_CSV)

    with open(answers_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        for q in questions.values():
            print("\n" + q.text)

            opts = choices.get(q.id, [])
            if not opts:
                print("⚠️ Esta pregunta no tiene opciones. Se omite.")
                continue

            for i, c in enumerate(opts, start=1):
                print(f"{i}. {c.text}")

            selected = _safe_select_index(len(opts))
            choice = opts[selected]

            earned = q.points if choice.is_correct else 0
            total += earned

            writer.writerow([user.id, q.id, choice.id, earned])

    print(f"\nPuntaje obtenido: {total}")
