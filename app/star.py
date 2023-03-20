# @see
# https://needtec.sakura.ne.jp/wod07672/2020/04/02/%E3%81%AF%E3%81%A6%E3%81%AA%E3%83%96%E3%83%83%E3%82%AF%E3%83%9E%E3%83%BC%E3%82%AF%E3%81%AErest-api%E3%82%92%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B/

import json
import os
import sys

import openai
import requests
from config import AI_USERNAME, HATENA_RK, HATENA_RKS
from entry import read_entry
from util.parser import parse_bookmark_page

login_url = "https://www.hatena.ne.jp/login"
endpoint = "https://s.hatena.ne.jp/star.add.json"


# "uri": "https://b.hatena.ne.jp/namabacon/20230310#bookmark-4733419499309148580"


# TODO: セッション切れに対応するためトークン取得を自動化する
def add_star(uri: str):
    params = {"uri": uri, "rks": HATENA_RKS}
    cookies = {"rk": HATENA_RK}

    response = requests.get(endpoint, params=params, cookies=cookies)

    print(response.status_code)
    print(json.loads(response.text))


def select_best_bookmark_comment(bookmarks: list[str]):
    prompt = f"""Please select the person whose comment is most appropriate for the following article as {AI_USERNAME}.

title:
{entry["title"]}

{entry.get("description", "")}
{entry.get("content", "")}

---

Please comment according to the following guidelines.

* Make a comment that will make those around you laugh with wit and humor.
* Don't make a comment that make people look stupid.
* Make a short comment in Japanese, about 1 or 2 sentences.
* Simulate the following program and generate comments while recursively increasing the degree of humor

comment = generate(article)
review = review_text(comment)
while check_humor(review) < 0.5:
    comment = update_comment(theme, review)
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": gpt_system_message},
            {"role": "user", "content": prompt},
        ],
        temperature=0.9,
    )
    return response["choices"][0]["message"]["content"]
    return ""


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        ValueError("情報を取得するURLを指定してください。")

    entry = read_entry(url)
    bookmark_page_url = entry["entry_url"]

    parse_bookmark_page(bookmark_page_url)

    # bookmarks = [f'{bookmark["user"]}: {bookmark["comment"]}' for bookmark in entry["bookmarks"] if bookmark.get("comment")]

    # if len(bookmarks) <= 0:
    #     os.exit(0)

    # print(entry["bookmarks"])

    # uri = "https://b.hatena.ne.jp/namabacon/20230310#bookmark-4733419499309148580"
    # add_star(uri)
