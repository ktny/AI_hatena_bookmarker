import requests
from bs4 import BeautifulSoup

# 不要なタグを検索するタグ名のタプル
REMOVE_TAGS = (
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
)
REMOVE_CLASSNAMES = ("refererlist", "hotentries-wrapper", "sectionfooter", "share-button")
REMOVE_IDS = ("bookmark-comment-unit",)

HEADLINE_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")
EXTRACT_TAGS = (("p", "tweet"),)  # for Togetter


def parse_page(url: str):
    res = requests.get(url)
    html_data = res.content.decode("utf-8")
    soup = BeautifulSoup(html_data, "html.parser")

    # HTMLから不要なタグを削除
    _remove_tags(soup)

    texts = ""

    # titleタグを取得します
    title_tag = soup.find("title")
    if title_tag is not None:
        title = title_tag.get_text()
        if title:
            texts += f"{title}\n"

    # meta descriptionタグを取得します
    descriptoin_tag = soup.find("meta", {"name": "description"})
    if descriptoin_tag is not None:
        description = descriptoin_tag.get("content")
        if description:
            texts += f"{description}\n"

    # 見出しタグを検索します
    for h_tag in soup.find_all(HEADLINE_TAGS):
        text = _extract_headline_and_text(h_tag)
        texts += f"{text}\n"

    for extract_tag, _class in EXTRACT_TAGS:
        for tag in soup.find_all(extract_tag, attrs={"class": _class}):
            text = tag.get_text()
            texts += f"{text}\n"

    return texts


def _remove_tags(soup: BeautifulSoup):
    for remove_tag in REMOVE_TAGS:
        for tag in soup.find_all(remove_tag):
            tag.decompose()
    for remove_tag in REMOVE_CLASSNAMES:
        for tag in soup.find_all(class_=remove_tag):
            tag.decompose()
    for remove_tag in REMOVE_IDS:
        for tag in soup.find_all(id=remove_tag):
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


def parse_bookmark_page(url: str):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # content = []
    comments = soup.select(".js-bookmarks .entry-comment-contents")

    # comment_models = []
    for comment in comments:
        meta = comment.find(".entry-comment-contents-main")

        print(meta)

        # meta = comment.css(".entry-comment-contents-foot > .entry-comment-meta")
        # username = main.css(".entry-comment-username > a::text").extract_first().strip()
        # icon = main.css(".entry-user-icon > img::attr('src')").extract_first().strip()
        # content = (
        #     main.css(".entry-comment-text")
        #     .extract_first()
        #     .strip()
        #     .replace('<span class="entry-comment-text js-bookmark-comment">', "")
        #     .replace("</span>", "")
        # )

        # commented_at = datetime.strptime(meta.css(".entry-comment-timestamp > a::text").extract_first().strip(), "%Y/%m/%d").date()
        # comment_models.append(
        #     Comment(
        #         entry_id=None,
        #         url=response.meta.get("url"),
        #         rank=i,
        #         username=username,
        #         icon=icon,
        #         content=content,
        #         commented_at=commented_at,
        #     )
        # )

    # # usernameが重複するものは排除し上位10個に絞る
    # comment_models = [
    #     comment for i, comment in enumerate(comment_models) if comment["username"] not in [c["username"] for c in comment_models[:i]]
    # ][:10]
    # for comment in comment_models:
    #     if comment["rank"] <= 10:
    #         yield comment
