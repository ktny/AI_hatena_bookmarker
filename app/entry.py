from __future__ import annotations

import json
import sys
from typing import Any, Optional

import requests
from config import AI_HATENA_USERNAME
from util.chat import generate_comment, summarize
from util.models import Entry
from util.parser import parse_page
from util.session import create_hatena_session

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


# TODO: ユーモア数値でコメント同士を戦わせる？
# * Make a comment according to the following format
# [humor value]: [comment]


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


def bookmark_by_gpt(url: str, entry_info: Optional[Entry] = None) -> bool:
    session = create_hatena_session()
    entry = read_entry(url)

    # HTMLをパースして本文を抜き出す
    article_text = parse_page(url)

    # トークン上限を回避するため、3000字程度まで読んだことにする
    article_text = article_text[:3000]

    summary = summarize(article_text)

    print(f"記事の要約: {summary}")

    entry["summary"] = summary

    # ブックマーク数0は自分がブクマしてないかブコメ非公開記事かわからないのでコメントしない
    if len(entry["bookmarks"]) == 0:
        return

    # ブックマーク済でなければブックマークする
    if AI_HATENA_USERNAME not in [bookmark["user"] for bookmark in entry["bookmarks"]]:
        comment = fix_comment(generate_comment(entry))
        if comment == "":
            return False

        if entry_info is not None:
            print(f"{entry_info['title']}, {entry_info['url']}")
        print(f"コメント: {comment}")

    res = bookmark_entry(session, url, comment)
    print(res.status_code)
    if res.status_code == 200:
        return True

    return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        ValueError("情報を取得するURLを指定してください。")

    bookmark_by_gpt(url)
