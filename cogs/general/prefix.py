from discord.ext import commands  # Bot Commands Frameworkのインポート

# コグとして用いるクラスを定義。


class Prefix(commands.Cog):

    # クラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx, *prefixes):
        prefixes = list(prefixes)
        if len(prefixes) < 1:
            raise "prefixを1つ以上指定してください。"
        else:
            print(self.bot.server_data)
            data = self.bot.server_data.read(ctx.guild.id)
            data.prefixes = prefixes
            self.bot.server_data.write(ctx.guild.id, data)
            await ctx.send(f":white_check_mark: プレフィックスを変更しました: `{str(prefixes)}`")

    # Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
    bot.add_cog(Prefix(bot))
