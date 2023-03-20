import random

import openai
from config import OPENAI_API_KEY, gpt_system_message

openai.api_key = OPENAI_API_KEY


def summarize(content: str):
    prompt = f"""Please summarize the following article in Japanese.

{content}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return response["choices"][0]["message"]["content"]


def generate_comment(entry: dict):
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


def generate_prompt(entry: dict):
    bookmarks = [bookmark["comment"] for bookmark in entry["bookmarks"] if bookmark.get("comment")]

    if len(bookmarks) > 10:
        random.shuffle(bookmarks)
        bookmarks = bookmarks[:10]

    comments = ",".join(bookmarks)
    return f"""次の記事に対して設定したキャラクターとしてコメントしてください。

# 記事

{entry["summary"]}

# 以下は記事に対する他の人のコメントです

{comments}

# 次のガイドラインに従ってコメントしてください

* ウィットとユーモアを最大限に生かしたコメントをしてください
* 人を馬鹿にするようなコメントはやめてください
* 日本語で1文で短いコメントをしてください
"""
