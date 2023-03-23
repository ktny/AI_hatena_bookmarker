# @see
# https://needtec.sakura.ne.jp/wod07672/2020/04/02/%E3%81%AF%E3%81%A6%E3%81%AA%E3%83%96%E3%83%83%E3%82%AF%E3%83%9E%E3%83%BC%E3%82%AF%E3%81%AErest-api%E3%82%92%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B/

import json
import sys

import requests
from chat import select_best_bookmarker
from config import HATENA_RK, HATENA_RKS
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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        ValueError("情報を取得するURLを指定してください。")

    entry = read_entry(url)
    bookmark_page_url = entry["entry_url"]
    bookmarks = parse_bookmark_page(bookmark_page_url)

    best_username = select_best_bookmarker(entry["title"], bookmarks)

    for bookmark in bookmarks:
        if bookmark["username"] == best_username:
            print("次のユーザーのコメントが選ばれました")
            print(bookmark)
            add_star(bookmark["link"])
