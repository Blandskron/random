from __future__ import annotations


class OpenAIError(Exception):
    """Base error para integración OpenAI."""


class OpenAIAuthError(OpenAIError):
    """API key inválida / no autorizada."""


class OpenAIRateLimitError(OpenAIError):
    """Rate limit / throttling."""


class OpenAIRequestError(OpenAIError):
    """Request mal formado / parámetros inválidos."""


class OpenAIServerError(OpenAIError):
    """Errores 5xx de OpenAI."""


class OpenAIResponseParseError(OpenAIError):
    """No se pudo parsear/validar la respuesta del modelo."""
