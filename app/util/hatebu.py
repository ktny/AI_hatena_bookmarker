import json
from typing import Any

import requests

read_entry_endpoint = "https://b.hatena.ne.jp/entry/jsonlite/"
bookmark_entry_endpoint = "https://bookmark.hatenaapis.com/rest/1/my/bookmark"


def read_entry(url: str):
    response = requests.get(read_entry_endpoint + url)
    return json.loads(response.text)


def bookmark_entry(session: Any, url: str, comment: str):
    return session.post(
        bookmark_entry_endpoint,
        params={"url": url, "comment": comment, "post_twitter": True},
    )
