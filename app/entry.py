from __future__ import annotations

import re
import sys

from chat import generate_comment, summarize
from config import AI_HATENA_USERNAME
from star import add_star_to_best_bookmarker
from util.hatebu import bookmark_entry, read_entry
from util.parser import parse_page
from util.session import create_hatena_session
from util.util import sanitize_filename

read_entry_endpoint = "https://b.hatena.ne.jp/entry/jsonlite/"
bookmark_entry_endpoint = "https://bookmark.hatenaapis.com/rest/1/my/bookmark"

cache_dir = "__cache__/"


def fix_comment(comment: str):
    sentences = comment.strip("。").split("。")
    result = ""
    for sentence in sentences:
        if len(result + sentence + "。") <= 100:
            result += sentence + "。"
        else:
            break

    result = result.replace("？。", "？").replace("！。", "！")
    match = re.match('^[「"](.+)[」"]。$', result)
    if match is not None:
        result = match.groups()[0]

    return result


def bookmark_by_gpt(url: str) -> bool:
    session = create_hatena_session()
    entry = read_entry(url) or {}

    entry["bookmarks"] = []

    try:
        entry["summary"] = _summary_url_page(url)
    except Exception as e:
        print(e)
        return False

    # print(f"タイトル: {entry['title']}\n")
    print(f"要約: {entry['summary']}\n")

    # ブックマーク済の場合はコメントしない
    if AI_HATENA_USERNAME in [bookmark["user"] for bookmark in entry.get("bookmarks")]:
        return False

    comment = fix_comment(generate_comment(entry))
    if comment:
        print(f"コメント: {comment}\n")
        add_star_to_best_bookmarker(url)
        res = bookmark_entry(session, url, comment)
        print(f"HTTP status: {res.status_code}\n")
        if res.status_code == 200:
            return True

    return False


def _summary_url_page(url: str) -> str:
    summary = ""

    try:
        # 記事の要約をキャッシュがあればキャッシュから取得、なければchatGPTに要約してもらう
        cache_file_path = cache_dir + sanitize_filename(url)[:200]
        with open(cache_file_path, "r") as f:
            summary = f.read()

    except Exception:
        # トークン上限を回避するため、3000字程度まで読んだことにする
        article_text = parse_page(url)[:3000]

        # 字数が少ない記事は情報不足としてコメントしない
        if len(article_text) < 200:
            raise ValueError("Article text length too short")

        print(f"{article_text}\n")
        summary = summarize(article_text)
        with open(cache_file_path, "w") as f:
            f.write(summary)

    return summary


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        ValueError("情報を取得するURLを指定してください。")

    bookmark_by_gpt(url)
