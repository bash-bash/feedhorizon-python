from __future__ import annotations

import httpx
import pytest

from feedhorizon import (
    APIConnectionError,
    APIError,
    AsyncFeedHorizon,
    AuthenticationError,
    ConflictError,
    FeedHorizon,
    FeedHorizonError,
    InternalServerError,
    InvalidRequestError,
    NotFoundError,
    RateLimitError,
    __version__,
)

from .conftest import Recorder, error

POST = {"id": "post_1", "status": "scheduled"}


def client_for(recorder: Recorder, **kwargs: object) -> FeedHorizon:
    return FeedHorizon(api_key="fh_test", http_client=httpx.Client(transport=httpx.MockTransport(recorder)), **kwargs)  # type: ignore[arg-type]


def test_create_post_sends_auth_body_and_idempotency_key() -> None:
    rec = Recorder([{"status": 201, "body": {"data": POST}}])
    post = client_for(rec).posts.create(profileId="prof_1", content="Hi", platforms=["linkedin"], publishNow=True)

    assert post == POST
    call = rec.calls[0]
    assert call.method == "POST"
    assert str(call.url) == "https://feedhorizon.com/api/v1/posts"
    assert call.headers["authorization"] == "Bearer fh_test"
    assert call.headers["content-type"] == "application/json"
    assert call.headers["user-agent"] == f"feedhorizon-python/{__version__}"
    assert call.headers["idempotency-key"].startswith("sdk-")
    assert rec.json(0) == {"profileId": "prof_1", "content": "Hi", "platforms": ["linkedin"], "publishNow": True}


def test_own_idempotency_key_and_none_on_get() -> None:
    rec = Recorder([{"body": {"data": POST}}, {"body": {"data": POST}}])
    client = client_for(rec)
    client.posts.publish("post_1", idempotency_key="mine")
    client.posts.get("post_1")
    assert rec.calls[0].headers["idempotency-key"] == "mine"
    assert rec.calls[0].url.path == "/api/v1/posts/post_1/publish"
    assert "idempotency-key" not in rec.calls[1].headers


def test_query_drops_none_maps_from_and_encodes_ids() -> None:
    rec = Recorder([{"body": {"data": [], "nextCursor": None}}, {"body": {"data": POST}}, {"body": {"data": {"slots": []}}}])
    client = client_for(rec)
    client.posts.list(profileId="prof_1", from_="2026-11-01T00:00:00Z", limit=10)
    client.posts.get("a/b")
    client.profiles.queue.slots("prof_1", count=5, free=True)
    assert dict(rec.calls[0].url.params) == {"profileId": "prof_1", "from": "2026-11-01T00:00:00Z", "limit": "10"}
    assert rec.calls[1].url.raw_path == b"/api/v1/posts/a%2Fb"
    assert dict(rec.calls[2].url.params) == {"count": "5", "free": "true"}


def test_env_key_and_base_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FEEDHORIZON_API_KEY", "fh_env")
    monkeypatch.setenv("FEEDHORIZON_BASE_URL", "http://localhost:3000/api/v1/")
    rec = Recorder([{"body": {"data": {"organization": {}}}}])
    client = FeedHorizon(http_client=httpx.Client(transport=httpx.MockTransport(rec)))
    client.me()
    assert rec.calls[0].headers["authorization"] == "Bearer fh_env"
    assert str(rec.calls[0].url) == "http://localhost:3000/api/v1/me"
    assert "fh_env" not in repr(client)


def test_missing_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FEEDHORIZON_API_KEY", raising=False)
    with pytest.raises(FeedHorizonError):
        FeedHorizon()


@pytest.mark.parametrize(
    ("status", "code", "cls"),
    [
        (400, "post_invalid", InvalidRequestError),
        (401, "invalid_api_key", AuthenticationError),
        (404, "resource_not_found", NotFoundError),
        (409, "post_not_editable", ConflictError),
    ],
)
def test_error_classes(status: int, code: str, cls: type[APIError]) -> None:
    rec = Recorder([error(status, code, details=[{"code": "content_too_long", "param": "content", "message": "too long"}])])
    with pytest.raises(cls) as info:
        client_for(rec).posts.get("post_1")
    assert info.value.status == status
    assert info.value.code == code
    assert info.value.request_id == "req_123"
    assert info.value.details[0]["code"] == "content_too_long"


