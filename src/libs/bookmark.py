import traceback

from libs.common import config
from libs.common.models import Entry
from libs.util import hatena
from libs.util.llm.chat import generate_comment, summarize_entry
from libs.util.parser import parse_bookmark_page

read_entry_endpoint = "https://b.hatena.ne.jp/entry/jsonlite/"
bookmark_entry_endpoint = "https://bookmark.hatenaapis.com/rest/1/my/bookmark"


def build_entry(url: str) -> Entry:
    """
    エントリ情報を構築する
    """
    entry = hatena.read_entry(url)

    if entry.entry_url is not None:
        bookmark_page_info = parse_bookmark_page(entry.entry_url)
        entry.popular_bookmarks = bookmark_page_info["popular"]
        entry.recent_bookmarks = bookmark_page_info["recent"]
        entry.category = bookmark_page_info["category"]

    entry.summary = summarize_entry(entry)

    return entry


def bookmark(url: str, comment: str | None = None) -> bool:
    """
    記事情報を元にブックマーク、スター付与などを行う
    """
    try:
        entry = build_entry(url)
        comment = generate_comment(entry)

        if config.dryrun:
            return True

        bookmarked = hatena.bookmark_entry(url, comment)

        if bookmarked is not None:
            try:
                hatena.add_star_to_best_bookmarker(entry)

            except Exception:
                print(traceback.format_exc())
        else:
            print("ブックマークに失敗しました")

        return True

    except Exception:
        print(traceback.format_exc())
        return False
