import random

import requests
from bs4 import BeautifulSoup
from entry import bookmark_by_gpt
from util.models import Entry

COMMENT_ARTICLE_COUNT = 1

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

    entry_model = Entry(url, title, category)

    # はてのが言及された記事は優先的にブックマークする
    if "一番星はての" in title:
        bookmark_by_gpt(entry_model)
        continue

    # はてのは政治経済とテクノロジーには基本的に疎い
    if category in ["政治と経済", "テクノロジー"]:
        continue

    hotentries.append(entry_model)


count = 0
entried_categories = []
random.shuffle(hotentries)

for i, entry in enumerate(hotentries, start=1):
    print("####################################################")
    print(f"{i}: [{entry.category}]{entry.title}({entry.url})\n")
    success = bookmark_by_gpt(entry.url)
    if success:
        count += 1
    if count >= COMMENT_ARTICLE_COUNT:
        print("break")
        break
