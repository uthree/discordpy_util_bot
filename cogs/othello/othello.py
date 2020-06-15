from discord.ext import commands  # Bot Commands Frameworkのインポート
import othello

# コグとして用いるクラスを定義。


class Othello(commands.Cog):

    # Utilitesクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot


# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(Othello(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
