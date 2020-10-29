from discord.ext import commands  # Bot Commands Frameworkのインポート
import discord as discord

# コグとして用いるクラスを定義。


class General(commands.Cog):

    # Utilitesクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # repository コマンド。 このbotのソースがあるリポジトリ を表示する。
    @commands.command()
    async def repository(self, ctx):
        await ctx.send("https://github.com/uthree/discordpy_util_bot")

    # pingコマンド
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')

    # sayコマンド
    @commands.command()
    async def say(self, ctx, *msg: str):
        m = ' '.join(msg)
        # 全体メンションは無効化
        m.replace('@everyone', '')
        m.replace('@here', '')
        await ctx.send(m)

    @commands.command()
    async def pwd(self, ctx): #現在のディレクトリを確認
        ud = self.bot.user_data.read(ctx.author.id)
        self.bot.set_command_result(f"{ctx, ud.filesystem.current_path}")

# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(General(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
