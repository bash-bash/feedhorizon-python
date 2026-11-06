"""Async resources. Generated from _resources.py by scripts/generate_async.py; do not edit."""

from __future__ import annotations

from collections.abc import Mapping
from typing import IO, TYPE_CHECKING, Any, Literal

from typing_extensions import Unpack

from ._errors import FeedHorizonError
from ._pagination import AsyncPager
from .types import (
    Account,
    ApiKey,
    ApiKeyCreated,
    ApiKeyCreateParams,
    Media,
    MediaCreated,
    MediaCreateParams,
    PinterestBoardList,
    Platform,
    PlatformId,
    PlatformInvite,
    PlatformInviteCreated,
    PlatformInviteCreateParams,
    Post,
    PostCreateParams,
    PostUpdateParams,
    PostValidateParams,
    PostValidation,
    Profile,
    ProfileCreateParams,
    ProfileUpdateParams,
    Queue,
    QueueSetParams,
    QueueSlots,
    TikTokCreatorInfo,
    Webhook,
    WebhookCreated,
    WebhookCreateParams,
    WebhookTestResult,
    WebhookUpdateParams,
)

if TYPE_CHECKING:
    from ._client import AsyncAPIClient

Deleted = Mapping[str, Any]
PostStatus = Literal["draft", "scheduled", "publishing", "published", "partially_failed", "failed"]


def _id(value: str) -> str:
    from urllib.parse import quote

    return quote(value, safe="")


class _AsyncResource:
    def __init__(self, client: AsyncAPIClient) -> None:
        self._client = client


