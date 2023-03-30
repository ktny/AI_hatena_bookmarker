import os

HATENA_CONSUMER_KEY = os.getenv("HATENA_CONSUMER_KEY")
HATENA_CONSUMER_SECRET = os.getenv("HATENA_CONSUMER_SECRET")
HATENA_ACCESS_TOKEN = os.getenv("HATENA_ACCESS_TOKEN")
HATENA_ACCESS_TOKEN_SECRET = os.getenv("HATENA_ACCESS_TOKEN_SECRET")
HATENA_RK = os.getenv("HATENA_RK")
HATENA_RKS = os.getenv("HATENA_RKS")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

AI_USERNAME = "はてな"
AI_HATENA_USERNAME = "hatena"

gpt_system_message = f"""あなたは{AI_USERNAME}という名前です。

* 設定

（ここに設定を書く）

* 発言サンプルなど

（ここに発言サンプルを書く）

上記の設定や発言サンプルを参考に、性格や口調や言葉の作り方を模倣してください"""
