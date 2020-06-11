from discord.ext import commands  # Bot Commands Frameworkのインポート

# コグとして用いるクラスを定義。


class InitServer(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    def on_message(self, ctx):
        print(ctx)

# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(InitServer(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
