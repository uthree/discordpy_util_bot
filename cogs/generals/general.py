from discord.ext import commands  # Bot Commands Frameworkのインポート
import discord as discord

# コグとして用いるクラスを定義。


class General(commands.Cog):

    # Utilitesクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # doコマンド。 直前のメモリを引数にコマンドを実行する。
    @commands.command()
    async def do(self, ctx, *chain):
        mem = self.bot.read_memory(ctx)
        await self.bot.run_command(ctx, ' '.join(chain) + ' ' + mem)

    # resetmemコマンド。 メモリをリセットする
    @commands.command()
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
    async def say(self, ctx, msg):
        print(msg)
        await ctx.send(str(msg))

    @commands.group()
    async def user(self, ctx):
        pass

    @user.command(aliases=['s'])
    async def select(self, ctx, *selectors):
        members = ctx.guild.members
        for selector in selectors:
            selector = selector.split("=")
            selector_prefix = selector[0]
            selector_suffix = selector[1]
            if selector_prefix == "id":
                members = [m for m in members if m.id == int(selector_suffix)]
        self.bot.write_memory(ctx, ' '.join([str(m.id) for m in members]))

    @user.command(aliases=['i'])
    async def info(self, ctx, *users: commands.MemberConverter):
        for user in users:
            embed = discord.Embed(
                title=str(user), description=f"ID: {user.id}")
            embed.color = user.color

            # まずは大まかな情報を表示する

            # ステータス表示処理
            status = user.status
            status_string = ":purple_circle: 不明"
            if status == discord.Status.dnd:
                status_string = ":red_circle: 取り込み中"
            elif status == discord.Status.idle:
                status_string = ":yellow_circle: 離席中"
            elif status == discord.Status.online:
                status_string = ":green_circle: オンライン"
            elif status == discord.Status.offline:
                status_string = ":black_circle: オフライン"
            if user.is_on_mobile():
                status_string += " (モバイル)"
            embed.add_field(name="状態", value=status_string)

            # ニックネーム表示処理
            embed.add_field(name="ニックネーム", value=user.nick)

            # 細かい情報
            roles_string = "```\n"
            for role in user.roles:
                roles_string += f"{role.name}\n"
            roles_string += "```"
            embed.add_field(name="役職", value=roles_string, inline=False)

            #　参加日表示処理
            joined_at = user.joined_at
            embed.add_field(
                name="参加日", value=f"{joined_at.year}/{joined_at.month}/{joined_at.day}",)

            created_at = user.created_at
            embed.add_field(
                name="アカウント作成日", value=f"{created_at.year}/{created_at.month}/{created_at.day}",)

            # アイコン設定
            embed.set_thumbnail(url=user.avatar_url)

            await ctx.send(embed=embed)

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
    bot.add_cog(General(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
