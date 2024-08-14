from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Category(Enum):
    """
    はてなエントリのカテゴリ情報
    """

    social = "世の中"  # コメントする
    life = "暮らし"  # コメントする
    knowledge = "学び"  # コメントする
    fun = "おもしろ"  # コメントする
    game = "アニメとゲーム"  # コメントする
    economics = "政治と経済"  # コメントしない
    it = "テクノロジー"  # コメントしない
    entertainment = "エンタメ"  # コメントしない


class Bookmark(BaseModel):
    """
    はてなのエントリーAPIで取得できる情報とスクレイピングで取得できる情報を組み合わせたブックマーク情報のモデル
    """

    user: str  # ブックマークしたユーザー
    comment: str  # ブックマークコメント
    tags: list[str] = []  # ブックマークのタグ
    timestamp: str | None  # ブックマークした日時
    link: str | None  # ブックマークのリンク（スター付与時に使用。スクレイピングでのみ取得可）


class Entry(BaseModel):
    """
    はてなのエントリーAPIで取得できる情報とスクレイピングで取得できる情報を組み合わせた記事情報のモデル
    """

    eid: str  # はてなの記事の固有ID
    url: str  # 記事自体のURL
    category: Category | None  # 記事カテゴリ
    title: str  # 記事タイトル
    text: str = ""  # 記事本文（タイトルを含む）（3000字まで）
    summary: str = ""  # 記事要約（textが1000字未満の場合はtextと同じ内容が入る）
    entry_url: str | None = None  # 記事に対するはてなブックマークのURL
    bookmarks: list[Bookmark] = []  # 記事に対してついたブックマーク
    popular_bookmarks: list[Bookmark] = (
        []
    )  # 記事に対してついた人気のブックマーク（スクレイピングで取得。取得内容が異なるのでbookmarksとは分ける）
    recent_bookmarks: list[Bookmark] = (
        []
    )  # 記事に対してついた直近のブックマーク（スクレイピングで取得。取得内容が異なるのでbookmarksとは分ける）
    count: int  # ブックマーク数
    published_at: datetime | None  # 初めてはてなブックマークされた日時（記事公開日ではないことに注意）
