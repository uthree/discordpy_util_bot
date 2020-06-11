from discord.ext import commands  # Bot Commands Frameworkのインポート

# コグとして用いるクラスを定義。


class Ping(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')

# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(Ping(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
