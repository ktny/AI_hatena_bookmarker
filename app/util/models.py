from dataclasses import dataclass


@dataclass
class Entry:
    url: str
    title: str
    category: str
