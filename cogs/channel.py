from discord.ext import commands  # Bot Commands Frameworkのインポート
# チャンネル管理cog

# コグとして用いるクラスを定義。


class Channel(commands.Cog):

    # Channelクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def channel(self, ctx):  # channel 系コマンド。
        pass

    @channel.command()
    async def select(self, ctx, *selectors):  # チャンネルを選択。
        pass

    @channel.command()
    @commands.has_permissions(manage_guild=True)  # 管理権限が必要
    async def config(self, ctx, key=None, value=None):
        cd = self.bot.channel_data.read(ctx.channel.id)
        if key:
            if value:
                cd.config.set_config(key, value)
                self.bot.set_command_result(ctx, f"{key} を `{cd.config.get_config(key).value}` に設定しました。")
            else:
                cd.config.get_config(key)
                self.bot.set_command_result(ctx, f"{key} : `{cd.config.get_config(key).value}`")
        else:
            self.bot.set_command_result(ctx, cd.config.get_view())
        self.bot.channel_data.write(ctx.channel.id, cd)
    
    @channel.command() # チャットログ取得コマンド(WIP)
    async def get_chatlog(self, ctx): #todo: これを完成させる
        async for message in ctx.channel.history(limit=10):
            print(message.content)


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Channel(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
