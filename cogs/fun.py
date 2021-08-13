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
    async def sinchoku(self,ctx):
        links = [
            "https://cdn.discordapp.com/attachments/708828790796845189/787409537883439134/alicedoudesuka-300x168.jpg",
            "https://cdn.discordapp.com/attachments/787413181277798400/787413202958417920/images-6.jpeg",
            "https://cdn.discordapp.com/attachments/787413181277798400/787413219085647872/images-5.jpeg",
            "https://cdn.discordapp.com/attachments/787413181277798400/787413268872429568/images.jpeg",
            "https://cdn.discordapp.com/attachments/787413181277798400/787413301776089118/main.pngcompresstrue.png",
            "https://cdn.discordapp.com/attachments/787413181277798400/787413247686737930/images-3.jpeg"
        ]
        await ctx.send(random.choice(links))

    @commands.command(aliases=["sintyoku_dame"])
    async def sinchoku_dame(self,ctx):
        links = [
                "https://ghippos.net/image/blog/20131008_1.jpg",
                "https://livedoor.blogimg.jp/tank_make/imgs/a/9/a996bd7c.jpg",
                "https://d2dcan0armyq93.cloudfront.net/photo/odai/400/8a1b02cea77695724af97b596cbc5acc_400.jpg"
                ]
        await ctx.send(random.choice(links))

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Fun(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
