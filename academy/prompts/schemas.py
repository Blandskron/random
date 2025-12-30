from __future__ import annotations

import json
from typing import Any, Dict, List, Tuple


def quiz_generation_contract() -> Dict[str, Any]:
    """
    Contrato de salida esperado (JSON):
    {
      "quiz_title": "string",
      "questions": [
        {
          "id": "string",
          "text": "string",
          "points": 10,
          "choices": [
            {"id": "string", "text": "string", "is_correct": true/false}
          ]
        }
      ]
    }
    """
    return {
        "quiz_title": "string",
        "questions": [
            {
                "id": "string",
                "text": "string",
                "points": "int",
                "choices": [
                    {"id": "string", "text": "string", "is_correct": "bool"}
                ],
            }
        ],
    }


def parse_quiz_json(raw_text: str) -> Dict[str, Any]:
    """
    Intenta parsear JSON. Si viene con texto extra, intenta recortar.
    """
    raw_text = raw_text.strip()

    # Caso común: el modelo devuelve ```json ... ```
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json", "", 1).strip()

    # Intento directo
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        pass

    # Heurística: buscar primer '{' y último '}'
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = raw_text[start : end + 1]
        return json.loads(candidate)

    raise ValueError("No pude parsear JSON desde la respuesta del modelo.")


def validate_quiz_payload(payload: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Valida estructura mínima (sin librerías externas).
    """
    if not isinstance(payload, dict):
        return False, "Payload no es dict."

    if "questions" not in payload or not isinstance(payload["questions"], list) or len(payload["questions"]) == 0:
        return False, "Falta 'questions' o está vacío."

    for qi, q in enumerate(payload["questions"]):
        if not isinstance(q, dict):
            return False, f"Question[{qi}] no es dict."
        for key in ("id", "text", "points", "choices"):
            if key not in q:
                return False, f"Question[{qi}] falta '{key}'."

        if not isinstance(q["id"], str) or not q["id"].strip():
            return False, f"Question[{qi}].id inválido."
        if not isinstance(q["text"], str) or not q["text"].strip():
            return False, f"Question[{qi}].text inválido."
        if not isinstance(q["points"], int) or q["points"] <= 0:
            return False, f"Question[{qi}].points debe ser int > 0."

        choices = q["choices"]
        if not isinstance(choices, list) or len(choices) < 2:
            return False, f"Question[{qi}].choices debe tener al menos 2 opciones."

        correct_count = 0
        for ci, c in enumerate(choices):
            if not isinstance(c, dict):
                return False, f"Choice[{qi}:{ci}] no es dict."
            for key in ("id", "text", "is_correct"):
                if key not in c:
                    return False, f"Choice[{qi}:{ci}] falta '{key}'."
            if not isinstance(c["id"], str) or not c["id"].strip():
                return False, f"Choice[{qi}:{ci}].id inválido."
            if not isinstance(c["text"], str) or not c["text"].strip():
                return False, f"Choice[{qi}:{ci}].text inválido."
            if not isinstance(c["is_correct"], bool):
                return False, f"Choice[{qi}:{ci}].is_correct debe ser bool."
            if c["is_correct"]:
                correct_count += 1

        if correct_count != 1:
            return False, f"Question[{qi}] debe tener exactamente 1 opción correcta (tiene {correct_count})."

    return True, "ok"
