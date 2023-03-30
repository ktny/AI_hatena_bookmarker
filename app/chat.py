import random

import openai
from config import AI_USERNAME, OPENAI_API_KEY, gpt_system_message

openai.api_key = OPENAI_API_KEY


def generate_comment(entry: dict) -> str:
    prompt = generate_prompt(entry)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": gpt_system_message},
            {"role": "user", "content": prompt},
        ],
        temperature=0.9,
    )
    return response["choices"][0]["message"]["content"]


def generate_prompt(entry: dict) -> str:
    bookmarks = [bookmark["comment"] for bookmark in entry["bookmarks"] if bookmark.get("comment")]

    if len(bookmarks) > 15:
        random.shuffle(bookmarks)
        bookmarks = bookmarks[:15]

    comments = "\n".join(bookmarks)
    return f"""# 次の記事に対して{AI_USERNAME}として日本語で1文で短いコメントしてください。

{entry["summary"]}

---

# 以下は記事に対する他の人のコメントです

{comments}

"""
