"""Types of the FeedHorizon API. Generated from spec/openapi.json by scripts/generate_types.py; do not edit."""

from __future__ import annotations

from typing import Any, Literal, Union

from typing_extensions import NotRequired, TypedDict

class Account(TypedDict):
    """A connected social account."""

    id: str
    """Account id"""
    profileId: str
    """Profile id"""
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""
    platformAccountId: str
    """The account's id on the platform"""
    displayName: str | None
    username: str | None
    avatarUrl: str | None
    status: Literal["active", "needs_reauth", "revoked"]
    """needs_reauth: the platform ended the connection; posts to it fail until the customer reconnects"""
    tokenExpiresAt: str | None
    """When the current platform token runs out. FeedHorizon refreshes it ahead of time where the platform allows; otherwise account.expiring is sent 7 days before"""
    createdAt: str
    """ISO 8601 timestamp"""

class ApiKey(TypedDict):
    id: str
    """API key id"""
    keyPrefix: str
    name: str
    permission: Literal["readwrite", "readonly"]
    """Summary of scopes: readwrite when any write scope is granted"""
    scopes: list[Literal["profiles:read", "profiles:write", "accounts:read", "accounts:write", "posts:read", "posts:write", "webhooks:read", "webhooks:write", "api_keys:read", "api_keys:write", "platform_invites:read", "platform_invites:write"]]
    fullAccess: bool
    """true = all profiles, including future ones"""
    profileIds: list[str]
    lastUsedAt: str | None
    expiresAt: str | None
    createdAt: str
    """ISO 8601 timestamp"""

class MeOrganization(TypedDict):
    id: str
    """Organization id"""
    name: str

class MeRateLimit(TypedDict):
    limit: int
    """Requests per minute for this key"""
    windowSeconds: int

class MeApiKey(TypedDict):
    id: str
    """API key id"""
    name: str
    keyPrefix: str
    scopes: list[Literal["profiles:read", "profiles:write", "accounts:read", "accounts:write", "posts:read", "posts:write", "webhooks:read", "webhooks:write", "api_keys:read", "api_keys:write", "platform_invites:read", "platform_invites:write"]]
    fullAccess: bool
    """true = all profiles, including future ones"""
    profileIds: list[str]
    """Profiles the key may use; empty when fullAccess is true"""
    expiresAt: str | None

class Me(TypedDict):
    organization: MeOrganization
    plan: str
    """Active plan of the organization: free or paid (older subscriptions: build, accelerate or unlimited)"""
    rateLimit: MeRateLimit
    apiKey: MeApiKey
    serverTime: str
    """Current time on the server, UTC"""

class Media(TypedDict):
    """A file that posts can use through mediaIds."""

    id: str
    """Media id"""
    url: str
    """Public URL of the file"""
    filename: str
    mimeType: str
    sizeBytes: int
    createdAt: str
    """ISO 8601 timestamp"""

class MediaCreatedUpload(TypedDict):
    url: str
    """PUT the file bytes here"""
    method: Literal["PUT"]
    headers: dict[str, str]
    """Send these headers with the upload"""
    expiresAt: str
    """ISO 8601 timestamp"""

class MediaCreated(TypedDict):
    id: str
    """Media id"""
    url: str
    """Public URL of the file"""
    filename: str
    mimeType: str
    sizeBytes: int
    createdAt: str
    """ISO 8601 timestamp"""
    upload: MediaCreatedUpload | None
    """Only for uploads; null for imports, which are stored already"""

class PinterestBoardListDataItem(TypedDict):
    boardId: str
    """Pinterest board id"""
    name: str
    privacy: str | None

class PinterestBoardList(TypedDict):
    data: list[PinterestBoardListDataItem]

class Platform(TypedDict):
    """What a platform accepts."""

    id: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""
    name: str
    available: bool
    """true when accounts can be connected and posts published today"""
    maxTextLength: int
    """Characters per post"""
    maxMediaCount: int
    """Media items per post"""
    supportedMediaTypes: list[str]
    """MIME types accepted for media"""

