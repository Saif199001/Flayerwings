import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class AIProviderError(RuntimeError):
    """Raised when the configured AI provider cannot return valid output."""


def ai_configured():
    provider = _provider()
    if provider == "gemini":
        return bool(os.getenv("AI_API_KEY") or os.getenv("GEMINI_API_KEY"))
    return bool(os.getenv("AI_API_KEY") or os.getenv("OPENAI_API_KEY"))


def _provider():
    return os.getenv("AI_PROVIDER", "gemini").strip().lower()


def _api_key():
    if _provider() == "gemini":
        return os.getenv("AI_API_KEY") or os.getenv("GEMINI_API_KEY")
    return os.getenv("AI_API_KEY") or os.getenv("OPENAI_API_KEY")


def _base_url():
    configured = os.getenv("AI_API_BASE_URL")
    if configured:
        configured = configured.rstrip("/")
        if _provider() == "gemini" and configured.endswith("/openai"):
            configured = configured[: -len("/openai")]
        return configured
    if _provider() == "gemini":
        return "https://generativelanguage.googleapis.com/v1beta"
    return "https://api.openai.com/v1"


def _model():
    configured = os.getenv("AI_MODEL")
    if configured:
        return configured
    return "gemini-2.5-flash" if _provider() == "gemini" else "gpt-4.1-mini"


def _extract_json(text):
    text = (text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        starts = [index for index in (text.find("{"), text.find("[")) if index >= 0]
        start = min(starts, default=-1)
        if start < 0:
            raise AIProviderError("AI provider returned non-JSON output.")
        end = max(text.rfind("}"), text.rfind("]"))
        if end < start:
            raise AIProviderError("AI provider returned incomplete JSON output.")
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError as exc:
            raise AIProviderError("AI provider returned invalid JSON.") from exc


def _request_json(url, payload, headers=None):
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "FlayerWings-Tools/1.0",
            **(headers or {}),
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        try:
            body = exc.read().decode("utf-8")
            error_payload = json.loads(body)
            message = (
                error_payload.get("error", {}).get("message")
                or error_payload.get("message")
                or body
                or str(exc)
            )
        except Exception:
            message = str(exc)
        raise AIProviderError(f"AI provider HTTP {exc.code}: {message}") from exc
    except (URLError, TimeoutError, ValueError) as exc:
        raise AIProviderError("AI provider is temporarily unavailable.") from exc


def _generate_gemini(system_prompt, user_prompt, temperature, max_tokens):
    url = f"{_base_url()}/models/{_model()}:generateContent?" + urlencode({"key": _api_key()})
    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
            "responseMimeType": "application/json",
        },
    }
    result = _request_json(url, payload)
    if isinstance(result, dict) and result.get("error"):
        raise AIProviderError(result["error"].get("message", "Gemini API request failed."))
    try:
        parts = result["candidates"][0]["content"]["parts"]
        content = "".join(part.get("text", "") for part in parts).strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise AIProviderError("Gemini returned an unexpected response.") from exc
    if not content:
        raise AIProviderError("Gemini returned an empty response.")
    return _extract_json(content)


def _generate_openai_compatible(system_prompt, user_prompt, temperature, max_tokens):
    payload = {
        "model": _model(),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    result = _request_json(
        f"{_base_url()}/chat/completions",
        payload,
        headers={"Authorization": f"Bearer {_api_key()}"},
    )
    if isinstance(result, dict) and result.get("error"):
        raise AIProviderError(result["error"].get("message", "AI provider request failed."))
    try:
        content = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise AIProviderError("AI provider returned an unexpected response.") from exc
    return _extract_json(content)


def generate_json(system_prompt, user_prompt, temperature=0.7, max_tokens=3000):
    if not ai_configured():
        raise AIProviderError("AI provider is not configured.")
    if _provider() == "gemini":
        return _generate_gemini(system_prompt, user_prompt, temperature, max_tokens)
    if _provider() == "openai":
        return _generate_openai_compatible(system_prompt, user_prompt, temperature, max_tokens)
    raise AIProviderError(f"Unsupported AI provider: {_provider()}")
