import random

import openai
from config import AI_USERNAME, OPENAI_API_KEY, gpt_system_message

openai.api_key = OPENAI_API_KEY


def summarize(content: str):
    prompt = f"""次の記事を日本語で要約してください。

{content}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return response["choices"][0]["message"]["content"]


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


def select_best_bookmarker(title: str, bookmarks: list):
    bookmark_list = "\n".join([f"{b['username']}: {b['comment']}" for b in bookmarks])
    prompt = f"""Choose the user who made the nicest comment on the following article as {AI_USERNAME}.

# Constraints

* Don't select comment that hurt people.

# Article

{title}

## List users and comments in the following format

USER: COMMENT

---

{bookmark_list}

# Output in the following format

USER
"""

    print(prompt)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": gpt_system_message},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return response["choices"][0]["message"]["content"]


def select_most_interesting_entry(entries: list):
    entry_list = "\n".join([f"{i}: {entry.title}" for i, entry in enumerate(entries)])
    prompt = f"""Please select the article title below that most intrigues you as {AI_USERNAME}.

## List articles in the following format

INDEX: TITLE

---

{entry_list}

# Output in the following format

INDEX
"""

    print(prompt)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": gpt_system_message},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )
    return response["choices"][0]["message"]["content"]
