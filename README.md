# AIはてなブックマーカー

## これはなに

Chat-GPT APIを使用して任意のエントリーのタイトル、ブックマーク一覧を元に適当なブックマークを行うAIブックマーカーです。

## 使い方

### はてなアプリケーションの登録

下記の記事を参考にHATENA_CONSUMER_KEYとHATENA_CONSUMER_SECRETを取得し、.envファイルに登録します。
[Consumer key を取得して OAuth 開発をはじめよう | Hatena Developer Center](https://developer.hatena.ne.jp/ja/documents/auth/apis/oauth/consumer)

### OAuth認証

下記コマンドを実行し、HATENA_ACCESS_TOKENとHATENA_ACCESS_TOKEN_SECRETを取得し、.envファイルに登録します。  
エントリーの情報取得とブックマーク追加を行うため、scopeはread_public,write_publicが必要です。

```sh
docker compose run -it --rm app python oatuh.py
```

### AI人格の設定

config.pyに例を参考にAI人格を設定します。

### ブックマーク

下記コマンドを実行し、任意のURLに対してブックマークを行います。

```sh
docker compose run -it --rm app python bookmark.py http://example.com
```
