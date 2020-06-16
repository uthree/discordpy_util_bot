from discord.ext import commands  # Bot Commands Frameworkのインポート
import othello as othellolib

# コグとして用いるクラスを定義。


class Othello(commands.Cog):

    # Utilitesクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.boards = {}

    @commands.group()
    async def othello(self, ctx):
        pass  # TODO: オセロコマンドを実装して、遊べるようにする。

    @othello.command()
    async def start(self, ctx):
        if not ctx.channel.id in self.boards:  # 新規にオセロを開始
            self.boards[ctx.channel.id] = {
                'board': othellolib.Board(),
                'now': 1,  # 黒のターン
                'black': ctx.author.id,
                'white': None,
            }
            await ctx.send(
                f"<@{ctx.author.id}> あなたは黒です。\nオセロの対戦相手を募集します。参加する場合は`othello start` コマンドを入力してください。")
        else:  # すでに開始しているオセロに参加
            self.boards[ctx.channel.id]['white'] = ctx.author.id
            await ctx.send(f"<@{ctx.author.id}> オセロに白で参加しました。")
            await ctx.send(self.boards[ctx.channel.id]
                           ['board'].get_board_discord_emojis())

    @othello.command()
    async def put(self, ctx):
        pass

# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(Othello(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
