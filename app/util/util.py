import re


def sanitize_filename(str: str) -> str:
    # ファイル名に使えない文字をアンダースコアに置換する正規表現パターンを定義する
    pattern = r'[\\/:\*\?"<>\|]'

    # 正規表現パターンにマッチする文字列をアンダースコアに置換する
    return re.sub(pattern, "_", str)
