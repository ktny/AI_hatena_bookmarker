#
# 記事に対してコメントする用のテンプレート
#
comment_to_article_template = """記事に対してコメントしてください。

## 記事
{summary}

## Guildline
ガイドラインを書いてください

## Format
COMMENT: <comment>"""

#
# 記事を要約する用のテンプレート
#
summarize_entry_template = """次の記事を要約してください。

## 記事
{title}
{text}

## 記事へのコメント
{comments}
"""

#
# 他のユーザーのブックマークコメントを選ぶ用のテンプレート
#
select_best_bookmarker_template = """Choose one user who made the nicest comment on the following article.

## Article
{summary}

## List users and comments in the following format

USER: COMMENT

---

{bookmark_list}

## Output in the following format

USER
"""
