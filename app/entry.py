from __future__ import annotations

import json
import random
import sys
from parser import parse_page
from typing import Any, Dict, Optional

import openai
import requests
from config import AI_HATENA_USERNAME, AI_USERNAME, OPENAI_API_KEY, gpt_system_message
from models import Entry
from session import create_hatena_session

read_entry_endpoint = "https://b.hatena.ne.jp/entry/jsonlite/"
bookmark_entry_endpoint = "https://bookmark.hatenaapis.com/rest/1/my/bookmark"

openai.api_key = OPENAI_API_KEY


def read_entry(url: str):
    response = requests.get(read_entry_endpoint + url)
    return json.loads(response.text)


def bookmark_entry(session: Any, url: str, comment: str):
    return session.post(
        bookmark_entry_endpoint,
        params={"url": url, "comment": comment, "post_twitter": True},
    )


def generate_comment(entry: Dict):
    prompt = generate_prompt(entry)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": gpt_system_message},
            {"role": "user", "content": prompt},
        ],
        temperature=0.9,
    )
    return response["choices"][0]["message"]["content"]


def generate_prompt(entry: Dict):
    bookmarks = [bookmark["comment"] for bookmark in entry["bookmarks"] if bookmark.get("comment")]

    if len(bookmarks) > 10:
        random.shuffle(bookmarks)
        bookmarks = bookmarks[:10]
    comments = ",".join(bookmarks)

    return f"""Please comment on the following article as {AI_USERNAME}.

# title

{entry["title"]}

# content

{entry.get("description", "")}
{entry.get("content", "")}

# other's comments

{comments}

# Please comment according to the following guidelines.

* Make a comment with wit and humor to the max.
* Don't make a comment that make people look stupid.
* Make a short comment in one sentence in Japanese.
"""


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

    result = (
        result.replace("「", "")
        .replace("」", "")
        .replace("（", "")
        .replace("）", "")
        .replace("(", "")
        .replace(")", "")
        .replace("comment = ", "")
        .replace("？。", "？")
        .replace("！。", "！")
    )

    return result


def bookmark_by_gpt(url: str, entry_info: Optional[Entry] = None) -> bool:
    session = create_hatena_session()
    entry = read_entry(url)

    # 特定ドメインはページをパースする
    if url.startswith("https://anond.hatelabo.jp/"):
        content = parse_page(url)
        entry["content"] = content

    entry["description"] = ""
    if entry_info is not None and entry_info.description is not None:
        entry["description"] = entry_info.description

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
        print(comment)

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