class PlatformInvite(TypedDict):
    id: str
    """Invite id"""
    profileId: str
    """Profile id"""
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""
    createdAt: str
    """ISO 8601 timestamp"""
    expiresAt: str
    """ISO 8601 timestamp"""
    usedAt: str | None

class PlatformInviteCreated(TypedDict):
    id: str
    """Invite id"""
    profileId: str
    """Profile id"""
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""
    createdAt: str
    """ISO 8601 timestamp"""
    expiresAt: str
    """ISO 8601 timestamp"""
    inviteUrl: str

class Post(TypedDict):
    id: str
    """Post id"""
    profileId: str
    """Profile id"""
    content: str | None
    status: Literal["draft", "scheduled", "publishing", "published", "partially_failed", "failed"]
    source: Literal["ui", "api", "queue"]
    scheduledAt: str | None
    timezone: str
    publishedAt: str | None
    idempotencyKey: str | None
    createdAt: str
    """ISO 8601 timestamp"""
    updatedAt: str
    """ISO 8601 timestamp"""
    targets: list[PostTarget]
    media: list[PostMedia]

class PostIssue(TypedDict):
    code: str
    """Stable, e.g. content_too_long, media_required, schedule_in_past"""
    message: str
    param: str | None
    """Request field it is about, e.g. targets.1.content"""
    accountId: str | None
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"] | None

class PostMedia(TypedDict):
    id: str
    """Media id"""
    url: str
    mimeType: str
    filename: str
    sizeBytes: int

class PostTargetError(TypedDict):
    code: str | None
    """Stable, e.g. account_needs_reauth, platform_rejected, platform_rate_limited"""
    category: Literal["auth_expired", "rate_limited", "rejected", "platform_error", "timeout", "unknown"]
    """What kind of failure, to react without parsing the message"""
    source: Literal["user", "platform", "system"]
    """Who can fix it: user (you or your customer), platform (wait and retry), system (FeedHorizon)"""
    message: str
    """For humans, usually the platform's own reason"""

class PostTarget(TypedDict):
    """The post on exactly one social account, with its own status."""

    id: str
    """Post target id"""
    socialAccountId: str
    """Account id"""
    accountName: str | None
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""
    content: str | None
    """Own text for this account. null means the post content is used"""
    options: PostTargetOptions | None
    status: Literal["draft", "scheduled", "publishing", "published", "failed", "cancelled"]
    attempts: int
    scheduledAt: str | None
    publishedAt: str | None
    platformPostId: str | None
    """Id of the post on the platform"""
    platformUrl: str | None
    """Link to the live post"""
    error: PostTargetError | None
    """Why publishing to this account failed; null unless status is failed"""

class PostTargetInput(TypedDict):
    """One account to publish to, optionally with its own text."""

    accountId: str
    """Account id"""
    content: NotRequired[str | None]
    """Own text for this account. Leave out to use the post content"""
    options: NotRequired[PostTargetOptions]

class PostTargetOptionsPinterest(TypedDict):
    boardId: NotRequired[str]
    """Board to pin to, from GET /accounts/{id}/boards. Default: the first board of the account"""
    title: NotRequired[str]
    """Pin title. Default: the first line of the text"""
    link: NotRequired[str]
    """Where the Pin leads when clicked"""

class PostTargetOptionsTiktok(TypedDict):
    privacyLevel: Literal["PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS", "FOLLOWER_OF_CREATOR", "SELF_ONLY"]
    """Required. Must be one of the account's privacyLevelOptions from GET /accounts/{id}/tiktok-creator"""
    allowComment: NotRequired[bool]
    """Default false"""
    allowDuet: NotRequired[bool]
    """Default false"""
    allowStitch: NotRequired[bool]
    """Default false"""
    brandOrganic: NotRequired[bool]
    """Promotes your own business; labelled "Promotional content\""""
    brandedContent: NotRequired[bool]
    """Paid partnership with another brand; labelled "Paid partnership". Not allowed with SELF_ONLY"""
    aiGenerated: NotRequired[bool]
    """The video is AI-generated"""

class PostTargetOptions(TypedDict):
    """Platform settings for one account. Only the key of that account's platform is used."""

    pinterest: NotRequired[PostTargetOptionsPinterest]
    tiktok: NotRequired[PostTargetOptionsTiktok]

