import os

from discord.ext import commands  # Bot Commands Frameworkのインポート
import discord as discord

from mylibrary.filesystem import *
# ファイルシステム系のCog

# コグとして用いるクラスを定義。
class File(commands.Cog):

    # Fileクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pwd(self, ctx): #現在のディレクトリを確認
        ud = self.bot.user_data.read(ctx.author.id) # load
        self.bot.set_command_result(ctx, f"{ud.filesystem.current_path}")
    
    @commands.command()
    async def cd(self, ctx, path): #カレントディレクトリを変更
        ud = self.bot.user_data.read(ctx.author.id) #load
        ud.filesystem.cd(path)
        self.bot.set_command_result(ctx, f":file_folder: {ud.filesystem.current_path} に移動しました。")
        self.bot.user_data.write(ctx.author.id, ud) #save

    @commands.command()
    async def mkdir(self, ctx, dirname): # 新規ディレクトリを作成。
        ud = self.bot.user_data.read(ctx.author.id) #load
        ud.filesystem.mkdir(dirname)
        self.bot.set_command_result(ctx, f"ディレクトリ :file_folder: {dirname} を作成しました。")
        self.bot.user_data.write(ctx.author.id, ud) #save

    @commands.command() # カレントディレクトリの中身を列挙。
    async def ls(self, ctx):
        ud = self.bot.user_data.read(ctx.author.id) #load
        fs = ud.filesystem
        s = ""
        for content in fs.current_directory.contents:
            if type(content) == Directory:
                s += f":file_folder: {content.name}/\n"
            else:
                s += f":page_facing_up: {content.name}\n"
        
        self.bot.set_command_result(ctx, s)
    
    @commands.command()
    async def rm(self, ctx, path): #特定のファイルまたはディレクトリを削除する
        ud = self.bot.user_data.read(ctx.author.id)
        fs = ud.filesystem
        content = fs.get_content(path)
        content.parent.remove_content(content)
        self.bot.user_data.write(ctx.author.id, ud)
        self.bot.set_command_result(ctx, f"{content.path} を削除しました。")
    
    @commands.command()
    async def export(self, ctx, path): #ファイルを出力する
        ud = self.bot.user_data.read(ctx.author.id)
        fs = ud.filesystem
        content = fs.get_content(path)
        if type(content) == TextFile:
            s = content.text
            with open(f"./{ctx.author.id}.txt", mode="w") as f:
                f.write(s)
            await ctx.send(file=discord.File(f"./{ctx.author.id}.txt"))
            os.remove(f"./{ctx.author.id}.txt")
        else:
            raise BotCommandException(f"{path}はディレクトリです。")

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(File(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
