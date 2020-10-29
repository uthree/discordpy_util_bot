from discord.ext import commands  # Bot Commands Frameworkのインポート
from mylibrary import texteditor
import re
import asyncio
# テキストエディタ cog

# コグとして用いるクラスを定義。
class Editor(commands.Cog):

    # Editorクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.editors = {} # エディタdict userid -> CUIEditor
    

    @commands.group(aliases=["edit", "textedit", "texteditor"])
    async def editor(self,ctx, filename=None):
        editor = texteditor.CUIEditor() #エディタを初期化
        self.editors[ctx.author.id] = editor # エディタdictに追加
        editor_message = await ctx.send(editor.get_view()) # エディタの初期画面を送信

        while editor.using:
            #メッセージの返信を待つ
            def check_message(message): 
                return message.channel == ctx.channel and message.author == ctx.author
            try:
                user_input_message = await self.bot.wait_for("message",timeout=600.0, check=check_message)
            except asyncio.TimeoutError: # タイムアウト時の処理
                print("TIMEOUT")
                editor.using = False
                await editor_message.delete()
                del self.editors[ctx.author.id] # エディタdictから削除
            else: #メッセージを受け取ったときの処理。
                content = user_input_message.content
                # "*"から始まるメッセージはエディタコマンドとみなす。
                
                if content[0] == ":":
                    cmd = content.split(" ")
                    
                    linemd = re.match("\:[a-z]?(\d+)", cmd[0]) #指定行に移動
                    if linemd:
                        editor.set_cursor_line(int(linemd[1])-1)
                    if re.match("\:o", cmd[0]): # 行上書きモード
                        editor.set_mode("overwrite_line")
                    if re.match("\:a", cmd[0]): # 行追加モード
                        editor.set_mode("add_line")
                    if re.match("\:i", cmd[0]): # 行挿入モード
                        editor.set_mode("insert_line")

                    if len(cmd) > 1: # エスケープ入力
                        editor.add_content(' '.join(cmd[1:])) # メッセージを追加

                else:
                    editor.add_content(user_input_message.content) # メッセージを追加
                await user_input_message.delete()#ユーザー側のメッセージを削除する
                await editor_message.edit(content=editor.get_view()) # エディタ画面を更新
    



        
# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(Editor(bot))  # CogにBotを渡してインスタンス化し、Botにコグとして登録する。
