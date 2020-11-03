# 多機能 bot

少数サーバー上で動かす便利機能を詰め込んだ bot。
一部は[自鯖](https://discord.gg/JBKuUHh)用

# 実行方法

1. このリポジトリをクローンする。

2. 依存しているライブラリをインストール

```bash
pip install -r requirements.txt
```

3. python コマンドで main.py を実行する。 すると自動的に token.yml が生成されてプログラムが終了する

```bash
python main.py
```

4. 自分の bot トークンを生成された token.yml の main: 項に貼り付ける

```yml
main: ここにトークンを貼り付ける
using: main # main項目のトークンを使う設定。
```

5. もう一度 python コマンドで main.py を実行する。

```bash
python main.py
```

# コマンドの仕組み・使い方

デフォルトのプレフィックスは `u!` です。

```
u!ping
```

これで`pong!`と帰ってきます。

```
u!prefix <新しいプレフィックス>
```

コマンドのプレフィックスを変更できます。


# todo

- [x] 独自のコマンドシステム(prefix 可変)を完成させる

  - [ ] 複雑な構文解析を作る(linux のシェルみたいな感じ)
  - [ ] main.py の作り直しまたは リファクタリング
    - [ ] コマンドの同期/非同期処理

- [x] prefix の後に、コマンドを改行区切りで送信することで、コマンドを順番に実行できるようにする
- [ ] チャンネルを編集する系のコマンドを作ってみる
- [ ] サーバ管理系コマンド
  - [ ]「実績」: ユーザーの発言や行動に応じて「実績解除！」みたいな感じのメッセージを出す
  - [ ] ユーザ数の増減やチャンネルの使用率のアナリティクス
- [x] ヘルプコマンドを作る

- [ ] 電卓機能 (括弧が使用可能, 計算の優先順位を考慮)
- [ ] wikipedia 検索
- [ ] worfarm alpha の API を使う

# 参考にさせていただいた記事

- [discord.py の Bot Commands Framework を用いた Bot 開発](https://qiita.com/Lazialize/items/81f1430d9cd57fbd82fb)
- [Discord.py 公式ドキュメント](https://discordpy.readthedocs.io/ja/latest/)

# 開発に用いた環境

- Python 3.9.0
- macOS 10.15.5
