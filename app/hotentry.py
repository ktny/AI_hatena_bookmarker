import random

import requests
from bs4 import BeautifulSoup
from entry import bookmark_by_gpt

# ホットエントリページの取得、解析
res = requests.get("http://b.hatena.ne.jp/hotentry")
soup = BeautifulSoup(res.text, "html.parser")

hotentry_urls = []
entries = soup.select(".entrylist-main .entrylist-contents-main")

for entry in entries:
    title_link = entry.find("a")
    title = title_link.get("title")
    url = title_link.get("href")
    category = title_link.get("data-entry-category")

    if category in ("世の中", "政治と経済"):
        continue

    hotentry_urls.append(url)

for url in random.sample(hotentry_urls, 5):
    bookmark_by_gpt(url)
