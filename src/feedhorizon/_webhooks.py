from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any, cast

from ._errors import WebhookVerificationError
from .types import WebhookEvent

__all__ = ["verify_webhook", "construct_webhook_event", "sign_webhook_payload"]


def _text(payload: str | bytes | bytearray) -> str:
    return payload if isinstance(payload, str) else bytes(payload).decode("utf-8")


def sign_webhook_payload(payload: str | bytes, secret: str, timestamp: int) -> str:
    """The ``X-Webhook-Signature`` FeedHorizon would send for this body and time. Useful in tests."""
    digest = hmac.new(secret.encode(), f"{timestamp}.{_text(payload)}".encode(), hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={digest}"


def verify_webhook(
    payload: str | bytes | bytearray,
    signature: str | None,
    secret: str,
    *,
    tolerance_seconds: int = 300,
    now: float | None = None,
) -> None:
    """Checks the ``X-Webhook-Signature`` header of a delivery.

    ``payload`` must be the raw request body, exactly as received: parsing and
    re-serializing the JSON breaks the signature. Raises ``WebhookVerificationError``
    when the signature is missing, wrong or older than ``tolerance_seconds``.
    """
    if not signature:
        raise WebhookVerificationError("Missing X-Webhook-Signature header")
    if not secret:
        raise WebhookVerificationError("Missing webhook secret")

    timestamp: int | None = None
    candidates: list[str] = []
    for part in signature.split(","):
        key, _, value = part.strip().partition("=")
        if key == "t":
            try:
                timestamp = int(value)
            except ValueError:
                timestamp = None
        elif key == "v1" and value:
            candidates.append(value)
    if not timestamp or not candidates:
        raise WebhookVerificationError("Malformed X-Webhook-Signature header")

    current = time.time() if now is None else now
    if abs(current - timestamp) > tolerance_seconds:
        raise WebhookVerificationError("Webhook timestamp is outside the tolerance; possible replay")

    expected = sign_webhook_payload(_text(payload), secret, timestamp).split("v1=", 1)[1]
    if not any(hmac.compare_digest(candidate, expected) for candidate in candidates):
        raise WebhookVerificationError("Webhook signature does not match")


def construct_webhook_event(
    payload: str | bytes | bytearray,
    signature: str | None,
    secret: str,
    *,
    tolerance_seconds: int = 300,
    now: float | None = None,
) -> WebhookEvent:
    """Verifies a delivery and returns the parsed event. Check ``event["event"]`` to see which one it is."""
    verify_webhook(payload, signature, secret, tolerance_seconds=tolerance_seconds, now=now)
    try:
        data: Any = json.loads(_text(payload))
    except ValueError as exc:
        raise WebhookVerificationError("Webhook body is not valid JSON") from exc
    return cast(WebhookEvent, data)
