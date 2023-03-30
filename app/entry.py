from __future__ import annotations

import argparse
import re

from chat import generate_comment
from config import AI_HATENA_USERNAME
from util.hatebu import bookmark_entry, read_entry
from util.session import create_hatena_session

read_entry_endpoint = "https://b.hatena.ne.jp/entry/jsonlite/"
bookmark_entry_endpoint = "https://bookmark.hatenaapis.com/rest/1/my/bookmark"

cache_dir = "__cache__/"


def fix_comment(comment: str):
    sentences = comment.strip("。").split("。")
    result = ""
    for sentence in sentences:
        if len(result + sentence + "。") <= 100:
            result += sentence + "。"
        else:
            break

    result = result.replace("？。", "？").replace("！。", "！")
    match = re.match('^[「"](.+)[」"]。$', result)
    if match is not None:
        result = match.groups()[0]

    return result


def bookmark_by_gpt(url: str, dryrun: bool = False) -> bool:
    session = create_hatena_session()
    entry = read_entry(url) or {"bookmarks": []}

    # ブックマーク済の場合はコメントしない
    if AI_HATENA_USERNAME in [bookmark["user"] for bookmark in entry.get("bookmarks")]:
        return False

    comment = fix_comment(generate_comment(entry))
    if comment:
        print(f"コメント: {comment}\n")
        if not dryrun:
            res = bookmark_entry(session, url, comment)
            print(f"HTTP status: {res.status_code}\n")
            if res.status_code == 200:
                return True

    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument("url", help="ブックマークなどを実行するURL")
    parser.add_argument("-d", "--dryrun", action="store_true", help="実際には実行しない")

    args = parser.parse_args()

    if args.url:
        print(f"URL is {args.url}")
    if args.dryrun:
        print("Dryrunで実行します")

    bookmark_by_gpt(args.url, args.dryrun)
