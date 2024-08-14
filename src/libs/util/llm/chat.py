from langchain.chains import LLMChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from libs.common import config
from libs.common.models import Entry
from libs.util.llm import prompt_template

memories: dict[str, ConversationBufferWindowMemory] = {}

MODEL = "gpt-4o-mini"


def create_llm_chain(
    temperature: float,
    user_prompt: str,
    system_prompt: str | None = None,
    model_name: str = MODEL,
) -> LLMChain:
    """
    chatモデルにprompt_templateを渡して会話をする用のchainを作成する
    """
    llm = ChatOpenAI(model_name=model_name, temperature=temperature)

    messages = []
    if system_prompt is not None:
        messages.append(SystemMessagePromptTemplate.from_template(system_prompt))
    messages.append(HumanMessagePromptTemplate.from_template(user_prompt))

    chat_prompt = ChatPromptTemplate.from_messages(messages)

    chain = LLMChain(llm=llm, prompt=chat_prompt, verbose=True)

    return chain


def summarize_entry(entry: Entry):
    """
    エントリを要約する
    """
    chain = create_llm_chain(temperature=0, user_prompt=prompt_template.summarize_entry_template)
    comments = "\n".join([b.comment for b in entry.recent_bookmarks][::-1][:15])
    prediction = chain.run(title=entry.title, text=entry.text[:5000], comments=comments)
    comment = prediction.strip()

    return comment


def generate_comment(entry: Entry) -> str:
    """
    エントリ情報に基づいてブックマークコメントを生成する
    """
    comment = ""

    # カテゴリごとに指示文やtempatureやコメント例を変更する
    match entry.category:
        case _:
            chain = create_llm_chain(
                temperature=0.7,
                user_prompt=prompt_template.comment_to_article_template,
                system_prompt=config.character_setting,
            )

            prediction = chain.run(summary=entry.summary)
            comment = prediction.strip()

    return comment


def select_best_bookmarker(entry: Entry) -> str:
    """
    エントリ情報に紐づくブックマークから最も適当なブックマークを選択する
    """
    bookmarks = []
    for b in entry.recent_bookmarks:
        if b.user == config.AI_HATENA_USERNAME:
            continue
        bookmarks.append(f"{b.user}: {b.comment}")
    bookmark_list = "\n".join(bookmarks)

    chain = create_llm_chain(
        temperature=0,
        user_prompt=prompt_template.select_best_bookmarker_template,
        system_prompt=config.character_setting,
    )
    prediction = chain.run(title=entry.title, summary=entry.summary, bookmark_list=bookmark_list)
    comment = prediction.strip()

    return comment
