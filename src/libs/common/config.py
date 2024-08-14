import os
from distutils.util import strtobool

from dotenv import load_dotenv

load_dotenv()

HATENA_CONSUMER_KEY = os.getenv("HATENA_CONSUMER_KEY")
HATENA_CONSUMER_SECRET = os.getenv("HATENA_CONSUMER_SECRET")
HATENA_ACCESS_TOKEN = os.getenv("HATENA_ACCESS_TOKEN")
HATENA_ACCESS_TOKEN_SECRET = os.getenv("HATENA_ACCESS_TOKEN_SECRET")
HATENA_RK = os.getenv("HATENA_RK")
HATENA_RKS = os.getenv("HATENA_RKS")

AI_HATENA_USERNAME = "your AI hatena bookmarker username"

dryrun = strtobool(os.getenv("DRYRUN", "True"))

character_setting = """

## 設定
ここに設定を書いてください

## 性格
ここに性格を書いてください

## 発言サンプル
ここに発言サンプルを書いてください

上記の設定を参考に性格や口調や言葉の作り方を模倣してください"""
