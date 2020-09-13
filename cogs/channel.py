from discord.ext import commands  # Bot Commands Frameworkのインポート
# チャンネル管理cog

# コグとして用いるクラスを定義。


class Channels(commands.Cog):

    # Channelsクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        pass

    @commands.group
    def channel(self, ctx):  # channel 系コマンド。
        pass

        # Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(Channels(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
