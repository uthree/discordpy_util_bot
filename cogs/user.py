from discord.ext import commands  # Bot Commands Frameworkのインポート
import discord as discord
# ユーザー管理用cog

# コグとして用いるクラスを定義。


class User(commands.Cog):

    # Userクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def user(self, ctx):
        pass

    @user.command(aliases=['s', 'sel'])
    async def select(self, ctx, *selectors):
        members = ctx.guild.members
        for selector in selectors:
            selector = selector.split("=")
            selector_prefix = selector[0]
            selector_suffix = selector[1]
            if selector_prefix == "id":
                members = [m for m in members if m.id == int(selector_suffix)]
            elif selector_prefix == "role_id":
                members = [m for m in members if ctx.guild.get_role(
                    int(selector_suffix)) in m.roles]
            elif selector_prefix == "name":
                members = [m for m in members if m.name == selector_suffix]
            else:
                continue
        self.bot.write_memory(ctx, ' '.join([str(m.id) for m in members]))

    @user.command(aliases=['i', 'infomation'])
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


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(User(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
