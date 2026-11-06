from __future__ import annotations

import hashlib
import hmac
import json

import pytest

from feedhorizon import WebhookVerificationError, construct_webhook_event, sign_webhook_payload, verify_webhook

SECRET = "whsec_test"
PAYLOAD = json.dumps({"id": "evt_1", "event": "post.target.failed", "timestamp": "2026-11-10T08:00:00.000Z", "data": {"postId": "post_1"}})
T = 1_800_000_000
# The server's algorithm (feedwave src/lib/webhooks.ts): hex HMAC-SHA256 of "<t>.<body>".
HEADER = f"t={T},v1=" + hmac.new(SECRET.encode(), f"{T}.{PAYLOAD}".encode(), hashlib.sha256).hexdigest()


def test_signs_like_the_server() -> None:
    assert sign_webhook_payload(PAYLOAD, SECRET, T) == HEADER


def test_valid_delivery() -> None:
    event = construct_webhook_event(PAYLOAD.encode(), HEADER, SECRET, now=T + 10)
    assert event["event"] == "post.target.failed"
    verify_webhook(PAYLOAD, HEADER, SECRET, now=T)


@pytest.mark.parametrize(
    ("payload", "header", "secret", "now"),
    [
        (PAYLOAD.replace("post_1", "post_2"), HEADER, SECRET, T),
        (PAYLOAD, HEADER, "whsec_other", T),
        (PAYLOAD, HEADER, SECRET, T + 301),
        (PAYLOAD, None, SECRET, T),
        (PAYLOAD, "v1=abc", SECRET, T),
    ],
)
def test_rejects(payload: str, header: str | None, secret: str, now: int) -> None:
    with pytest.raises(WebhookVerificationError):
        verify_webhook(payload, header, secret, now=now)
