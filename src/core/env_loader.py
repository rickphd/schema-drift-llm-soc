"""Lightweight .env loader.

Walks up from the current working directory until it finds a ``.env`` file.
Keys already present in ``os.environ`` are NOT overridden — real env vars win.

Usage at the top of an entry script::

    from core.env_loader import load_env
    load_env()
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


def _find_env(start: Path, max_levels: int = 4) -> Optional[Path]:
    cur = start.resolve()
    for _ in range(max_levels + 1):
        candidate = cur / ".env"
        if candidate.is_file():
            return candidate
        if cur.parent == cur:
            return None
        cur = cur.parent
    return None


def load_env(start: Optional[Path] = None) -> Optional[Path]:
    """Load key=value lines from the nearest .env into os.environ.

    Returns the path that was loaded, or None if no .env was found.
    """
    origin = Path(start) if start else Path.cwd()
    env_path = _find_env(origin)
    if env_path is None:
        return None

    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key or key in os.environ:
            continue
        os.environ[key] = value

    return env_path