class PostValidationTargetsItem(TypedDict):
    accountId: str
    """Account id"""
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""

class PostValidation(TypedDict):
    valid: bool
    """true when creating this post would succeed"""
    errors: list[PostIssue]
    """Problems that make creating the post fail"""
    warnings: list[PostIssue]
    """Things that may still make publishing fail later, e.g. an account that must reconnect"""
    scheduledAt: str | None
    """When the post would go out (the queue slot for addToQueue)"""
    targets: list[PostValidationTargetsItem]
    """The accounts the post would go to"""

class Profile(TypedDict):
    """A brand or client inside your organization. Accounts and posts belong to a profile."""

    id: str
    """Profile id"""
    name: str
    color: str
    timezone: str
    isDefault: bool
    queueEnabled: bool
    externalId: str | None
    createdAt: str
    """ISO 8601 timestamp"""
    updatedAt: str
    """ISO 8601 timestamp"""

class Queue(TypedDict):
    """Weekly posting times of a profile. Posts created with addToQueue take the next free slot."""

    profileId: str
    """Profile id"""
    enabled: bool
    """When false, addToQueue is refused"""
    timezone: str
    """Time zone of the slots (the profile time zone)"""
    slots: list[QueueSlot]

class QueueSlot(TypedDict):
    dayOfWeek: int
    """0 = Sunday, 6 = Saturday"""
    time: str
    """Local time HH:MM in the queue's time zone"""

class QueueSlotsSlotsItem(TypedDict):
    at: str
    """ISO 8601 timestamp"""
    postId: str | None
    postContent: str | None
    """Start of the post text, for display"""

class QueueSlots(TypedDict):
    slots: list[QueueSlotsSlotsItem]

class TikTokCreatorInfo(TypedDict):
    creatorUsername: str | None
    creatorNickname: str | None
    creatorAvatarUrl: str | None
    privacyLevelOptions: list[Literal["PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS", "FOLLOWER_OF_CREATOR", "SELF_ONLY"]]
    commentDisabled: bool
    duetDisabled: bool
    stitchDisabled: bool
    maxVideoPostDurationSec: int | None

class Webhook(TypedDict):
    id: str
    """Webhook id"""
    name: str
    url: str
    events: list[str]
    isActive: bool
    failCount: int
    lastFiredAt: str | None
    customHeaders: dict[str, str] | None
    createdAt: str
    """ISO 8601 timestamp"""
    updatedAt: str
    """ISO 8601 timestamp"""

class WebhookTestResult(TypedDict):
    delivered: bool
    statusCode: int | None
    error: str | None

class ErrorErrorDetailsItem(TypedDict):
    param: NotRequired[str]
    code: NotRequired[str]
    """Stable code of this problem, e.g. content_too_long. Set on post checks."""
    message: str

class ErrorError(TypedDict):
    type: Literal["invalid_request_error", "authentication_error", "permission_error", "not_found_error", "conflict_error", "idempotency_error", "rate_limit_error", "api_error"]
    """Error class. Stable, safe to branch on."""
    code: str
    """Machine-readable code such as validation_failed. Stable."""
    message: str
    """For humans. May be reworded, never branch on it."""
    param: NotRequired[str]
    """The field or parameter at fault, dotted when nested."""
    details: NotRequired[list[ErrorErrorDetailsItem]]
    docUrl: str
    requestId: str
    """Quote it when you contact support."""

class Error(TypedDict):
    error: ErrorError

PostListParams = TypedDict("PostListParams", {"profileId": "NotRequired[str]", "status": "NotRequired[Literal[\"draft\", \"scheduled\", \"publishing\", \"published\", \"partially_failed\", \"failed\"]]", "platform": "NotRequired[Literal[\"twitter\", \"linkedin\", \"instagram\", \"facebook\", \"tiktok\", \"youtube\", \"threads\", \"bluesky\", \"pinterest\"]]", "from": "NotRequired[str]", "to": "NotRequired[str]", "updatedSince": "NotRequired[str]", "limit": "NotRequired[int]", "cursor": "NotRequired[str]"})

