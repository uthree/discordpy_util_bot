from discord.ext import commands  # Bot Commands Frameworkのインポート
import discord as discord
from mylibrary.filesystem import Directory
from mylibrary.filesystem import TextFile
from mylibrary.filesystem import *

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

    #進捗管理系
    # taskコマンド 現在のタスクを表示する
    @commands.group()
    async def task(self, ctx):
        pass

    # task add コマンド
    async def add(self, ctx, task_name, deadline):
        pass

        
# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(General(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
