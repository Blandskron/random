from __future__ import annotations


def build_answer_evaluation_prompt(question_text: str, user_answer: str, correct_answer: str) -> tuple[str, str]:
    """
    Retorna (instructions, user_input) para evaluar y dar feedback.
    (No lo usamos todavía en el flujo principal, pero queda listo.)
    """
    instructions = (
        "Eres un evaluador pedagógico.\n"
        "Devuelve SOLO JSON válido, sin texto extra.\n"
        "Campos: {\"is_correct\": bool, \"feedback\": string, \"suggestion\": string}\n"
    )

    user_input = (
        f"Pregunta: {question_text}\n"
        f"Respuesta del usuario: {user_answer}\n"
        f"Respuesta correcta: {correct_answer}\n"
        "Evalúa si es correcta y entrega feedback breve y útil."
    )

    return instructions, user_input
