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
        if key == "adblock":
            if value == "true":
                cdata = self.bot._channel_data.read(ctx.channel.id)
                cdata.adblock = True
                self.bot._channel_data.write(ctx.channel.id, cdata)
                self.bot.set_command_result(ctx,"宣伝ブロックが**有効**になりました。")
            elif value == "false":
                cdata = self.bot._channel_data.read(ctx.channel.id)
                cdata.adblock = False
                self.bot._channel_data.write(ctx.channel.id, cdata)
                self.bot.set_command_result(ctx,"宣伝ブロックが**無効**になりました。")
            else:
                cdata = self.bot._channel_data.read(ctx.channel.id)
                self.bot.set_command_result(ctx,f"true/falseで指定してください。\n 現在は{cdata.adblock}")
        elif key == "thread":
            if value == "true":
                cdata = self.bot._channel_data.read(ctx.channel.id)
                cdata.thread_creator = True
                self.bot._channel_data.write(ctx.channel.id, cdata)
                self.bot.set_command_result(ctx,"このカテゴリをスレッド用にし、このチャンネルをスレッド作成用チャンネルにしました。")
            elif value == "false":
                cdata = self.bot._channel_data.read(ctx.channel.id)
                cdata.thread_creator = False
                self.bot._channel_data.write(ctx.channel.id, cdata)
                self.bot.set_command_result(ctx,"スレッドの設定を解除しました。")
            else:
                cdata = self.bot._channel_data.read(ctx.channel.id)
                self.bot.set_command_result(ctx,f"true/falseで指定してください。\n 現在は{cdata.adblock}")
        else:
            self.bot.set_command_result(ctx,f"コンフィグ `{key}`は存在しません。")
    
    @channel.command() # チャットログ取得コマンド(WIP)
    async def get_chatlog(self, ctx): #todo: これを完成させる
        async for message in ctx.channel.history(limit=10):
            print(message.content)


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Channel(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
