import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class MetaGraphError(RuntimeError):
    """Raised when Meta Graph API cannot provide the requested data."""


def meta_graph_configured():
    return bool(os.getenv("META_GRAPH_ACCESS_TOKEN"))


def _graph_version():
    return os.getenv("META_GRAPH_API_VERSION", "v24.0")


def _graph_host():
    return os.getenv("META_GRAPH_API_HOST", "https://graph.facebook.com")


def graph_get(object_id, fields):
    token = os.getenv("META_GRAPH_ACCESS_TOKEN")
    if not token:
        raise MetaGraphError("Meta Graph API is not configured.")

    query = urlencode({"fields": fields, "access_token": token})
    url = f"{_graph_host().rstrip('/')}/{_graph_version()}/{object_id}?{query}"
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "FlayerWings-Tools/1.0"})

    try:
        with urlopen(request, timeout=12) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        try:
            error_payload = json.loads(exc.read().decode("utf-8"))
        except Exception:
            error_payload = {"error": {"message": str(exc)}}
        message = error_payload.get("error", {}).get("message", "Meta Graph API request failed.")
        raise MetaGraphError(message) from exc
    except (URLError, TimeoutError, ValueError) as exc:
        raise MetaGraphError("Meta Graph API is temporarily unavailable.") from exc

    if payload.get("error"):
        raise MetaGraphError(payload["error"].get("message", "Meta Graph API request failed."))
    return payload


def get_business_discovery(username):
    username = username.lstrip("@").strip()
    fields = (
        "business_discovery.username(" + username + "){"
        "id,username,name,biography,website,followers_count,follows_count,media_count,"
        "profile_picture_url,media.limit(12){id,caption,media_type,media_product_type,"
        "permalink,timestamp,like_count,comments_count}"
        "}"
    )
    return graph_get("me", fields).get("business_discovery")
