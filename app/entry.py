from __future__ import annotations

import json
import random
import sys
from typing import Any, Dict

import openai
import requests
from config import AI_HATENA_USERNAME, AI_USERNAME, OPENAI_API_KEY, gpt_system_message
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
    bookmarks = [
        bookmark["comment"]
        for bookmark in entry["bookmarks"]
        if bookmark.get("comment")
    ]

    if len(bookmarks) > 30:
        bookmarks = random.sample(bookmarks, 30)
    comments = ",".join(bookmarks)

    return f"""次のお題に対して「{AI_USERNAME}」としてコメントしてください。

お題

・タイトル：{entry["title"]}
・ブコメ：{comments}

以下の制約を守ってコメントしてください。

・100文字以内で簡潔にコメントする
・お題は「タイトル」を60%、「ブコメ」を40%の割合でどちらも参考にコメントする

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


def bookmark_by_gpt(url: str):
    session = create_hatena_session()
    entry = read_entry(url)

    print(f"{entry['title']}, {url}")

    # ブックマーク済でなければブックマークする
    if AI_HATENA_USERNAME not in [bookmark["user"] for bookmark in entry["bookmarks"]]:
        comment = fix_comment(generate_comment(entry))
        print(comment)
        res = bookmark_entry(session, url, comment)
        print(res.status_code)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        ValueError("情報を取得するURLを指定してください。")

    bookmark_by_gpt(url)
