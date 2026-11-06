"""Writes src/feedhorizon/_async_resources.py from _resources.py.

Run: python scripts/generate_async.py   (CI runs it with --check)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "feedhorizon" / "_resources.py"
OUT = ROOT / "src" / "feedhorizon" / "_async_resources.py"

CLASSES = [
    "_Resource",
    "Posts",
    "MediaResource",
    "ProfileQueue",
    "Profiles",
    "Accounts",
    "Platforms",
    "PlatformInvites",
    "Webhooks",
    "ApiKeys",
]


def convert(text: str) -> str:
    text = text.replace(
        '"""Sync resources. _async_resources.py is generated from this file by scripts/generate_async.py."""',
        '"""Async resources. Generated from _resources.py by scripts/generate_async.py; do not edit."""',
    )
    text = text.replace("from ._pagination import Page\n", "from ._pagination import AsyncPager\n")
    text = text.replace("from ._client import SyncAPIClient", "from ._client import AsyncAPIClient")
    text = text.replace("client: SyncAPIClient", "client: AsyncAPIClient")
    text = re.sub(r"\bPage\[", "AsyncPager[", text)
    for name in CLASSES:
        text = re.sub(rf"\b{name}\b", "_AsyncResource" if name == "_Resource" else f"Async{name}", text)
    # Every method except list() becomes a coroutine; list() returns an AsyncPager right away.
    text = re.sub(r"(\n    )def (?!list\b|__init__\b)(\w+)\(", r"\1async def \2(", text)
    text = text.replace("return self._client._data(", "return await self._client._data(")
    text = text.replace("return self.create(", "return await self.create(")
    text = text.replace("created = self.create(", "created = await self.create(")
    text = text.replace("response = self._client._http.request(", "response = await self._client._http.request(")
    return text


def main() -> None:
    text = convert(SRC.read_text())
    if "--check" in sys.argv:
        if OUT.read_text() != text:
            sys.exit(f"{OUT.relative_to(ROOT)} is out of date: run python scripts/generate_async.py")
        return
    OUT.write_text(text)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
