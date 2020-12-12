from discord.ext import commands  # Bot Commands Frameworkのインポート
import discord as discord
import random
# ネタ系コマンド cog

# コグとして用いるクラスを定義。


class Fun(commands.Cog):

    # Funクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["sintyoku"])
    def sintyoku(self,ctx):
        links = [
            "https://cdn.discordapp.com/attachments/708828790796845189/787409537883439134/alicedoudesuka-300x168.jpg"
        ]
        ctx.send(random.choice(links))
    


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Fun(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