class PostCreateParams(TypedDict):
    """Parameters of `POST /posts`."""

    profileId: str
    """Profile id"""
    content: NotRequired[str]
    """Post text. Each account can get its own text through targets"""
    platforms: NotRequired[list[Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]]]
    """Publish to every active account of these platforms in the profile"""
    accountIds: NotRequired[list[str]]
    """Or name the accounts explicitly (wins over platforms)"""
    targets: NotRequired[list[PostTargetInput]]
    """The accounts to publish to, each with optional own text. Wins over platforms and accountIds"""
    mediaIds: NotRequired[list[str]]
    """Files from POST /media, in display order"""
    scheduledFor: NotRequired[str]
    """Schedule for this time. Leave out all three timing fields for a draft"""
    publishNow: NotRequired[Literal[True]]
    """Publish right away"""
    addToQueue: NotRequired[Literal[True]]
    """Take the profile's next free queue slot"""
    timezone: NotRequired[str]
    """Time zone shown with the post. Defaults to the profile's"""

class PostValidateParams(TypedDict):
    """Parameters of `POST /posts/validate`."""

    profileId: str
    """Profile id"""
    content: NotRequired[str]
    """Post text. Each account can get its own text through targets"""
    platforms: NotRequired[list[Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]]]
    """Publish to every active account of these platforms in the profile"""
    accountIds: NotRequired[list[str]]
    """Or name the accounts explicitly (wins over platforms)"""
    targets: NotRequired[list[PostTargetInput]]
    """The accounts to publish to, each with optional own text. Wins over platforms and accountIds"""
    mediaIds: NotRequired[list[str]]
    """Files from POST /media, in display order"""
    scheduledFor: NotRequired[str]
    """Schedule for this time. Leave out all three timing fields for a draft"""
    publishNow: NotRequired[Literal[True]]
    """Publish right away"""
    addToQueue: NotRequired[Literal[True]]
    """Take the profile's next free queue slot"""
    timezone: NotRequired[str]
    """Time zone shown with the post. Defaults to the profile's"""

class PostUpdateParams(TypedDict):
    """Parameters of `PATCH /posts/{id}`."""

    content: NotRequired[str | None]
    platforms: NotRequired[list[Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]]]
    accountIds: NotRequired[list[str]]
    targets: NotRequired[list[PostTargetInput]]
    """The accounts to publish to, each with optional own text. Wins over platforms and accountIds"""
    mediaIds: NotRequired[list[str]]
    """Replaces the media of the post; [] removes all"""
    scheduledFor: NotRequired[str | None]
    timezone: NotRequired[str]
    """IANA time zone, e.g. Europe/Berlin"""

class MediaListParams(TypedDict):
    """Parameters of `GET /media`."""

    limit: NotRequired[int]
    """Items per page, 1 to 100"""
    cursor: NotRequired[str]
    """nextCursor from the previous page"""

class MediaCreateParams(TypedDict):
    """Parameters of `POST /media`."""

    url: NotRequired[str]
    """Import this public https URL"""
    filename: NotRequired[str]
    """File name, required for uploads"""
    mimeType: NotRequired[Literal["image/jpeg", "image/png", "image/gif", "image/webp", "video/mp4", "video/quicktime", "video/webm", "application/pdf"]]
    """Required for uploads"""
    sizeBytes: NotRequired[int]
    """Required for uploads"""

class ProfileListParams(TypedDict):
    """Parameters of `GET /profiles`."""

    externalId: NotRequired[str]
    """Your own id for this object, e.g. your customer id. Unique per organization"""

class ProfileCreateParams(TypedDict):
    """Parameters of `POST /profiles`."""

    name: str
    color: NotRequired[str]
    timezone: NotRequired[str]
    """IANA time zone, e.g. Europe/Berlin"""
    externalId: NotRequired[str]
    """Your own id for this object, e.g. your customer id. Unique per organization"""

class ProfileUpdateParams(TypedDict):
    """Parameters of `PATCH /profiles/{id}`."""

    name: NotRequired[str]
    color: NotRequired[str]
    timezone: NotRequired[str]
    """IANA time zone, e.g. Europe/Berlin"""
    isDefault: NotRequired[Literal[True]]
    queueEnabled: NotRequired[bool]
    externalId: NotRequired[str | None]
    """Your own id for this profile. null removes it"""

