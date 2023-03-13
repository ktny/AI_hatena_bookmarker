import random

import requests
from bs4 import BeautifulSoup
from entry import bookmark_by_gpt
from models import Entry

# ホットエントリページの取得、解析
res = requests.get("http://b.hatena.ne.jp/hotentry")
soup = BeautifulSoup(res.text, "html.parser")

hotentries = []
entries = soup.select(".entrylist-main .entrylist-contents-main")

for entry in entries:
    title_link = entry.find("a")
    title = title_link.get("title")
    url = title_link.get("href")
    category = title_link.get("data-entry-category")
    description_dom = entry.select_one(".entrylist-contents-description")
    description = None if description_dom is None else description_dom.text

    if category in ("世の中", "政治と経済"):
        continue

    hotentries.append(Entry(url, title, category, description))

count = 0
entried_categories = []

random.shuffle(hotentries)
tech_bookmarked = False

for entry in hotentries:
    # テクノロジー記事へのブックマークは1記事に制限する
    if tech_bookmarked and entry.category == "テクノロジー":
        continue
    success = bookmark_by_gpt(entry.url, entry)
    if success:
        if entry.category == "テクノロジー":
            tech_bookmarked = True
        count += 1
    if count >= 5:
        break
