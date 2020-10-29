from discord.ext import commands  # Bot Commands Frameworkのインポート
from mylibrary import texteditor
# テキストエディタ cog

# コグとして用いるクラスを定義。
class Editor(commands.Cog):

    # Editorクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["editor", "textedit", "texteditor"])
    async def edit(self,ctx, filename=None):
        editor = texteditor.CUIEditor()
        editor_message = await ctx.send(editor.get_view())

        while editor.using:

            #メッセージの返信を待つ
            def check_message(message): 
                return message.channel == ctx.channel and message.author == ctx.author
            try:
                user_input_message = await self.bot.wait_for("message",timeout=60, check=check_message)
            except asyncio.TimeoutError: # タイムアウト時の処理
                editor.using = False
                editor_message.delete()
            else: #メッセージを受け取ったときの処理。
                editor.add_content(user_input_message.content) # メッセージを追加
                await editor_message.edit(content=editor.get_view()) # エディタ画面を更新



        
# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(Editor(bot))  # CogにBotを渡してインスタンス化し、Botにコグとして登録する。
