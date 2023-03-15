from __future__ import annotations

import json
import random
import sys
from typing import Any, Dict, Optional

import openai
import requests
from config import AI_HATENA_USERNAME, AI_USERNAME, OPENAI_API_KEY, gpt_system_message
from models import Entry
from session import create_hatena_session
from tokenizer import extract_nouns

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
    bookmarks = [
        bookmark["comment"]
        for bookmark in entry["bookmarks"]
        if bookmark.get("comment")
    ]

    if len(bookmarks) > 10:
        bookmarks = random.sample(bookmarks, 10)
    comments = ",".join(bookmarks)

    nouns = extract_nouns(entry["title"])

    print("nouns", nouns)

    return f"""次のお題に対して「{AI_USERNAME}」としてコメントしてください。

お題

・タイトル：{entry["title"]}
・説明文：{entry["description"]}
・ブコメ：{comments}

以下の制約を守ってコメントしてください。

・1文でコメントする

以下の単語を絶対に使わないでください。

・{", ".join(nouns)}

以下の形式でコメントしてください。

{AI_USERNAME}：コメント
"""


def fix_comment(comment: str):
    excluding_words = ["（楽観的）", "（可能性）", "（話題の変更）", "（同意）", "（質問）", "（提案）"]
    for word in excluding_words:
        comment = comment.replace(word, "")

    comment = comment.replace(f"{AI_USERNAME}：", "").strip()
    sentences = comment.strip("。").split("。")
    result = ""
    for sentence in sentences:
        if len(result + sentence + "。") <= 100:
            result += sentence + "。"
        else:
            break

    return result


def bookmark_by_gpt(url: str, entry_info: Optional[Entry] = None) -> bool:
    session = create_hatena_session()
    entry = read_entry(url)

    entry["description"] = ""
    if entry_info is not None and entry_info.description is not None:
        entry["description"] = entry_info.description

    # ブックマーク数0は自分がブクマしてないかブコメ非公開記事かわからないのでコメントしない
    if len(entry["bookmarks"]) == 0:
        return

    # ブックマーク済でなければブックマークする
    if AI_HATENA_USERNAME not in [bookmark["user"] for bookmark in entry["bookmarks"]]:
        comment = fix_comment(generate_comment(entry))
        if entry_info is not None:
            print(f"{entry_info.title}, {entry_info.category}")
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