class QueueSetParams(TypedDict):
    """Parameters of `PUT /profiles/{id}/queue`."""

    slots: list[QueueSlot]
    timezone: NotRequired[str]
    """IANA time zone, e.g. Europe/Berlin"""
    enabled: NotRequired[bool]
    reshuffle: NotRequired[bool]
    """Move queued posts to the new slots"""

class QueueSlotsParams(TypedDict):
    """Parameters of `GET /profiles/{id}/queue/slots`."""

    count: NotRequired[int]
    """How many slots, 1 to 100"""
    free: NotRequired[Literal["true", "false"]]
    """true lists only free slots"""

class AccountListParams(TypedDict):
    """Parameters of `GET /accounts`."""

    profileId: NotRequired[str]
    """Only accounts of this profile"""
    platform: NotRequired[Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""

class PlatformInviteListParams(TypedDict):
    """Parameters of `GET /platform-invites`."""

    profileId: str
    """Profile id"""
    platform: NotRequired[Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""

class PlatformInviteCreateParams(TypedDict):
    """Parameters of `POST /platform-invites`."""

    profileId: str
    """Profile id"""
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""

class WebhookCreateParams(TypedDict):
    """Parameters of `POST /webhooks`."""

    url: str
    events: list[Literal["post.scheduled", "post.published", "post.failed", "post.partial", "post.updated", "post.deleted", "account.connected", "account.disconnected", "account.expiring", "account.needs_reauth", "post.target.published", "post.target.failed"]]
    name: NotRequired[str]
    secret: NotRequired[str]
    """Your own signing secret. Generated when left out"""
    isActive: NotRequired[bool]
    customHeaders: NotRequired[dict[str, str]]
    """Extra headers sent with every delivery, e.g. for your own auth"""

class WebhookUpdateParams(TypedDict):
    """Parameters of `PATCH /webhooks/{id}`."""

    url: NotRequired[str]
    events: NotRequired[list[Literal["post.scheduled", "post.published", "post.failed", "post.partial", "post.updated", "post.deleted", "account.connected", "account.disconnected", "account.expiring", "account.needs_reauth", "post.target.published", "post.target.failed"]]]
    name: NotRequired[str]
    isActive: NotRequired[bool]
    customHeaders: NotRequired[dict[str, str] | None]

class ApiKeyCreateParams(TypedDict):
    """Parameters of `POST /api-keys`."""

    name: str
    scopes: NotRequired[list[Literal["profiles:read", "profiles:write", "accounts:read", "accounts:write", "posts:read", "posts:write", "webhooks:read", "webhooks:write", "api_keys:read", "api_keys:write", "platform_invites:read", "platform_invites:write"]]]
    """Rights of the key. Wins over permission"""
    permission: NotRequired[Literal["readwrite", "readonly"]]
    """Shorthand used when scopes is left out"""
    fullAccess: NotRequired[bool]
    """true = all profiles, including future ones"""
    profileIds: NotRequired[list[str]]
    """Profiles the key may use when fullAccess is false"""
    expiresAt: NotRequired[str]
    """ISO 8601 timestamp"""

class WebhookCreated(TypedDict):
    id: str
    """Webhook id"""
    name: str
    url: str
    events: list[str]
    isActive: bool
    failCount: int
    lastFiredAt: str | None
    customHeaders: dict[str, str] | None
    createdAt: str
    """ISO 8601 timestamp"""
    updatedAt: str
    """ISO 8601 timestamp"""
    secret: str
    """Signing secret, shown only once"""

class ApiKeyCreated(TypedDict):
    id: str
    """API key id"""
    keyPrefix: str
    name: str
    permission: Literal["readwrite", "readonly"]
    """Summary of scopes: readwrite when any write scope is granted"""
    scopes: list[Literal["profiles:read", "profiles:write", "accounts:read", "accounts:write", "posts:read", "posts:write", "webhooks:read", "webhooks:write", "api_keys:read", "api_keys:write", "platform_invites:read", "platform_invites:write"]]
    fullAccess: bool
    """true = all profiles, including future ones"""
    profileIds: list[str]
    lastUsedAt: str | None
    expiresAt: str | None
    createdAt: str
    """ISO 8601 timestamp"""
    key: str
    """The secret key, shown only once"""

class PostScheduledEventData(TypedDict):
    postId: str
    """Post id"""
    profileId: str
    """Profile id"""
    scheduledAt: str | None
    platforms: list[Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]]
    """Platforms of the accounts it goes to"""

class PostScheduledEvent(TypedDict):
    """A post was scheduled. Sent when a post is created with a time or in the queue, or a draft gets scheduled."""

    id: str
    """Event id, the same on every retry. Use it to drop duplicates"""
    event: Literal["post.scheduled"]
    timestamp: str
    """When the event happened (ISO 8601, UTC)"""
    data: PostScheduledEventData

class PostPublishedEventDataTargetsItemError(TypedDict):
    code: str | None
    """See Publishing errors"""
    category: Literal["auth_expired", "rate_limited", "rejected", "platform_error", "timeout", "unknown"]
    source: Literal["user", "platform", "system"]
    """Who can fix it"""
    message: str

class PostPublishedEventDataTargetsItem(TypedDict):
    targetId: str
    """Target id: the post on this one account"""
    accountId: str
    """Account id"""
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""
    status: Literal["draft", "scheduled", "publishing", "published", "failed", "cancelled"]
    platformPostId: str | None
    """Id of the post on the platform"""
    platformUrl: str | None
    """Link to the live post"""
    error: PostPublishedEventDataTargetsItemError | None
    """Why this account failed; null unless status is failed"""

class PostPublishedEventData(TypedDict):
    postId: str
    """Post id"""
    profileId: str
    """Profile id"""
    status: Literal["draft", "scheduled", "publishing", "published", "partially_failed", "failed"]
    targets: list[PostPublishedEventDataTargetsItem]
    """One entry per account of the post"""

class PostPublishedEvent(TypedDict):
    """A post is published on all its accounts. Sent once every account of the post has published."""

    id: str
    """Event id, the same on every retry. Use it to drop duplicates"""
    event: Literal["post.published"]
    timestamp: str
    """When the event happened (ISO 8601, UTC)"""
    data: PostPublishedEventData

class PostFailedEventDataTargetsItemError(TypedDict):
    code: str | None
    """See Publishing errors"""
    category: Literal["auth_expired", "rate_limited", "rejected", "platform_error", "timeout", "unknown"]
    source: Literal["user", "platform", "system"]
    """Who can fix it"""
    message: str

class PostFailedEventDataTargetsItem(TypedDict):
    targetId: str
    """Target id: the post on this one account"""
    accountId: str
    """Account id"""
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""
    status: Literal["draft", "scheduled", "publishing", "published", "failed", "cancelled"]
    platformPostId: str | None
    """Id of the post on the platform"""
    platformUrl: str | None
    """Link to the live post"""
    error: PostFailedEventDataTargetsItemError | None
    """Why this account failed; null unless status is failed"""

class PostFailedEventData(TypedDict):
    postId: str
    """Post id"""
    profileId: str
    """Profile id"""
    status: Literal["draft", "scheduled", "publishing", "published", "partially_failed", "failed"]
    targets: list[PostFailedEventDataTargetsItem]
    """One entry per account of the post"""

class PostFailedEvent(TypedDict):
    """A post failed on all its accounts. Sent once every account is done and none published. `targets[].error` says why."""

    id: str
    """Event id, the same on every retry. Use it to drop duplicates"""
    event: Literal["post.failed"]
    timestamp: str
    """When the event happened (ISO 8601, UTC)"""
    data: PostFailedEventData

class PostPartialEventDataTargetsItemError(TypedDict):
    code: str | None
    """See Publishing errors"""
    category: Literal["auth_expired", "rate_limited", "rejected", "platform_error", "timeout", "unknown"]
    source: Literal["user", "platform", "system"]
    """Who can fix it"""
    message: str

class PostPartialEventDataTargetsItem(TypedDict):
    targetId: str
    """Target id: the post on this one account"""
    accountId: str
    """Account id"""
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""
    status: Literal["draft", "scheduled", "publishing", "published", "failed", "cancelled"]
    platformPostId: str | None
    """Id of the post on the platform"""
    platformUrl: str | None
    """Link to the live post"""
    error: PostPartialEventDataTargetsItemError | None
    """Why this account failed; null unless status is failed"""

class PostPartialEventData(TypedDict):
    postId: str
    """Post id"""
    profileId: str
    """Profile id"""
    status: Literal["draft", "scheduled", "publishing", "published", "partially_failed", "failed"]
    targets: list[PostPartialEventDataTargetsItem]
    """One entry per account of the post"""

class PostPartialEvent(TypedDict):
    """A post is published on some accounts and failed on others. Sent once every account is done and at least one failed. `targets[].error` says why."""

    id: str
    """Event id, the same on every retry. Use it to drop duplicates"""
    event: Literal["post.partial"]
    timestamp: str
    """When the event happened (ISO 8601, UTC)"""
    data: PostPartialEventData

PostUpdatedEventDataChangesValue = TypedDict("PostUpdatedEventDataChangesValue", {"from": "Any", "to": "Any"})

class PostUpdatedEventData(TypedDict):
    postId: str
    """Post id"""
    profileId: str
    """Profile id"""
    status: Literal["draft", "scheduled", "publishing", "published", "partially_failed", "failed"]
    scheduledAt: str | None
    platforms: list[Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]]
    changes: dict[str, PostUpdatedEventDataChangesValue]
    """One entry per changed field, with the value before (`from`) and after (`to`)"""

