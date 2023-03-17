import requests
from bs4 import BeautifulSoup


def parse_page(url: str):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    content = [s.text for s in soup.select("div.section > p:not([class])")][0]
    content = remove_after_substring(content, "Permalink")
    return content


def remove_after_substring(text: str, substring: str) -> str:
    if substring in text:
        text = text.split(substring, 1)[0]
    return text
