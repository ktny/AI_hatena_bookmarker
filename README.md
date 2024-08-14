# AIはてなブックマーカー

![ex. 一番星はてのインフラ構成図](./ARCHITECTURE.svg)

OpenAI APIを利用して任意のはてなブックマークエントリーの記事やブックマークを元にコメントを行うAIブックマーカーを作ることのできるシステムです。  
（上記は参考構成図です。一番星はてのはこのリポジトリを元にした別のリポジトリで運用されています。）

## 使い方

### はてなアプリケーションの登録

下記の記事を参考にHATENA_CONSUMER_KEYとHATENA_CONSUMER_SECRETを取得し、.envファイルに記載します。
[Consumer key を取得して OAuth 開発をはじめよう | Hatena Developer Center](https://developer.hatena.ne.jp/ja/documents/auth/apis/oauth/consumer)

その他OpenAIのAPIKeyの設定なども必要です。

## AI人格の設定

[config.py](src/libs/common/config.py)や[prompt_template.py](src/libs/util/llm/prompt_template.py)にAIの設定や人格、指示を記述します。

## ビルド&デプロイ

```bash
sam build
sam deploy --guided
```

## テスト

### SAM

```bash
$ sam local invoke AIBookmarkerFunction --event events/get_hello.json
```

### Lambda

```bash
$ sam local start-lambda
$ aws lambda invoke --function-name "AIBookmarkerFunction" --endpoint-url "http://127.0.0.1:3001" --payload file://events/get_hello.json response.json && cat response.json
```

### HTTP API

```bash
$ sam local start-api
$ curl http://localhost:3000/hello
```
