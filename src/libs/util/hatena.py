"""
はてなAPIなどを使用した関数リスト
"""

import json

import requests
from requests_oauthlib import OAuth1Session

from libs.common import config
from libs.common.models import Bookmark, Entry
from libs.util.llm.chat import select_best_bookmarker

login_url = "https://www.hatena.ne.jp/login"

read_entry_endpoint = "https://b.hatena.ne.jp/entry/jsonlite/"
bookmark_entry_endpoint = "https://bookmark.hatenaapis.com/rest/1/my/bookmark"
add_star_endpoint = "https://s.hatena.ne.jp/star.add.json"


def create_hatena_session() -> OAuth1Session:
    """
    認証情報を使ってOAuth1Sessionオブジェクトを作成する
    """
    return OAuth1Session(
        config.HATENA_CONSUMER_KEY,
        client_secret=config.HATENA_CONSUMER_SECRET,
        resource_owner_key=config.HATENA_ACCESS_TOKEN,
        resource_owner_secret=config.HATENA_ACCESS_TOKEN_SECRET,
    )


def read_entry(url: str) -> Entry:
    """
    はてなのエントリーAPIから記事情報を取得する
    記事カテゴリ情報、初ブックマーク日は取得できない（スクレイピングでしか取得できない）
    """
    try:
        response = requests.get(read_entry_endpoint + url)
        data = json.loads(response.text)
        return Entry.parse_obj(data)
    except Exception:
        return Entry(eid="", url=url, category=None, title="", count=0)


def get_my_bookmark(url: str) -> Bookmark | None:
    """
    エントリの自分のブックマークを取得する
    """
    try:
        session = create_hatena_session()
        response = session.get(bookmark_entry_endpoint, params={"url": url})
        data = json.loads(response.text)
        bookmark = Bookmark.parse_obj(
            {
                "user": data["user"],
                "comment": data["comment_raw"],
                "tags": data["tags"],
                "timestamp": data["created_datetime"],
                "link": data["permalink"],
            }
        )
        return bookmark

    except Exception:
        return None


def bookmark_entry(url: str, comment: str, tags: list[str] | None = None) -> Bookmark | None:
    """
    はてなのエントリーにブックマークをする
    """
    if config.dryrun:
        return None

    session = create_hatena_session()
    res = session.post(bookmark_entry_endpoint, params={"url": url, "comment": comment, "tags": tags})
    if res.status_code == 200:
        data = json.loads(res.text)
        bookmark = Bookmark.parse_obj(
            {
                "user": data["user"],
                "comment": data["comment"],
                "tags": data["tags"],
                "timestamp": data["created_datetime"],
                "link": data["permalink"],
            }
        )
        return bookmark

    return None


def add_star(uri: str):
    """
    はてなのブックマークにスターを付与する
    公式APIではなく、はてなのwebサイトの挙動をHTTPリクエストで再現している

    @see
    https://needtec.sakura.ne.jp/wod07672/2020/04/02/%E3%81%AF%E3%81%A6%E3%81%AA%E3%83%96%E3%83%83%E3%82%AF%E3%83%9E%E3%83%BC%E3%82%AF%E3%81%AErest-api%E3%82%92%E5%88%A9%E7%94%A8%E3%81%99%E3%82%8B/

    TODO: セッション切れに対応するためトークン取得を自動化する
    """
    if config.dryrun:
        return

    requests.get(
        add_star_endpoint,
        params={"uri": uri, "rks": config.HATENA_RKS},
        cookies={"rk": config.HATENA_RK},
    )


def add_star_to_best_bookmarker(entry: Entry):
    """
    指定された記事に対するブックマークとして最もよいコメントにスターを付与する
    """
    if config.dryrun:
        return

    if len(entry.recent_bookmarks) <= 0:
        return

    best_user = select_best_bookmarker(entry)

    for bookmark in entry.recent_bookmarks:
        if bookmark.user == best_user:
            add_star(bookmark.link)
            break
