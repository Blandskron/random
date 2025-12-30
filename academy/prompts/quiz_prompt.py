from __future__ import annotations

from academy.prompts.schemas import quiz_generation_contract


def build_quiz_generation_prompt(topic: str, difficulty: str, n_questions: int, points_per_question: int) -> tuple[str, str]:
    """
    Retorna (instructions, user_input) para Responses API.
    """
    contract = quiz_generation_contract()

    instructions = (
        "Eres un generador profesional de quizzes.\n"
        "Devuelve SIEMPRE un JSON válido, sin texto extra, sin markdown.\n"
        "No incluyas explicaciones fuera del JSON.\n"
        "Reglas:\n"
        "- Cada pregunta debe tener exactamente 4 opciones.\n"
        "- Exactamente 1 opción correcta por pregunta.\n"
        "- ids deben ser strings únicos.\n"
        "- points debe ser int.\n"
    )

    user_input = (
        f"Tema: {topic}\n"
        f"Dificultad: {difficulty}\n"
        f"Cantidad de preguntas: {n_questions}\n"
        f"Puntos por pregunta: {points_per_question}\n\n"
        "Formato de salida requerido (estructura):\n"
        f"{contract}\n\n"
        "Genera preguntas claras, sin ambigüedad, enfocadas al tema."
    )

    return instructions, user_input
