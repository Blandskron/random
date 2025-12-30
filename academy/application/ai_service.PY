from __future__ import annotations

from typing import Dict, List, Tuple
from uuid import uuid4

from academy.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_TEMPERATURE,
    OPENAI_MAX_OUTPUT_TOKENS,
    OPENAI_TIMEOUT_SECONDS,
)
from academy.domain.quiz.models import Question, Choice
from academy.infrastructure.llm import OpenAIClient, OpenAISettings
from academy.infrastructure.llm.openai_errors import OpenAIResponseParseError
from academy.prompts.quiz_prompt import build_quiz_generation_prompt
from academy.prompts.schemas import parse_quiz_json, validate_quiz_payload


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def generate_quiz_with_ai(
    topic: str,
    difficulty: str = "media",
    n_questions: int = 5,
    points_per_question: int = 10,
) -> Tuple[Dict[str, Question], Dict[str, List[Choice]]]:
    """
    Genera un set de preguntas + choices usando OpenAI, y lo retorna
    en el mismo formato que tu app ya usa:
      questions: {question_id: Question}
      choices: {question_id: [Choice, Choice, ...]}
    """
    settings = OpenAISettings(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL,
        temperature=OPENAI_TEMPERATURE,
        max_output_tokens=OPENAI_MAX_OUTPUT_TOKENS,
        timeout_seconds=OPENAI_TIMEOUT_SECONDS,
    )
    client = OpenAIClient(settings)

    instructions, user_input = build_quiz_generation_prompt(
        topic=topic,
        difficulty=difficulty,
        n_questions=n_questions,
        points_per_question=points_per_question,
    )

    raw = client.create_response_text(instructions=instructions, user_input=user_input)

    try:
        payload = parse_quiz_json(raw)
    except Exception as e:
        raise OpenAIResponseParseError(f"No pude parsear JSON del modelo. raw_preview={raw[:200]}") from e

    ok, msg = validate_quiz_payload(payload)
    if not ok:
        raise OpenAIResponseParseError(f"JSON del modelo no cumple contrato: {msg}")

    questions: Dict[str, Question] = {}
    choices: Dict[str, List[Choice]] = {}

    # Convertir a tus dataclasses
    for q in payload["questions"]:
        qid = str(q.get("id") or _new_id("q")).strip()
        text = str(q["text"]).strip()
        points = int(q["points"])

        questions[qid] = Question(qid, text, points)

        local_choices: List[Choice] = []
        for c in q["choices"]:
            cid = str(c.get("id") or _new_id("c")).strip()
            ctext = str(c["text"]).strip()
            is_correct = bool(c["is_correct"])
            local_choices.append(Choice(cid, qid, ctext, is_correct))

        choices[qid] = local_choices

    return questions, choices
