from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable, Generator, Iterator
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Page(Generic[T]):
    """One page of a list."""

    def __init__(self, data: list[T], next_cursor: str | None, fetch: Callable[[str], Page[T]]) -> None:
        self.data = data
        self.next_cursor = next_cursor
        self._fetch = fetch

    def has_next_page(self) -> bool:
        return self.next_cursor is not None

    def get_next_page(self) -> Page[T] | None:
        """The next page, or ``None`` after the last one."""
        return None if self.next_cursor is None else self._fetch(self.next_cursor)

    def iter_all(self) -> Iterator[T]:
        """Every item from this page on, fetching further pages as needed."""
        page: Page[T] | None = self
        while page is not None:
            yield from page.data
            page = page.get_next_page()

    def __iter__(self) -> Iterator[T]:
        return self.iter_all()

    def __repr__(self) -> str:
        return f"Page(data=[{len(self.data)} items], next_cursor={self.next_cursor!r})"


class AsyncPage(Generic[T]):
    """One page of a list, for the async client."""

    def __init__(self, data: list[T], next_cursor: str | None, fetch: Callable[[str], Awaitable[AsyncPage[T]]]) -> None:
        self.data = data
        self.next_cursor = next_cursor
        self._fetch = fetch

    def has_next_page(self) -> bool:
        return self.next_cursor is not None

    async def get_next_page(self) -> AsyncPage[T] | None:
        return None if self.next_cursor is None else await self._fetch(self.next_cursor)

    async def iter_all(self) -> AsyncIterator[T]:
        page: AsyncPage[T] | None = self
        while page is not None:
            for item in page.data:
                yield item
            page = await page.get_next_page()

    def __aiter__(self) -> AsyncIterator[T]:
        return self.iter_all()

    def __repr__(self) -> str:
        return f"AsyncPage(data=[{len(self.data)} items], next_cursor={self.next_cursor!r})"


class AsyncPager(Generic[T]):
    """What an async list call returns: ``await`` it for the first page, or ``async for`` over every item."""

    def __init__(self, load: Callable[[], Awaitable[AsyncPage[T]]]) -> None:
        self._load = load

    def __await__(self) -> Generator[Any, None, AsyncPage[T]]:
        return self._load().__await__()

    async def __aiter__(self) -> AsyncIterator[T]:
        page = await self._load()
        async for item in page.iter_all():
            yield item
