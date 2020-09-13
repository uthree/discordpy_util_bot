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

    # doコマンド。 直前のメモリを引数にコマンドを実行する。
    @commands.command()
    async def do(self, ctx, *chain):
        mem = self.bot.read_memory(ctx)
        await self.bot.run_command(ctx, ' '.join(chain) + ' ' + mem)

    # resetmemコマンド。 メモリをリセットする
    @commands.command(aliases=["reset", "init"])
    async def resetmem(self, ctx):
        self.bot.reset_memory(ctx)

    # stringコマンド。メモリに任意の文字列をのせる
    @commands.command()
    async def string(self, ctx, s: str):
        self.bot.write_memory(ctx, s)

    # pingコマンド
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')

    # sayコマンド
    @commands.command()
    async def say(self, ctx, *msg: str):
        print(msg)
        await ctx.send(' '.join(msg))


# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(General(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