class PostUpdatedEvent(TypedDict):
    """A post was changed. Sent when the text, time, accounts or status of a post change through the API, the dashboard or MCP."""

    id: str
    """Event id, the same on every retry. Use it to drop duplicates"""
    event: Literal["post.updated"]
    timestamp: str
    """When the event happened (ISO 8601, UTC)"""
    data: PostUpdatedEventData

class PostDeletedEventData(TypedDict):
    postId: str
    """Post id"""
    profileId: str
    """Profile id"""
    status: Literal["draft", "scheduled", "publishing", "published", "partially_failed", "failed"]
    scheduledAt: str | None

class PostDeletedEvent(TypedDict):
    """A post was deleted. Sent when a post is deleted in FeedHorizon. Posts already live stay on the platforms."""

    id: str
    """Event id, the same on every retry. Use it to drop duplicates"""
    event: Literal["post.deleted"]
    timestamp: str
    """When the event happened (ISO 8601, UTC)"""
    data: PostDeletedEventData

class AccountConnectedEventData(TypedDict):
    accountId: str
    """Account id"""
    profileId: str
    """Profile id"""
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""
    displayName: str | None
    """Name of the account on the platform"""

class AccountConnectedEvent(TypedDict):
    """An account was connected. Sent when an account is connected in the dashboard or through a connect link, including reconnects."""

    id: str
    """Event id, the same on every retry. Use it to drop duplicates"""
    event: Literal["account.connected"]
    timestamp: str
    """When the event happened (ISO 8601, UTC)"""
    data: AccountConnectedEventData

