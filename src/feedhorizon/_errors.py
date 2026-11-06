from __future__ import annotations

from typing import Any

import httpx

__all__ = [
    "FeedHorizonError",
    "APIError",
    "InvalidRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "RateLimitError",
    "InternalServerError",
    "APIConnectionError",
    "APITimeoutError",
    "WebhookVerificationError",
]


class FeedHorizonError(Exception):
    """Base class of every error this SDK raises."""


class APIError(FeedHorizonError):
    """The API answered with an error status. Branch on ``code``, not on the message.

    Every code is listed at https://feedhorizon.com/docs/api/errors
    """

    status: int
    """HTTP status, e.g. 400."""
    type: str
    """Error type, e.g. ``invalid_request_error``."""
    code: str
    """Error code, e.g. ``content_too_long``."""
    message: str
    param: str | None
    """The request field the error is about, if any."""
    details: list[dict[str, Any]]
    """Every problem at once, for ``post_invalid`` and ``validation_failed``."""
    request_id: str | None
    """Quote this when you contact support."""
    doc_url: str | None
    headers: httpx.Headers
    body: Any

    def __init__(self, status: int, body: Any, headers: httpx.Headers) -> None:
        error: dict[str, Any] = body["error"] if isinstance(body, dict) and isinstance(body.get("error"), dict) else {}
        self.status = status
        self.type = error.get("type") or "api_error"
        self.code = error.get("code") or "unknown"
        self.message = error.get("message") or f"HTTP {status}"
        self.param = error.get("param")
        self.details = error.get("details") or []
        self.request_id = error.get("requestId") or headers.get("x-request-id")
        self.doc_url = error.get("docUrl")
        self.headers = headers
        self.body = body
        super().__init__(f"{self.message} (status {status}, code {self.code})")

    @staticmethod
    def from_response(status: int, body: Any, headers: httpx.Headers) -> APIError:
        cls: type[APIError] = APIError
        if status in (400, 422):
            cls = InvalidRequestError
        elif status == 401:
            cls = AuthenticationError
        elif status == 403:
            cls = PermissionDeniedError
        elif status == 404:
            cls = NotFoundError
        elif status == 409:
            cls = ConflictError
        elif status == 429:
            cls = RateLimitError
        elif status >= 500:
            cls = InternalServerError
        return cls(status, body, headers)


class InvalidRequestError(APIError):
    """400 or 422: the request breaks a rule. ``details`` lists every problem."""


class AuthenticationError(APIError):
    """401: no key, or the key is unknown, revoked or expired."""


class PermissionDeniedError(APIError):
    """403: the key lacks a scope or access to the profile."""


class NotFoundError(APIError):
    """404: the object does not exist or the key cannot see it."""


class ConflictError(APIError):
    """409: the current state does not allow this, e.g. editing a published post."""


class RateLimitError(APIError):
    """429: too many requests."""

    @property
    def retry_after(self) -> float | None:
        """Seconds to wait, from the ``Retry-After`` header."""
        try:
            value = float(self.headers.get("retry-after", ""))
        except ValueError:
            return None
        return value if value > 0 else None


class InternalServerError(APIError):
    """5xx: something failed on FeedHorizon's side."""


class APIConnectionError(FeedHorizonError):
    """The request never got an answer: network error or DNS failure."""


class APITimeoutError(APIConnectionError):
    """The request took longer than ``timeout``."""


class WebhookVerificationError(FeedHorizonError):
    """A webhook signature is missing, malformed, wrong or too old."""
