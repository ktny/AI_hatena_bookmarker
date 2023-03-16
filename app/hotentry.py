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

    if category in ["政治と経済"]:
        continue

    hotentries.append(Entry(url, title, category, description))

count = 0
entried_categories = []

random.shuffle(hotentries)

for entry in hotentries:
    success = bookmark_by_gpt(entry.url, entry)
    if success:
        count += 1
    if count >= 5:
        break
