from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Entry:
    title: str
    count: int
    url: str
    entry_url: str
    screenshot: str
    eid: int
    bookmarks: list[Bookmark]


@dataclass
class Bookmark:
    user: str
    comment: str
    timestamp: datetime
