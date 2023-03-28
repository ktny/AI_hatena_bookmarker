# TODO: hotentryと合わせてリファクタリング

import requests
from bs4 import BeautifulSoup
from chat import select_most_interesting_entry
from entry import bookmark_by_gpt
from util.models import Entry

COMMENT_ARTICLE_COUNT = 1

# 新着エントリページの取得、解析
res = requests.get("https://b.hatena.ne.jp/entrylist/all")
soup = BeautifulSoup(res.text, "html.parser")

newentries = []
entries = soup.select(".entrylist-main .entrylist-contents-main")


for entry in entries:
    title_link = entry.find("a")
    title = title_link.get("title")
    url = title_link.get("href")
    category = title_link.get("data-entry-category")

    newentries.append(Entry(url, title, category))


index = int(select_most_interesting_entry(newentries))

print(index, newentries[index].title)

bookmark_by_gpt(newentries[index].url)
