from __future__ import annotations

import json
import socket
import urllib.error
import urllib.request
from dataclasses import asdict

from academy.infrastructure.llm.openai_models import OpenAISettings
from academy.infrastructure.llm.openai_errors import (
    OpenAIAuthError,
    OpenAIRateLimitError,
    OpenAIRequestError,
    OpenAIServerError,
    OpenAIError,
)


class OpenAIClient:
    """
    Cliente minimalista (stdlib) para OpenAI Responses API.
    - Sin SDK
    - Timeout configurable
    - Manejo de errores comunes
    """

    def __init__(self, settings: OpenAISettings) -> None:
        if not settings.api_key:
            raise OpenAIAuthError("OPENAI_API_KEY no está configurada.")
        self.settings = settings

    def create_response_text(self, instructions: str, user_input: str) -> str:
        """
        Retorna texto (idealmente JSON) generado por el modelo.
        """
        payload = {
            "model": self.settings.model,
            "instructions": instructions,
            "input": user_input,
            "temperature": self.settings.temperature,
            "max_output_tokens": self.settings.max_output_tokens,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.settings.base_url,
            data=data,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.settings.api_key}",
                "Content-Type": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=self.settings.timeout_seconds) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                obj = json.loads(raw)
                return self._extract_output_text(obj)
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8", errors="replace")
            except Exception:
                body = ""

            status = getattr(e, "code", None)
            if status in (401, 403):
                raise OpenAIAuthError(f"OpenAI Auth error ({status}). {body}")
            if status == 429:
                raise OpenAIRateLimitError(f"OpenAI Rate limit ({status}). {body}")
            if status and 400 <= status < 500:
                raise OpenAIRequestError(f"OpenAI Request error ({status}). {body}")
            if status and 500 <= status:
                raise OpenAIServerError(f"OpenAI Server error ({status}). {body}")
            raise OpenAIError(f"OpenAI HTTP error ({status}). {body}") from e
        except (socket.timeout, TimeoutError) as e:
            raise OpenAIError("Timeout llamando a OpenAI.") from e
        except json.JSONDecodeError as e:
            raise OpenAIError("Respuesta no es JSON válido (error parse).") from e

    def _extract_output_text(self, response_obj: dict) -> str:
        """
        Responses API suele devolver salida en response_obj["output"] como lista de items.
        Extraemos el texto del primer contenido disponible.
        """
        output = response_obj.get("output", [])
        # Formato típico: output -> [{type:"message", content:[{type:"output_text", text:"..."}]}]
        for item in output:
            content = item.get("content", [])
            for c in content:
                if c.get("type") in ("output_text", "text"):
                    txt = c.get("text", "")
                    if txt:
                        return txt
        # Fallbacks comunes
        if "output_text" in response_obj and response_obj["output_text"]:
            return str(response_obj["output_text"])
        if "text" in response_obj and response_obj["text"]:
            return str(response_obj["text"])

        raise OpenAIError(f"No pude extraer texto del response: keys={list(response_obj.keys())}")
