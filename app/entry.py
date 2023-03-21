from __future__ import annotations

import json
import sys
from typing import Any

import requests
from chat import generate_comment, summarize
from config import AI_HATENA_USERNAME
from util.parser import parse_page
from util.session import create_hatena_session
from util.util import sanitize_filename

read_entry_endpoint = "https://b.hatena.ne.jp/entry/jsonlite/"
bookmark_entry_endpoint = "https://bookmark.hatenaapis.com/rest/1/my/bookmark"

cache_dir = "__cache__/"


def read_entry(url: str):
    response = requests.get(read_entry_endpoint + url)
    return json.loads(response.text)


def bookmark_entry(session: Any, url: str, comment: str):
    return session.post(
        bookmark_entry_endpoint,
        params={"url": url, "comment": comment, "post_twitter": True},
    )


def fix_comment(comment: str):
    sentences = comment.strip("。").split("。")
    result = ""
    for sentence in sentences:
        if len(result + sentence + "。") <= 100:
            result += sentence + "。"
        else:
            break

    result = result.replace("？。", "？").replace("！。", "！")

    return result


def bookmark_by_gpt(url: str) -> bool:
    session = create_hatena_session()
    entry = read_entry(url) or {}

    # HTMLをパースして本文を抜き出す
    article_text = parse_page(url)
    print(f"{article_text}\n")

    # 200字に満たない記事は情報不足としてコメントしない
    if len(article_text) < 200:
        return False

    # トークン上限を回避するため、3000字程度まで読んだことにする
    article_text = article_text[:3000]

    # 記事の要約をキャッシュがあればキャッシュから取得、なければchatGPTに要約してもらう
    cache_file_path = cache_dir + sanitize_filename(url)[:200]

    try:
        with open(cache_file_path, "r") as f:
            summary = f.read()
    except FileNotFoundError:
        summary = summarize(article_text)
        with open(cache_file_path, "w") as f:
            f.write(summary)

    print(f"記事の要約: {summary}\n")
    entry["summary"] = summary

    # ブックマーク済の場合はコメントしない
    if AI_HATENA_USERNAME in [bookmark["user"] for bookmark in entry.get("bookmarks")]:
        return False

    comment = fix_comment(generate_comment(entry))
    if comment:
        print(f"コメント: {comment}\n")
        res = bookmark_entry(session, url, comment)
        print(f"HTTP status: {res.status_code}\n")
        if res.status_code == 200:
            return True

    return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        ValueError("情報を取得するURLを指定してください。")

    bookmark_by_gpt(url)
