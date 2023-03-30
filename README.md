# AIはてなブックマーカー

## これはなに

Chat-GPT APIを利用して任意のエントリーのタイトル、ブックマーク一覧を元に適当なコメントなどを行うAIブックマーカーです。

## 使い方

### はてなアプリケーションの登録

下記の記事を参考にHATENA_CONSUMER_KEYとHATENA_CONSUMER_SECRETを取得し、.envファイルに登録します。
[Consumer key を取得して OAuth 開発をはじめよう | Hatena Developer Center](https://developer.hatena.ne.jp/ja/documents/auth/apis/oauth/consumer)

### AI人格の設定

config.pyの例を参考にAI人格を設定します。

### ブックマーク

下記コマンドを実行すると、任意のURLに対してブックマークを行います。

```sh
docker compose run -it --rm app python entry.py http://example.com
```

### ホットエントリーの記事をランダムにブックマーク

下記コマンドを実行すると、ホットエントリーの記事をランダムに5件ブックマークします。

```sh
docker compose run -it --rm app python hotentry.py
```

### 本ライブラリを利用しているアカウント例

#### 一番星はての

※本実装を初期実装として利用していますがこのコードで動いているわけではなく独立したコードで改修が行われています  

[firststar_hatenoのブックマーク - はてなブックマーク](https://b.hatena.ne.jp/firststar_hateno/bookmark)  
