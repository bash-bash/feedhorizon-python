from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

import httpx
import pytest

Reply = dict[str, Any] | Exception


class Recorder:
    """Answers requests from a queue and records them."""

    def __init__(self, replies: list[Reply]) -> None:
        self.replies = list(replies)
        self.calls: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.calls.append(request)
        if not self.replies:
            raise AssertionError("No reply left")
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        body = reply.get("body")
        return httpx.Response(
            reply.get("status", 200),
            content=b"" if body is None else json.dumps(body).encode(),
            headers={"content-type": "application/json", **reply.get("headers", {})},
        )

    def json(self, index: int) -> Any:
        return json.loads(self.calls[index].content)


def error(status: int, code: str, type_: str = "invalid_request_error", **extra: Any) -> dict[str, Any]:
    return {
        "status": status,
        "body": {
            "error": {
                "type": type_,
                "code": code,
                "message": f"{code} happened",
                "docUrl": "https://feedhorizon.com/docs/api/errors",
                "requestId": "req_123",
                **extra,
            }
        },
    }


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch: pytest.MonkeyPatch) -> list[float]:
    """Retries sleep for real otherwise; record the waits instead."""
    waits: list[float] = []

    async def fake_async_sleep(seconds: float) -> None:
        waits.append(seconds)

    monkeypatch.setattr("feedhorizon._client.time.sleep", waits.append)
    monkeypatch.setattr("feedhorizon._client.asyncio.sleep", fake_async_sleep)
    return waits


@pytest.fixture
def make_recorder() -> Callable[[list[Reply]], Recorder]:
    return Recorder
