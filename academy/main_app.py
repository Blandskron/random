from __future__ import annotations

from academy.config import (
    INPUT_DIR,
    OUTPUT_DIR,
    USERS_CSV,
    QUESTIONS_CSV,
    CHOICES_CSV,
)
from academy.common.utils import ensure_dirs
from academy.infrastructure.storage.csv_users_repo import load_users
from academy.infrastructure.storage.csv_quiz_repo import load_questions
from academy.application.auth_service import login
from academy.application.quiz_service import run_quiz
from academy.application.report_service import export_results_and_report

from academy.application.ai_service import generate_quiz_with_ai


def _ask_int(prompt: str, default: int) -> int:
    raw = input(prompt).strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def run() -> None:
    # Directorios (estables, basados en BASE_DIR + DATA_INPUT/DATA_OUTPUT)
    ensure_dirs(INPUT_DIR, OUTPUT_DIR)

    # Cargar data (CSV)
    users = load_users(str(USERS_CSV))
    questions, choices = load_questions(str(QUESTIONS_CSV), str(CHOICES_CSV))

    # Login
    user = login(users)
    print(f"\n✅ Bienvenido {user.full_name}")

    # Menú principal
    while True:
        print("\n--- ACADEMIA XP ---")
        print("1. Hacer quiz (CSV)")
        print("2. Exportar resultados + reporte")
        print("3. Hacer quiz con IA (OpenAI)")
        print("4. Salir")

        opt = input("> ").strip()

        try:
            if opt == "1":
                run_quiz(user, questions, choices)

            elif opt == "2":
                export_results_and_report(users)
                print("✅ results.csv y report.txt generados en data/output/")

            elif opt == "3":
                topic = input("Tema del quiz (ej: Python, redes, UX): ").strip() or "Python"
                difficulty = input("Dificultad (facil/media/dificil): ").strip() or "media"
                n = _ask_int("Cantidad de preguntas (default 5): ", 5)

                ai_questions, ai_choices = generate_quiz_with_ai(
                    topic=topic,
                    difficulty=difficulty,
                    n_questions=n,
                    points_per_question=10,
                )
                print("\n🤖 Quiz generado. ¡Comencemos!")
                run_quiz(user, ai_questions, ai_choices)

            elif opt == "4":
                print("👋 Saliendo...")
                break

            else:
                print("❌ Opción inválida")

        except Exception as e:
            print(f"❌ Error: {e}")
