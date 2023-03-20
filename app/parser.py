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


def parse_page(url: str):
    res = requests.get(url)
    html_data = res.content.decode("utf-8")
    soup = BeautifulSoup(html_data, "html.parser")

    # HTMLから不要なタグを削除
    for remove_tag in REMOVE_TAGS:
        for tag in soup.find_all(remove_tag):
            tag.decompose()
    for remove_tag in REMOVE_CLASSNAMES:
        for tag in soup.find_all(class_=remove_tag):
            tag.decompose()
    for remove_tag in REMOVE_IDS:
        for tag in soup.find_all(id=remove_tag):
            tag.decompose()

    texts = ""

    # タイトルタグを取得します
    title_tag = soup.find("title")
    if title_tag is not None:
        title = title_tag.get_text()
        if title:
            texts += f"# {title}\n"

    # 見出しタグを検索します
    for h_tag in soup.find_all(HEADLINE_TAGS):
        # 見出しタグのテキストを取得
        h_text = h_tag.get_text()
        texts += f"# {h_text}\n"

        # print(f"(デバッグ) {h_tag.name}: {h_text}")

        # 見出しの次のタグを取得
        next_tag = h_tag.find_next_sibling()

        # 次のタグがなくなるまでループ
        while next_tag is not None:
            if next_tag.name in HEADLINE_TAGS:
                # print(f"(デバッグ) 次の見出しタグ {next_tag.name} が見つかった。")
                # print(f"(デバッグ) while ブレーク\n")
                break

            # タグのテキストを取得
            text = next_tag.get_text()
            if text:
                texts += text

            # print(f"(デバッグ) {next_tag.name}: {text}")

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
