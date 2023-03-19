import requests
from bs4 import BeautifulSoup


def parse_page(url: str):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    content = [s.text for s in soup.select("div.section > p")][0]
    content = remove_after_substring(content, "Permalink")
    return content


def remove_after_substring(text: str, substring: str) -> str:
    if substring in text:
        text = text.split(substring, 1)[0]
    return text


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
