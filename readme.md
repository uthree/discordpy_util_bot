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

```
u!user select id=405609119106727937
do user info
```

コマンドは複数行に分けて書くと、順番に実行されます。
do コマンドは、任意のコマンドの後ろに、直前のコマンドの出力を付け足します。

# todo

- [x] 独自のコマンドシステム(prefix 可変)を完成させる

  - [ ] 複雑な構文解析を作る
  - [ ] main.py の作り直し
    - [ ] コマンドの同期/非同期処理

- [x] prefix の後に、コマンドを改行区切りで送信することで、コマンドを順番に実行できるようにする
- [ ] とりあえずコマンド部分を普通のに戻す
- [ ] チャンネルを編集する系のコマンドを作ってみる
- [x] ヘルプコマンドを作る

# 参考にさせていただいた記事

- [discord.py の Bot Commands Framework を用いた Bot 開発](https://qiita.com/Lazialize/items/81f1430d9cd57fbd82fb)
- [Discord.py 公式ドキュメント](https://discordpy.readthedocs.io/ja/latest/)

# 開発に用いた環境

- Python 3.8.0
- macOS 10.15.5