class AsyncPosts(_AsyncResource):
    def list(
        self,
        *,
        profileId: str | None = None,
        status: PostStatus | None = None,
        platform: PlatformId | None = None,
        from_: str | None = None,
        to: str | None = None,
        updatedSince: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> AsyncPager[Post]:
        """Lists posts, newest first. With ``from_`` or ``to`` it is a calendar range, oldest first.

        Iterate the result for every post across all pages.
        """
        query = {
            "profileId": profileId,
            "status": status,
            "platform": platform,
            "from": from_,
            "to": to,
            "updatedSince": updatedSince,
            "limit": limit,
            "cursor": cursor,
        }
        return self._client._list("/posts", query, timeout=timeout, max_retries=max_retries, headers=extra_headers)

    async def get(
        self, post_id: str, *, timeout: float | None = None, max_retries: int | None = None, extra_headers: Mapping[str, str] | None = None
    ) -> Post:
        return await self._client._data("GET", f"/posts/{_id(post_id)}", timeout=timeout, max_retries=max_retries, headers=extra_headers)

    async def create(
        self,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
        **params: Unpack[PostCreateParams],
    ) -> Post:
        """Creates a draft, a scheduled post (``scheduledFor``), a queued post (``addToQueue``) or publishes right away (``publishNow``).

        Raises ``InvalidRequestError`` with every problem in ``details`` if the post breaks a platform's rules.
        """
        return await self._client._data(
            "POST", "/posts", body=params, idempotency_key=idempotency_key, timeout=timeout, max_retries=max_retries, headers=extra_headers
        )

    async def validate(
        self,
        *,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
        **params: Unpack[PostValidateParams],
    ) -> PostValidation:
        """Runs every check of ``create`` without creating anything."""
        return await self._client._data("POST", "/posts/validate", body=params, timeout=timeout, max_retries=max_retries, headers=extra_headers)

    async def update(
        self,
        post_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
        **params: Unpack[PostUpdateParams],
    ) -> Post:
        """Changes a post that has not started publishing. ``scheduledFor=None`` makes it a draft."""
        return await self._client._data(
            "PATCH",
            f"/posts/{_id(post_id)}",
            body=params,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def delete(
        self,
        post_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Deleted:
        """Deletes the post in FeedHorizon. AsyncPosts already live stay on the platforms."""
        return await self._client._data(
            "DELETE",
            f"/posts/{_id(post_id)}",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def publish(
        self,
        post_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Post:
        """Publishes a draft or scheduled post right away."""
        return await self._client._data(
            "POST",
            f"/posts/{_id(post_id)}/publish",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def cancel(
        self,
        post_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Post:
        """Takes a scheduled post off the schedule; it stays as a draft."""
        return await self._client._data(
            "POST",
            f"/posts/{_id(post_id)}/cancel",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def retry(
        self,
        post_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Post:
        """Sends the failed accounts of a post again."""
        return await self._client._data(
            "POST",
            f"/posts/{_id(post_id)}/retry",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def duplicate(
        self,
        post_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Post:
        """Copies a post as a new draft."""
        return await self._client._data(
            "POST",
            f"/posts/{_id(post_id)}/duplicate",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )


class AsyncMediaResource(_AsyncResource):
    def list(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> AsyncPager[Media]:
        return self._client._list(
            "/media", {"limit": limit, "cursor": cursor}, timeout=timeout, max_retries=max_retries, headers=extra_headers
        )

    async def get(
        self, media_id: str, *, timeout: float | None = None, max_retries: int | None = None, extra_headers: Mapping[str, str] | None = None
    ) -> Media:
        return await self._client._data("GET", f"/media/{_id(media_id)}", timeout=timeout, max_retries=max_retries, headers=extra_headers)

    async def create(
        self,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
        **params: Unpack[MediaCreateParams],
    ) -> MediaCreated:
        """Imports a file from a public https ``url`` (up to 100 MB), or announces an upload (``filename``, ``mimeType``, ``sizeBytes``).

        For uploads, ``upload()`` does both steps.
        """
        return await self._client._data(
            "POST", "/media", body=params, idempotency_key=idempotency_key, timeout=timeout, max_retries=max_retries, headers=extra_headers
        )

    async def import_url(
        self,
        url: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> MediaCreated:
        """Shortcut for ``create(url=...)``."""
        return await self.create(url=url, idempotency_key=idempotency_key, timeout=timeout, max_retries=max_retries, extra_headers=extra_headers)

    async def upload(
        self,
        file: bytes | IO[bytes],
        *,
        filename: str,
        mime_type: str,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> Media:
        """Uploads a file (up to 5 GB): announces it, then sends the bytes. Returns the stored file.

        ``file`` is ``bytes`` or a binary file object, e.g. ``open("teaser.mp4", "rb")``.
        """
        content = file if isinstance(file, (bytes, bytearray)) else file.read()
        created = await self.create(
            filename=filename,
            mimeType=mime_type,  # type: ignore[arg-type]
            sizeBytes=len(content),
            idempotency_key=idempotency_key,
            timeout=timeout,
        )
        upload = created.get("upload")
        if not upload:
            raise FeedHorizonError("The API did not return an upload URL.")
        response = await self._client._http.request(
            "PUT", upload["url"], content=content, headers=upload["headers"], timeout=timeout or max(self._client.timeout, 600.0)
        )
        if response.is_error:
            raise FeedHorizonError(f"Upload of {filename} failed with HTTP {response.status_code}")
        media = {k: v for k, v in created.items() if k != "upload"}
        return media  # type: ignore[return-value]

    async def delete(
        self,
        media_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Deleted:
        """Deletes a file no post uses. Raises ``ConflictError`` (``media_in_use``) otherwise."""
        return await self._client._data(
            "DELETE",
            f"/media/{_id(media_id)}",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )


class AsyncProfileQueue(_AsyncResource):
    """The weekly posting times of a profile."""

    async def get(
        self,
        profile_id: str,
        *,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Queue:
        return await self._client._data(
            "GET", f"/profiles/{_id(profile_id)}/queue", timeout=timeout, max_retries=max_retries, headers=extra_headers
        )

    async def set(
        self,
        profile_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
        **params: Unpack[QueueSetParams],
    ) -> Queue:
        """Replaces all slots. ``reshuffle=True`` moves queued posts to the new times."""
        return await self._client._data(
            "PUT",
            f"/profiles/{_id(profile_id)}/queue",
            body=params,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def slots(
        self,
        profile_id: str,
        *,
        count: int | None = None,
        free: bool | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> QueueSlots:
        """The next slots with the post that holds each one. ``free=True`` lists only open slots."""
        return await self._client._data(
            "GET",
            f"/profiles/{_id(profile_id)}/queue/slots",
            query={"count": count, "free": free},
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )


class AsyncProfiles(_AsyncResource):
    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.queue = AsyncProfileQueue(client)

    def list(
        self,
        *,
        externalId: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> AsyncPager[Profile]:
        """Lists profiles. ``externalId`` finds the profile of one of your customers."""
        return self._client._list("/profiles", {"externalId": externalId}, timeout=timeout, max_retries=max_retries, headers=extra_headers)

    async def get(
        self,
        profile_id: str,
        *,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Profile:
        return await self._client._data("GET", f"/profiles/{_id(profile_id)}", timeout=timeout, max_retries=max_retries, headers=extra_headers)

    async def create(
        self,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
        **params: Unpack[ProfileCreateParams],
    ) -> Profile:
        return await self._client._data(
            "POST",
            "/profiles",
            body=params,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def update(
        self,
        profile_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
        **params: Unpack[ProfileUpdateParams],
    ) -> Profile:
        return await self._client._data(
            "PATCH",
            f"/profiles/{_id(profile_id)}",
            body=params,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def delete(
        self,
        profile_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Deleted:
        """Deletes the profile with its accounts, posts and queue."""
        return await self._client._data(
            "DELETE",
            f"/profiles/{_id(profile_id)}",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )


class AsyncAccounts(_AsyncResource):
    def list(
        self,
        *,
        profileId: str | None = None,
        platform: PlatformId | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> AsyncPager[Account]:
        return self._client._list(
            "/accounts", {"profileId": profileId, "platform": platform}, timeout=timeout, max_retries=max_retries, headers=extra_headers
        )

    async def get(
        self,
        account_id: str,
        *,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Account:
        return await self._client._data("GET", f"/accounts/{_id(account_id)}", timeout=timeout, max_retries=max_retries, headers=extra_headers)

    async def delete(
        self,
        account_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Deleted:
        """Disconnects the account. Its scheduled posts are deleted with it."""
        return await self._client._data(
            "DELETE",
            f"/accounts/{_id(account_id)}",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def boards(
        self,
        account_id: str,
        *,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> PinterestBoardList:
        """The boards of a Pinterest account, for ``targets[].options.pinterest.boardId``."""
        return await self._client._data(
            "GET", f"/accounts/{_id(account_id)}/boards", timeout=timeout, max_retries=max_retries, headers=extra_headers
        )

    async def tiktok_creator(
        self,
        account_id: str,
        *,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> TikTokCreatorInfo:
        """What a TikTok account may post, for ``targets[].options.tiktok``."""
        return await self._client._data(
            "GET", f"/accounts/{_id(account_id)}/tiktok-creator", timeout=timeout, max_retries=max_retries, headers=extra_headers
        )


class AsyncPlatforms(_AsyncResource):
    def list(
        self, *, timeout: float | None = None, max_retries: int | None = None, extra_headers: Mapping[str, str] | None = None
    ) -> AsyncPager[Platform]:
        """Every platform with its limits: text length, media types and counts."""
        return self._client._list("/platforms", None, timeout=timeout, max_retries=max_retries, headers=extra_headers)

    async def get(
        self,
        platform: PlatformId,
        *,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Platform:
        return await self._client._data("GET", f"/platforms/{_id(platform)}", timeout=timeout, max_retries=max_retries, headers=extra_headers)


class AsyncPlatformInvites(_AsyncResource):
    """Connect links: let a customer connect their account to one of your profiles."""

    def list(
        self,
        *,
        profileId: str,
        platform: PlatformId | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> AsyncPager[PlatformInvite]:
        return self._client._list(
            "/platform-invites",
            {"profileId": profileId, "platform": platform},
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def create(
        self,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
        **params: Unpack[PlatformInviteCreateParams],
    ) -> PlatformInviteCreated:
        """Creates a link for one profile and platform. ``inviteUrl`` is returned only here."""
        return await self._client._data(
            "POST",
            "/platform-invites",
            body=params,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def delete(
        self,
        invite_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Deleted:
        """Revokes a link."""
        return await self._client._data(
            "DELETE",
            f"/platform-invites/{_id(invite_id)}",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )


class AsyncWebhooks(_AsyncResource):
    """Webhook endpoints. To check incoming deliveries, use ``feedhorizon.verify_webhook`` / ``construct_webhook_event``."""

    def list(
        self, *, timeout: float | None = None, max_retries: int | None = None, extra_headers: Mapping[str, str] | None = None
    ) -> AsyncPager[Webhook]:
        return self._client._list("/webhooks", None, timeout=timeout, max_retries=max_retries, headers=extra_headers)

    async def get(
        self,
        webhook_id: str,
        *,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Webhook:
        return await self._client._data("GET", f"/webhooks/{_id(webhook_id)}", timeout=timeout, max_retries=max_retries, headers=extra_headers)

    async def create(
        self,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
        **params: Unpack[WebhookCreateParams],
    ) -> WebhookCreated:
        """Creates an endpoint. The answer holds the signing ``secret``, shown only once."""
        return await self._client._data(
            "POST",
            "/webhooks",
            body=params,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def update(
        self,
        webhook_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
        **params: Unpack[WebhookUpdateParams],
    ) -> Webhook:
        return await self._client._data(
            "PATCH",
            f"/webhooks/{_id(webhook_id)}",
            body=params,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def delete(
        self,
        webhook_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Deleted:
        return await self._client._data(
            "DELETE",
            f"/webhooks/{_id(webhook_id)}",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def test(
        self,
        webhook_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> WebhookTestResult:
        """Sends a signed ``webhook.test`` event to the endpoint."""
        return await self._client._data(
            "POST",
            f"/webhooks/{_id(webhook_id)}/test",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )


class AsyncApiKeys(_AsyncResource):
    def list(
        self, *, timeout: float | None = None, max_retries: int | None = None, extra_headers: Mapping[str, str] | None = None
    ) -> AsyncPager[ApiKey]:
        return self._client._list("/api-keys", None, timeout=timeout, max_retries=max_retries, headers=extra_headers)

    async def create(
        self,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
        **params: Unpack[ApiKeyCreateParams],
    ) -> ApiKeyCreated:
        """Creates a key. The answer holds the full ``key``, shown only once."""
        return await self._client._data(
            "POST",
            "/api-keys",
            body=params,
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )

    async def delete(
        self,
        key_id: str,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        extra_headers: Mapping[str, str] | None = None,
    ) -> Deleted:
        """Revokes a key at once."""
        return await self._client._data(
            "DELETE",
            f"/api-keys/{_id(key_id)}",
            idempotency_key=idempotency_key,
            timeout=timeout,
            max_retries=max_retries,
            headers=extra_headers,
        )


__all__ = ["AsyncPosts", "AsyncMediaResource", "AsyncProfiles", "AsyncProfileQueue", "AsyncAccounts", "AsyncPlatforms", "AsyncPlatformInvites", "AsyncWebhooks", "AsyncApiKeys"]
