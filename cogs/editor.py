import asyncio
import re

from discord.ext import commands  # Bot Commands Frameworkのインポート

from mylibrary.filesystem import *
from mylibrary import texteditor
from mylibrary.exception import BotCommandException

# テキストエディタ cog

# コグとして用いるクラスを定義。
class Editor(commands.Cog):

    # Editorクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.editors = {} # エディタdict userid -> CUIEditor
    

    @commands.group(aliases=["edit", "textedit", "texteditor"])
    async def editor(self, ctx, filename="new_file"):
        editor = texteditor.CUIEditor() #エディタを初期化
        self.editors[ctx.author.id] = editor # エディタdictに追加
        ud = self.bot.user_data.read(ctx.author.id)

        if filename: # ファイル読み込み, 存在しなければ新規作成の処理
            data = []
            try:
                f = ud.filesystem.get_content(filename)
                data = ud.filesystem.get_content(filename).text.split("\n")
            except BotCommandException:
                pass
            filepath = ud.filesystem.current_path
            editor.instances[0].lines = data
            editor.instances[0].directory_path = filepath
            editor.instances[0].file_name = filename

        editor_message = await ctx.send(editor.get_view()) # エディタの初期画面を送信
        while editor.using:
            #メッセージの返信を待つ
            def check_message(message): 
                return message.channel == ctx.channel and message.author == ctx.author
            try:
                user_input_message = await self.bot.wait_for("message",timeout=600.0, check=check_message)
            except asyncio.TimeoutError: # タイムアウト時の処理
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
                    if re.match("\:d", cmd[0]): # 行削除
                        editor.delete_line()
                    if re.match("\:q", cmd[0]): # エディタ終了
                        editor.quit_editor()
                    if re.match("\:w", cmd[0]): # 保存
                        fs = ud.filesystem
                        editor.write_file(fs, ctx.author)
                        self.bot.user_data.write(ctx.author.id, ud) # ユーザーデータを保存
                    if re.match("\:r", cmd[0]) and len(cmd) >= 1: #読み込み
                        fs = ud.filesystem
                        editor.read_file(fs, cmd[1])
                    md = re.match("\:c(\d+)", cmd[0])
                    if md: # 編集ファイル切り替え
                        editor.change_edit_file(int(md[1]))
                    if re.match("\:wq", cmd[0]): # 保存して終了
                        fs = ud.filesystem
                        editor.write_file(fs, ctx.author)
                        self.bot.user_data.write(ctx.author.id, ud) # ユーザーデータを保存
                        editor.quit_editor()

                    if len(cmd) > 1 : # エスケープ入力
                        editor.add_content(' '.join(cmd[1:])) # メッセージを追加

                else:
                    editor.add_content(user_input_message.content) # メッセージを追加
                await user_input_message.delete()#ユーザー側のメッセージを削除する
                await editor_message.edit(content=editor.get_view()) # エディタ画面を更新
        await editor_message.delete()
        self.bot.user_data.write(ctx.author.id, ud) # ユーザーデータを保存
    



        
# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(Editor(bot))  # CogにBotを渡してインスタンス化し、Botにコグとして登録する。
