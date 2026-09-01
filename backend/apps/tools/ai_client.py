import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class AIProviderError(RuntimeError):
    """Raised when the configured AI provider cannot return valid output."""


def ai_configured():
    return bool(os.getenv("AI_API_KEY") or os.getenv("OPENAI_API_KEY"))


def _api_key():
    return os.getenv("AI_API_KEY") or os.getenv("OPENAI_API_KEY")


def _base_url():
    return os.getenv("AI_API_BASE_URL", "https://api.openai.com/v1").rstrip("/")


def _model():
    return os.getenv("AI_MODEL", "gpt-4.1-mini")


def _extract_json(text):
    text = (text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = min((index for index in (text.find("{"), text.find("[")) if index >= 0), default=-1)
        if start < 0:
            raise AIProviderError("AI provider returned non-JSON output.")
        end = max(text.rfind("}"), text.rfind("]"))
        if end < start:
            raise AIProviderError("AI provider returned incomplete JSON output.")
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError as exc:
            raise AIProviderError("AI provider returned invalid JSON.") from exc


def generate_json(system_prompt, user_prompt, temperature=0.7, max_tokens=3000):
    if not ai_configured():
        raise AIProviderError("AI provider is not configured.")

    payload = json.dumps(
        {
            "model": _model(),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
    ).encode("utf-8")
    request = Request(
        f"{_base_url()}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "FlayerWings-Tools/1.0",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=45) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        try:
            error_payload = json.loads(exc.read().decode("utf-8"))
            message = error_payload.get("error", {}).get("message", str(exc))
        except Exception:
            message = str(exc)
        raise AIProviderError(message) from exc
    except (URLError, TimeoutError, ValueError) as exc:
        raise AIProviderError("AI provider is temporarily unavailable.") from exc

    try:
        content = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AIProviderError("AI provider returned an unexpected response.") from exc

    return _extract_json(content)
