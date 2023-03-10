from __future__ import annotations

import json
import sys

import openai
import requests
from config import OPENAI_API_KEY
from session import create_hatena_session

read_entry_endpoint = "https://b.hatena.ne.jp/entry/jsonlite/"
bookmark_entry_endpoint = "https://bookmark.hatenaapis.com/rest/1/my/bookmark"

openai.api_key = OPENAI_API_KEY


def read_entry(url):
    # APIにリクエストを送信
    response = requests.get(read_entry_endpoint + url)
    return json.loads(response.text)


def bookmark_entry(session, url, comment):
    # ブックマークを追加するためのデータ
    params = {
        "url": url,
        "comment": comment,
        # "tags": "example, bookmark",
    }

    # APIにリクエストを送信
    return session.post(bookmark_entry_endpoint, params=params)


def generate_comment(entry):
    prompt = generate_prompt(entry)
    print(prompt)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたはお嬢様です"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.9,
    )
    return response["choices"][0]["message"]["content"]


def generate_prompt(entry):
    return f"""次の記事のタイトルと記事に対するコメントから感想をコメントしてください

制約: 60文字以内
記事のタイトル：{entry["title"]}
記事に対するコメント：うーむ
"""


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        ValueError("情報を取得するURLを指定してください。")

    session = create_hatena_session()
    entry = read_entry(url)
    comment = generate_comment(entry)
    print(comment)

    res = bookmark_entry(session, entry["url"], comment)

    print(res.status_code)
    print(res.text)
