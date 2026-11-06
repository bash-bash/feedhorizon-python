import re
from pathlib import Path

import feedhorizon


def test_version_matches_pyproject() -> None:
    text = (Path(__file__).parent.parent / "pyproject.toml").read_text()
    match = re.search(r'^version = "([^"]+)"', text, re.M)
    assert match and feedhorizon.__version__ == match.group(1)
