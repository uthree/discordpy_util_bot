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
        await ctx.send(editor.get_view())
        
# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(Editor(bot))  # CogにBotを渡してインスタンス化し、Botにコグとして登録する。
