from discord.ext import commands  # Bot Commands Frameworkのインポート
# サーバー管理用cog

# コグとして用いるクラスを定義。


class Moderation(commands.Cog):

    # Moderationクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        pass


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Moderation(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