class AccountDisconnectedEventData(TypedDict):
    accountId: str
    """Account id"""
    profileId: str
    """Profile id"""
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""

class AccountDisconnectedEvent(TypedDict):
    """An account was disconnected. Sent when an account is removed. Its scheduled posts on this account are deleted with it."""

    id: str
    """Event id, the same on every retry. Use it to drop duplicates"""
    event: Literal["account.disconnected"]
    timestamp: str
    """When the event happened (ISO 8601, UTC)"""
    data: AccountDisconnectedEventData

class AccountExpiringEventData(TypedDict):
    accountId: str
    """Account id"""
    profileId: str
    """Profile id"""
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""
    displayName: str | None
    """Name of the account on the platform"""
    expiresAt: str
    """When the connection ends"""

class AccountExpiringEvent(TypedDict):
    """An account connection runs out soon. Sent 7 days before a connection ends on platforms where FeedHorizon cannot renew it. Ask the owner to reconnect."""

    id: str
    """Event id, the same on every retry. Use it to drop duplicates"""
    event: Literal["account.expiring"]
    timestamp: str
    """When the event happened (ISO 8601, UTC)"""
    data: AccountExpiringEventData

class AccountNeedsReauthEventData(TypedDict):
    accountId: str
    """Account id"""
    profileId: str
    """Profile id"""
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""
    displayName: str | None
    """Name of the account on the platform"""
    reason: Literal["token_expired", "refresh_rejected"]
    """token_expired: the connection ran out; refresh_rejected: the platform refused to renew it"""

