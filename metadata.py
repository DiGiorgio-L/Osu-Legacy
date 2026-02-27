from pathlib import Path
import sys

# Ensure the local enfocate package (enfocate-core-lib/src) is importable
root = Path(__file__).resolve().parents[1]
pkg_src = root / "enfocate-core-lib" / "src"
if str(pkg_src) not in sys.path:
    sys.path.insert(0, str(pkg_src))

from enfocate.metadata import GameMetadata  # type: ignore

__all__ = ["GameMetadata"]
