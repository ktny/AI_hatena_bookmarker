import chardet
import requests
from bs4 import BeautifulSoup

from libs.common.models import Bookmark, Category

# 不要なタグを検索するタグ名のタプル
REMOVE_TAGS = (
    "link",
    "meta",
    "style",
    "script",
    "noscript",
    "iframe",
    "aside",
    "header",
    "footer",
    "img",
    "map",
    "area",
    "form",
    "input",
    "select",
    "option",
    "textarea",
    "address",
    "table",
    "code",
    "figcaption",
)


HEADLINE_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")


def parse_page(url: str) -> str:

    res = requests.get(url)
    if res.status_code >= 400:
        raise ValueError(f"Cannot read url: {url}")

    encoding = chardet.detect(res.content)["encoding"]

    if encoding is None or encoding.lower() not in ("shift_jis", "utf-8", "euc-jp"):
        encoding = "utf-8"

    html_data = res.content.decode(encoding)
    soup = BeautifulSoup(html_data, "html.parser")
    texts = ""

    # HTMLから不要なタグを削除
    _remove_tags(soup)

    # meta descriptionタグを取得します
    descriptoin_tag = soup.find("meta", {"name": "description"})
    if descriptoin_tag is not None:
        description = descriptoin_tag.get("content")
        if description:
            texts += f"{description}\n"

    # 見出しタグを検索
    for h_tag in soup.find_all(HEADLINE_TAGS):
        text = _extract_headline_and_text(h_tag)
        texts += f"{text}\n"

    if len(texts) < 150:
        raise Exception("記事で読めた文章が短すぎます。")

    return texts


def _remove_tags(soup: BeautifulSoup):
    for remove_tag in REMOVE_TAGS:
        for tag in soup.find_all(remove_tag):
            tag.decompose()


def _extract_headline_and_text(h_tag):
    texts = ""

    # 見出しタグのテキストを取得
    h_text = h_tag.get_text()
    texts += f"{h_text}\n"

    # 見出しの次のタグを取得
    next_tag = h_tag.find_next_sibling()

    # 次のタグがなくなるまでループ
    while next_tag is not None:
        if next_tag.name in HEADLINE_TAGS:
            break

        # タグのテキストを取得
        text = next_tag.get_text()
        if text:
            texts += text

        # さらに次のタグを取得してループする
        next_tag = next_tag.find_next_sibling()

    return texts


def parse_bookmark_page(url: str) -> dict[str, list[Bookmark] | Category]:
    """
    はてブのブックマークページをスクレイピングしてブックマーク一覧、カテゴリ情報を取得する
    エントリーAPIでは取得できないブックマークごとのリンクが取得できる。スター付与にはリンクが必要
    """
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    tabs = ["popular", "recent"]
    result = {"popular": [], "recent": [], "category": None}

    # ブックマーク一覧のパース
    for tab in tabs:
        bookmarks: list[Bookmark] = []
        recent_bookmarks_dom = soup.find("div", class_=f"js-bookmarks-{tab}")
        parsed_bookmarks = recent_bookmarks_dom.find_all("div", class_="entry-comment-contents")

        for bookmark in parsed_bookmarks:
            username_dom = bookmark.find("span", class_="entry-comment-username")
            comment_dom = bookmark.find("span", class_="entry-comment-text")
            link_dom = bookmark.find("a", class_="js-bookmark-anchor-path")

            if username_dom is None or comment_dom is None or link_dom is None:
                continue

            bookmarks.append(
                Bookmark(
                    user=username_dom.get_text(),
                    comment=comment_dom.get_text(),
                    link=link_dom.get("href"),
                )
            )

        result[tab] = bookmarks

    # カテゴリ情報を取得
    result["category"] = Category(soup.select_one(".entry-info-category-name").get_text())

    return result