class AccountNeedsReauthEvent(TypedDict):
    """An account must be reconnected. Sent when the platform ended the connection. Posts to this account fail with `account_needs_reauth` until it is reconnected."""

    id: str
    """Event id, the same on every retry. Use it to drop duplicates"""
    event: Literal["account.needs_reauth"]
    timestamp: str
    """When the event happened (ISO 8601, UTC)"""
    data: AccountNeedsReauthEventData

class PostTargetPublishedEventDataError(TypedDict):
    code: str | None
    """See Publishing errors"""
    category: Literal["auth_expired", "rate_limited", "rejected", "platform_error", "timeout", "unknown"]
    source: Literal["user", "platform", "system"]
    """Who can fix it"""
    message: str

class PostTargetPublishedEventData(TypedDict):
    postId: str
    """Post id"""
    profileId: str
    """Profile id"""
    targetId: str
    """Target id: the post on this one account"""
    accountId: str
    """Account id"""
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""
    status: Literal["published", "failed"]
    platformPostId: str | None
    """Id of the post on the platform"""
    platformUrl: str | None
    """Link to the live post"""
    error: PostTargetPublishedEventDataError | None
    """Why this account failed; null unless status is failed"""

class PostTargetPublishedEvent(TypedDict):
    """A post is published on one account. Sent per account as soon as it is published, without waiting for the post's other accounts."""

    id: str
    """Event id, the same on every retry. Use it to drop duplicates"""
    event: Literal["post.target.published"]
    timestamp: str
    """When the event happened (ISO 8601, UTC)"""
    data: PostTargetPublishedEventData

class PostTargetFailedEventDataError(TypedDict):
    code: str | None
    """See Publishing errors"""
    category: Literal["auth_expired", "rate_limited", "rejected", "platform_error", "timeout", "unknown"]
    source: Literal["user", "platform", "system"]
    """Who can fix it"""
    message: str

class PostTargetFailedEventData(TypedDict):
    postId: str
    """Post id"""
    profileId: str
    """Profile id"""
    targetId: str
    """Target id: the post on this one account"""
    accountId: str
    """Account id"""
    platform: Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
    """Platform id. Publishing works on tiktok, instagram, linkedin, twitter, bluesky, pinterest today; the others are planned"""
    status: Literal["published", "failed"]
    platformPostId: str | None
    """Id of the post on the platform"""
    platformUrl: str | None
    """Link to the live post"""
    error: PostTargetFailedEventDataError | None
    """Why this account failed; null unless status is failed"""

class PostTargetFailedEvent(TypedDict):
    """A post failed on one account. Sent per account once it failed for good: after the last retry, or at once for errors that are not retried."""

    id: str
    """Event id, the same on every retry. Use it to drop duplicates"""
    event: Literal["post.target.failed"]
    timestamp: str
    """When the event happened (ISO 8601, UTC)"""
    data: PostTargetFailedEventData

WebhookEvent = Union[PostScheduledEvent, PostPublishedEvent, PostFailedEvent, PostPartialEvent, PostUpdatedEvent, PostDeletedEvent, AccountConnectedEvent, AccountDisconnectedEvent, AccountExpiringEvent, AccountNeedsReauthEvent, PostTargetPublishedEvent, PostTargetFailedEvent]
"""Any webhook event; check `event["event"]` to narrow it."""

WebhookEventName = Literal["post.scheduled", "post.published", "post.failed", "post.partial", "post.updated", "post.deleted", "account.connected", "account.disconnected", "account.expiring", "account.needs_reauth", "post.target.published", "post.target.failed"]

PlatformId = Literal["twitter", "linkedin", "instagram", "facebook", "tiktok", "youtube", "threads", "bluesky", "pinterest"]
