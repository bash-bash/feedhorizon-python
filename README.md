# FeedHorizon Python SDK

The official Python client for the [FeedHorizon API](https://feedhorizon.com/docs): schedule and publish posts on X, LinkedIn, Instagram, Bluesky, Pinterest and TikTok with one API.

- Sync and async clients (`FeedHorizon`, `AsyncFeedHorizon`)
- Typed parameters and responses (`TypedDict`), generated from the [OpenAPI spec](https://feedhorizon.com/openapi.json)
- Automatic retries with idempotency keys, so a retry never posts twice
- Iterate any list across all pages
- Webhook signature verification
- Python 3.10+, depends only on `httpx`

## Install

```bash
pip install feedhorizon
```

## Quickstart

Create an API key under **API & Apps** in the [dashboard](https://feedhorizon.com/dashboard/api-keys) and set it as `FEEDHORIZON_API_KEY`.

```python
from feedhorizon import FeedHorizon

client = FeedHorizon()  # reads FEEDHORIZON_API_KEY

profile = client.profiles.list().data[0]

post = client.posts.create(
    profileId=profile["id"],
    content="Hello from the FeedHorizon SDK!",
    platforms=["linkedin", "bluesky"],
    scheduledFor="2026-11-12T09:00:00+01:00",
)
print(post["id"], post["status"])  # post_… scheduled
```

Parameters and fields use the API's names (`profileId`, `scheduledFor`), so everything in the [API reference](https://feedhorizon.com/docs/api) applies one to one. Responses are plain dicts with type hints.

Leave out the timing field for a draft, or send `addToQueue=True` or `publishNow=True` instead of `scheduledFor`. See [Scheduling](https://feedhorizon.com/docs/guides/scheduling).

## Async

```python
import asyncio
from feedhorizon import AsyncFeedHorizon


async def main() -> None:
    async with AsyncFeedHorizon() as client:
        post = await client.posts.get("post_…")
        async for failed in client.posts.list(status="failed"):
            print(failed["id"])


asyncio.run(main())
```

## Check a post before creating it

```python
check = client.posts.validate(profileId=profile_id, content=text, platforms=["twitter", "instagram"])
if not check["valid"]:
    for issue in check["errors"]:
        print(issue["code"], issue["message"])
```

## Media

```python
# From a public URL
image = client.media.import_url("https://example.com/launch.jpg")

# From a file (up to 5 GB)
with open("teaser.mp4", "rb") as f:
    video = client.media.upload(f, filename="teaser.mp4", mime_type="video/mp4")

client.posts.create(
    profileId=profile_id, content="The teaser is out", platforms=["instagram"], mediaIds=[image["id"], video["id"]], addToQueue=True
)
```

## Lists and pagination

A list call returns the first page. Iterate it for every item across all pages:

```python
page = client.posts.list(status="failed", limit=50)
print(len(page.data), page.has_next_page())

for post in client.posts.list(updatedSince="2026-11-01T00:00:00Z"):
    print(post["id"], post["status"])
```

`from` is a Python keyword, so the calendar filter of `posts.list` is `from_`.

## Errors

Every API error is an `APIError` with `status`, `code`, `message`, `param`, `details` and `request_id`. Branch on `code`; the [error reference](https://feedhorizon.com/docs/api/errors) lists them all.

```python
from feedhorizon import ConflictError, InvalidRequestError

try:
    client.posts.update(post_id, content="New text")
except InvalidRequestError as e:
    for d in e.details:
        print(d["code"], d.get("param"), d["message"])
except ConflictError as e:
    if e.code == "post_not_editable":
        ...  # already publishing or published
```

| Class | Status |
| --- | --- |
| `InvalidRequestError` | 400, 422 |
| `AuthenticationError` | 401 |
| `PermissionDeniedError` | 403 |
| `NotFoundError` | 404 |
| `ConflictError` | 409 |
| `RateLimitError` | 429 (`retry_after` in seconds) |
| `InternalServerError` | 5xx |
| `APIConnectionError`, `APITimeoutError` | no answer |

## Retries and idempotency

Network errors, timeouts, `429` and `5xx` are retried twice with backoff (honouring `Retry-After`). Every write gets an `Idempotency-Key`, the same on each attempt, so a retry after a lost answer returns the first result instead of creating a second post. Pass your own key to make retries safe across process restarts:

```python
client.posts.create(**params, idempotency_key=f"launch-{campaign_id}")
```

```python
client = FeedHorizon(max_retries=5, timeout=30)
client.posts.get(post_id, max_retries=0, timeout=5)
```

## Webhooks

Verify the signature against the **raw** body, then handle the event:

```python
import os

from flask import Flask, request
from feedhorizon import WebhookVerificationError, construct_webhook_event

app = Flask(__name__)


@app.post("/webhooks/feedhorizon")
def feedhorizon_webhook():
    try:
        event = construct_webhook_event(
            request.get_data(), request.headers.get("X-Webhook-Signature"), os.environ["FEEDHORIZON_WEBHOOK_SECRET"]
        )
    except WebhookVerificationError:
        return "", 400

    if event["event"] == "post.target.failed":
        print(event["data"]["platform"], event["data"]["error"])
    return "", 200
```

## Resources

| | Methods |
| --- | --- |
| `client.me()` | Organization, plan, rate limit and scopes of the key |
| `client.posts` | `list`, `get`, `create`, `validate`, `update`, `delete`, `publish`, `cancel`, `retry`, `duplicate` |
| `client.media` | `list`, `get`, `create`, `import_url`, `upload`, `delete` |
| `client.profiles` | `list`, `get`, `create`, `update`, `delete` |
| `client.profiles.queue` | `get`, `set`, `slots` |
| `client.accounts` | `list`, `get`, `delete`, `boards`, `tiktok_creator` |
| `client.platforms` | `list`, `get` |
| `client.platform_invites` | `list`, `create`, `delete` (connect links) |
| `client.webhooks` | `list`, `get`, `create`, `update`, `delete`, `test` |
| `client.api_keys` | `list`, `create`, `delete` |

Every method also takes `timeout`, `max_retries` and `extra_headers`; writes take `idempotency_key`.

## Configuration

| Argument | Default |
| --- | --- |
| `api_key` | `FEEDHORIZON_API_KEY` |
| `base_url` | `FEEDHORIZON_BASE_URL`, else `https://feedhorizon.com/api/v1` |
| `timeout` | `60` seconds |
| `max_retries` | `2` |
| `default_headers` | none |
| `http_client` | a new `httpx.Client` / `httpx.AsyncClient` |

Use the client as a context manager (`with FeedHorizon() as client:`) or call `close()` to release connections.

## Development

```bash
uv sync
uv run pytest
uv run mypy
curl -fsSL https://feedhorizon.com/openapi.json -o spec/openapi.json && python scripts/generate_types.py
```

`_async_resources.py` is generated from `_resources.py` by `scripts/generate_async.py`. Releases are published to PyPI from GitHub releases (tag `vX.Y.Z`) with trusted publishing.

## License

MIT
