from __future__ import annotations

import asyncio
import json
import os
import random
import time
import uuid
from collections.abc import Mapping
from typing import Any, TypeVar

import httpx

from ._errors import APIConnectionError, APIError, APITimeoutError, FeedHorizonError
from ._pagination import AsyncPage, AsyncPager, Page
from ._version import __version__

T = TypeVar("T")

DEFAULT_BASE_URL = "https://feedhorizon.com/api/v1"
DEFAULT_TIMEOUT = 60.0
DEFAULT_MAX_RETRIES = 2

Query = Mapping[str, Any]


class _Base:
    """Configuration and retry policy shared by the sync and the async client."""

    def __init__(
        self,
        api_key: str | None,
        base_url: str | None,
        timeout: float,
        max_retries: int,
        default_headers: Mapping[str, str] | None,
    ) -> None:
        api_key = api_key or os.environ.get("FEEDHORIZON_API_KEY")
        if not api_key:
            raise FeedHorizonError("No API key. Pass api_key or set the FEEDHORIZON_API_KEY environment variable.")
        self._api_key = api_key
        self.base_url = (base_url or os.environ.get("FEEDHORIZON_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._default_headers = dict(default_headers or {})

    def __repr__(self) -> str:
        return f"{type(self).__name__}(base_url={self.base_url!r})"

    def _build(
        self,
        method: str,
        path: str,
        query: Query | None,
        body: Any,
        headers: Mapping[str, str] | None,
        idempotency_key: str | None,
    ) -> dict[str, Any]:
        params = {k: _query_value(v) for k, v in (query or {}).items() if v is not None}
        all_headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._api_key}",
            "User-Agent": f"feedhorizon-python/{__version__}",
            **self._default_headers,
            **(headers or {}),
        }
        if idempotency_key:
            all_headers["Idempotency-Key"] = idempotency_key
        request: dict[str, Any] = {"method": method, "url": self.base_url + path, "params": params, "headers": all_headers}
        if body is not None:
            all_headers["Content-Type"] = "application/json"
            request["content"] = json.dumps(body)
        return request

    @staticmethod
    def _idempotency_key(method: str, given: str | None) -> str | None:
        # One key for all attempts, so a retry after a lost answer never runs twice.
        if method == "GET":
            return None
        return given or f"sdk-{uuid.uuid4()}"

    @staticmethod
    def _should_retry(error: APIError) -> bool:
        if error.status in (408, 429) or error.status >= 500:
            return True
        return error.status == 409 and error.code == "idempotency_request_in_progress"

    @staticmethod
    def _backoff(attempt: int, retry_after: str | None = None) -> float:
        try:
            seconds = float(retry_after) if retry_after else 0.0
        except ValueError:
            seconds = 0.0
        if 0 < seconds <= 60:
            return seconds
        base = min(0.5 * 2**attempt, 8.0)
        return base * (0.75 + random.random() * 0.25)

    @staticmethod
    def _parse(response: httpx.Response) -> Any:
        if not response.content:
            return {}
        return response.json()

    @staticmethod
    def _error(response: httpx.Response) -> APIError:
        try:
            body = response.json()
        except ValueError:
            body = None
        return APIError.from_response(response.status_code, body, response.headers)


def _query_value(value: Any) -> Any:
    if isinstance(value, bool):
        return "true" if value else "false"
    return value


class SyncAPIClient(_Base):
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        super().__init__(api_key, base_url, timeout, max_retries, default_headers)
        self._http = http_client or httpx.Client(timeout=timeout)
        self._owns_http = http_client is None

    def close(self) -> None:
        """Closes the HTTP connection pool."""
        if self._owns_http:
            self._http.close()

    def __enter__(self: T) -> T:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        query: Query | None = None,
        body: Any = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        """Sends a request with retries and returns the parsed JSON body."""
        retries = self.max_retries if max_retries is None else max_retries
        request = self._build(method, path, query, body, headers, self._idempotency_key(method, idempotency_key))
        attempt = 0
        while True:
            try:
                response = self._http.request(**request, timeout=timeout if timeout is not None else self.timeout)
            except httpx.TimeoutException as exc:
                if attempt < retries:
                    time.sleep(self._backoff(attempt))
                    attempt += 1
                    continue
                raise APITimeoutError(f"Request timed out: {exc}") from exc
            except httpx.TransportError as exc:
                if attempt < retries:
                    time.sleep(self._backoff(attempt))
                    attempt += 1
                    continue
                raise APIConnectionError(f"Could not reach FeedHorizon: {exc}") from exc

            if response.is_success:
                return self._parse(response)
            error = self._error(response)
            if attempt < retries and self._should_retry(error):
                time.sleep(self._backoff(attempt, response.headers.get("retry-after")))
                attempt += 1
                continue
            raise error

    def _data(self, method: str, path: str, **kwargs: Any) -> Any:
        return self.request(method, path, **kwargs)["data"]

    def _list(self, path: str, query: Query | None = None, **kwargs: Any) -> Page[Any]:
        def load(cursor: str | None) -> Page[Any]:
            q = {**(query or {}), **({"cursor": cursor} if cursor else {})}
            body = self.request("GET", path, query=q, **kwargs)
            return Page(body["data"], body.get("nextCursor"), load)

        return load(None)


class AsyncAPIClient(_Base):
    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(api_key, base_url, timeout, max_retries, default_headers)
        self._http = http_client or httpx.AsyncClient(timeout=timeout)
        self._owns_http = http_client is None

    async def close(self) -> None:
        """Closes the HTTP connection pool."""
        if self._owns_http:
            await self._http.aclose()

    async def __aenter__(self: T) -> T:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    async def request(
        self,
        method: str,
        path: str,
        *,
        query: Query | None = None,
        body: Any = None,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        """Sends a request with retries and returns the parsed JSON body."""
        retries = self.max_retries if max_retries is None else max_retries
        request = self._build(method, path, query, body, headers, self._idempotency_key(method, idempotency_key))
        attempt = 0
        while True:
            try:
                response = await self._http.request(**request, timeout=timeout if timeout is not None else self.timeout)
            except httpx.TimeoutException as exc:
                if attempt < retries:
                    await asyncio.sleep(self._backoff(attempt))
                    attempt += 1
                    continue
                raise APITimeoutError(f"Request timed out: {exc}") from exc
            except httpx.TransportError as exc:
                if attempt < retries:
                    await asyncio.sleep(self._backoff(attempt))
                    attempt += 1
                    continue
                raise APIConnectionError(f"Could not reach FeedHorizon: {exc}") from exc

            if response.is_success:
                return self._parse(response)
            error = self._error(response)
            if attempt < retries and self._should_retry(error):
                await asyncio.sleep(self._backoff(attempt, response.headers.get("retry-after")))
                attempt += 1
                continue
            raise error

    async def _data(self, method: str, path: str, **kwargs: Any) -> Any:
        return (await self.request(method, path, **kwargs))["data"]

    def _list(self, path: str, query: Query | None = None, **kwargs: Any) -> AsyncPager[Any]:
        async def load(cursor: str | None = None) -> AsyncPage[Any]:
            q = {**(query or {}), **({"cursor": cursor} if cursor else {})}
            body = await self.request("GET", path, query=q, **kwargs)
            return AsyncPage(body["data"], body.get("nextCursor"), load)

        return AsyncPager(load)
