from __future__ import annotations

from collections.abc import Mapping

import httpx

from ._async_resources import (
    AsyncAccounts,
    AsyncApiKeys,
    AsyncMediaResource,
    AsyncPlatformInvites,
    AsyncPlatforms,
    AsyncPosts,
    AsyncProfiles,
    AsyncWebhooks,
)
from ._client import DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT, AsyncAPIClient, SyncAPIClient
from ._resources import Accounts, ApiKeys, MediaResource, PlatformInvites, Platforms, Posts, Profiles, Webhooks
from .types import Me


class FeedHorizon(SyncAPIClient):
    """The FeedHorizon API client.

    >>> from feedhorizon import FeedHorizon
    >>> client = FeedHorizon()  # reads FEEDHORIZON_API_KEY
    >>> post = client.posts.create(profileId="prof_…", content="Hello", platforms=["linkedin"], publishNow=True)

    :param api_key: Your API key (``fh_…``). Defaults to ``FEEDHORIZON_API_KEY``.
    :param base_url: Defaults to ``FEEDHORIZON_BASE_URL`` or ``https://feedhorizon.com/api/v1``.
    :param timeout: Seconds before a request is aborted. Default 60.
    :param max_retries: Retries after network errors, 408, 409 in-progress, 429 and 5xx. Default 2.
    :param default_headers: Headers sent with every request.
    :param http_client: Your own ``httpx.Client``, e.g. for proxies.
    """

    posts: Posts
    media: MediaResource
    profiles: Profiles
    accounts: Accounts
    platforms: Platforms
    platform_invites: PlatformInvites
    webhooks: Webhooks
    api_keys: ApiKeys

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
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            http_client=http_client,
        )
        self.posts = Posts(self)
        self.media = MediaResource(self)
        self.profiles = Profiles(self)
        self.accounts = Accounts(self)
        self.platforms = Platforms(self)
        self.platform_invites = PlatformInvites(self)
        self.webhooks = Webhooks(self)
        self.api_keys = ApiKeys(self)

    def me(self, *, timeout: float | None = None) -> Me:
        """The organization, plan, rate limit and scopes of this key."""
        return self._data("GET", "/me", timeout=timeout)


class AsyncFeedHorizon(AsyncAPIClient):
    """The FeedHorizon API client for asyncio. Same methods as ``FeedHorizon``, awaited.

    >>> client = AsyncFeedHorizon()
    >>> post = await client.posts.get("post_…")
    >>> async for post in client.posts.list(status="failed"):
    ...     print(post["id"])
    """

    posts: AsyncPosts
    media: AsyncMediaResource
    profiles: AsyncProfiles
    accounts: AsyncAccounts
    platforms: AsyncPlatforms
    platform_invites: AsyncPlatformInvites
    webhooks: AsyncWebhooks
    api_keys: AsyncApiKeys

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
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            http_client=http_client,
        )
        self.posts = AsyncPosts(self)
        self.media = AsyncMediaResource(self)
        self.profiles = AsyncProfiles(self)
        self.accounts = AsyncAccounts(self)
        self.platforms = AsyncPlatforms(self)
        self.platform_invites = AsyncPlatformInvites(self)
        self.webhooks = AsyncWebhooks(self)
        self.api_keys = AsyncApiKeys(self)

    async def me(self, *, timeout: float | None = None) -> Me:
        """The organization, plan, rate limit and scopes of this key."""
        return await self._data("GET", "/me", timeout=timeout)
