from discord.ext import commands  # Bot Commands Frameworkのインポート
# チャンネル管理cog

# コグとして用いるクラスを定義。


class Channel(commands.Cog):

    # Channelクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        pass

    @commands.group()
    async def channel(self, ctx):  # channel 系コマンド。
        pass

    @channel.command()
    async def select(self, ctx, *selectors):  # チャンネルを選択。
        pass

# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(Channel(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