def test_retries_5xx_with_same_key(no_sleep: list[float]) -> None:
    rec = Recorder([error(500, "internal_error", "api_error"), {"status": 201, "body": {"data": POST}}])
    assert client_for(rec).posts.create(profileId="prof_1", content="Hi") == POST
    assert len(rec.calls) == 2
    assert rec.calls[0].headers["idempotency-key"] == rec.calls[1].headers["idempotency-key"]
    assert len(no_sleep) == 1


def test_429_waits_retry_after_then_gives_up(no_sleep: list[float]) -> None:
    limited = {**error(429, "rate_limited", "rate_limit_error"), "headers": {"retry-after": "3"}}
    rec = Recorder([limited, limited, limited])
    with pytest.raises(RateLimitError) as info:
        client_for(rec).posts.get("post_1")
    assert info.value.retry_after == 3
    assert no_sleep == [3.0, 3.0]
    assert len(rec.calls) == 3


def test_no_retry_on_4xx() -> None:
    rec = Recorder([error(409, "post_not_editable", "conflict_error")])
    with pytest.raises(ConflictError):
        client_for(rec).posts.update("post_1", content="x")
    assert len(rec.calls) == 1


def test_network_error_retried_then_raised() -> None:
    rec = Recorder([httpx.ConnectError("down"), httpx.ConnectError("down")])
    with pytest.raises(APIConnectionError):
        client_for(rec, max_retries=1).me()
    assert len(rec.calls) == 2


def test_max_retries_zero() -> None:
    rec = Recorder([error(503, "internal_error", "api_error")])
    with pytest.raises(InternalServerError):
        client_for(rec, max_retries=0).me()


def test_pagination_iterates_all_pages() -> None:
    rec = Recorder(
        [
            {"body": {"data": [{"id": "post_1"}, {"id": "post_2"}], "nextCursor": "c2"}},
            {"body": {"data": [{"id": "post_3"}], "nextCursor": None}},
        ]
    )
    page = client_for(rec).posts.list(limit=2)
    assert [p["id"] for p in page.data] == ["post_1", "post_2"]
    assert page.has_next_page()
    assert [p["id"] for p in page] == ["post_1", "post_2", "post_3"]
    assert dict(rec.calls[1].url.params) == {"limit": "2", "cursor": "c2"}


def test_media_upload_two_steps() -> None:
    created = {
        "id": "med_1",
        "url": "https://cdn/x.png",
        "filename": "x.png",
        "mimeType": "image/png",
        "sizeBytes": 3,
        "createdAt": "2026-11-10T08:00:00.000Z",
        "upload": {
            "url": "https://storage/put",
            "method": "PUT",
            "headers": {"content-type": "image/png"},
            "expiresAt": "2026-11-10T10:00:00.000Z",
        },
    }
    rec = Recorder([{"status": 201, "body": {"data": created}}, {"status": 200}])
    media = client_for(rec).media.upload(b"\x01\x02\x03", filename="x.png", mime_type="image/png")
    assert rec.json(0) == {"filename": "x.png", "mimeType": "image/png", "sizeBytes": 3}
    assert rec.calls[1].method == "PUT"
    assert str(rec.calls[1].url) == "https://storage/put"
    assert rec.calls[1].content == b"\x01\x02\x03"
    assert rec.calls[1].headers["content-type"] == "image/png"
    assert "upload" not in media and media["id"] == "med_1"


async def test_async_client() -> None:
    rec = Recorder(
        [
            {"status": 201, "body": {"data": POST}},
            {"body": {"data": [{"id": "post_1"}], "nextCursor": "c2"}},
            {"body": {"data": [{"id": "post_2"}], "nextCursor": None}},
            {"body": {"data": [{"id": "post_1"}], "nextCursor": "c2"}},
            error(404, "resource_not_found", "not_found_error"),
        ]
    )
    async with AsyncFeedHorizon(api_key="fh_test", http_client=httpx.AsyncClient(transport=httpx.MockTransport(rec))) as client:
        assert await client.posts.create(profileId="prof_1", content="Hi") == POST
        assert [p["id"] async for p in client.posts.list()] == ["post_1", "post_2"]
        page = await client.posts.list()
        assert page.next_cursor == "c2"
        with pytest.raises(NotFoundError):
            await client.posts.get("post_x")
