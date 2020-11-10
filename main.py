import os
import yaml
import copy
import uuid
import time
import re
import datetime
import traceback
import asyncio

from discord.ext import commands
import discord as discord

from mylibrary import savedata
import dataformats

from mylibrary.exception import BotCommandException

class UtilBot(commands.Bot):
    # コンストラクタ
    def __init__(self, command_prefix):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix)

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

        # channeldataオブジェクトを初期化
        self._channel_data = savedata.SaveData(
            "./data/channel", default_data=dataformats.channel_data.ChannelData())
        # userdata
        self._user_data = savedata.SaveData(
            "./data/user", default_data=dataformats.user_data.UserData())
        # serverdata
        self._server_data = savedata.SaveData(
            "./data/server", default_data=dataformats.server_data.ServerData())

        # コマンド実行中のユーザidを格納し、同時実行しないようにする。
        self.command_running_users = []
        # ヘルプコマンドのデータを読み込み。
        with open('./help.yml') as file:
            self.help_data = yaml.safe_load(file)

        # コマンドの結果を格納するdict (message : str)
        self.command_results = {}

    # セーブデータオブジェクトのプロパティ
    @property
    def channel_data(self):
        return self._channel_data

    @property
    def user_data(self):
        return self._user_data

    @property
    def server_data(self):
        return self._server_data
    
    def set_command_result(self, ctx, result: str): # コマンドの結果を記載する。
        self.command_results[ctx.message.id] = result

    def get_command_result(self, ctx):
        if ctx.message.id in self.command_results:
            return self.command_results[ctx.message.id]
        else:
            return ""
    
    async def ask_choices(self, ctx, answers=[]): # 選択肢でユーザに質問する
        if len(answers) == 0: # 回答リストが空の場合
            answers = ["yes", "no"]
        def check_message(message):
            return message.author == ctx.author and message.channel == ctx.channel
        try:
            message = await self.wait_for('message', timeout=60.0, check=check_message)
        except asyncio.TimeoutError:
            pass
        else:
            #回答リストからマッチするものを検索
            for answer in answers:
                if type(answer) == re.Pattern:
                    if answer.match(message.content):
                        return answer
                elif type(answer) == str:
                    if answer == message.content:
                        return answer
                    if message.content in answer:
                        return answer
            #マッチしなかった場合
            return None


    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print('-----')

        # ゲームを変更。
        game = discord.Game("u!help")
        await self.change_presence(status=discord.Status.online, activity=game)

    async def adblock(self, message):  # ADBlock機能の動作。
        if re.match(r"(.+)discord.gg(.+)", message.content):  # サーバ宣伝を自動的に削除する。
            await message.delete()

    async def create_new_thread(self, message):  # スレッド作成
        ctx = await self.get_context(message)
        category = message.channel.category
        # 更新のないスレッドを削除
        channels = category.text_channels
        if len(channels) > 20:  # チャンネル数が多いときは
            for channel in channels:
                # 7日以上前が最終発言のスレッドを削除する。
                if (datetime.datetime.now(datetime.timezone.utc) - channel.last_message.created_at).days > 7:
                    await channel.delete()
        # 新規作成
        await category.create_text_channel(message.content)

    async def on_message(self, message):
        if type(message.channel) == discord.DMChannel:
            return 
        await super().on_message(message)  # スーパークラスのon_messageを呼び出し。
        # ADBlock config
        if self._channel_data.read(message.channel.id).config.get_config("adblock").value == True:
            await self.adblock(message)
        # thread creator config
        if self._channel_data.read(message.channel.id).config.get_config("thread_creator").value == True:
            await self.create_new_thread(message)

        if not message.author.id in self.command_running_users:
            self.command_running_users.append(
                message.author.id)  # コマンド実行中のユーザに追加

            ctx = await self.get_context(message)
            # prefixを読み込み
            prefixes = self.server_data.read(ctx.guild.id).prefixes
            raw_command = ""
            for pref in prefixes:  # どれかのプレフィックスにマッチするものがあれば、プレフィックスを排除した文字列を抽出。
                if ctx.message.content[0: len(pref)] == pref:
                    raw_command = ctx.message.content[len(pref):]
                    break
            if not raw_command == "":
                # commandを実行する
                commands = re.split("\n", raw_command)  # 改行で区切る
                # 進捗を辞書型に入れて、変化があり次第メッセージを更新する。
                progress = {}
                progress_embed = await ctx.channel.send(embed=self.generate_progress_list(progress))
                i = 0
                for command_string in commands:
                    progress[i] = {
                        "command": command_string,
                        "status": "waiting",
                        "message": "",
                    }
                    i += 1

                # forで回して順番に実行
                i = 0
                for command_string in commands:
                    progress[i]["status"] = "running"
                    await progress_embed.edit(embed=self.generate_progress_list(progress))

                    if command_string == "":
                        continue
                    #print(f"{command_string} を実行する。")
                    try:
                        # コマンドの結果を格納するメッセージを送信
                        await self.run_command(ctx, command_string)
                        progress[i]["status"] = "success"
                        progress[i]["message"] = f" {self.get_command_result(ctx)} "
                    except BotCommandException as e:
                        progress[i]["status"] = "warning"
                        progress[i]["message"] = str(e)
                    except Exception as e:
                        self.set_command_result(ctx, traceback.format_exc(limit=5))
                        traceback.print_exc()
                        progress[i]["status"] = "error"
                        progress[i]["message"] = f"内部エラーが発生しました\n ```\n{self.get_command_result(ctx)}\n```"
                        # 未知のコマンドの場合はエラーを出す。
                    await progress_embed.edit(embed=self.generate_progress_list(progress))
                    time.sleep(1)
                    i += 1

            self.command_running_users.remove(
                message.author.id)  # コマンド実行中のユーザから削除

    def generate_progress_list(self, progress):
        s = ""
        for k, p in progress.items():
            status = p["status"]
            if status == "waiting":
                s += ":stop_button: "
            elif status == "running":
                s += ":arrow_forward: "
            elif status == "success":
                s += ":white_check_mark: "
            elif status == "warning":
                s += ":warning: "
            elif status == "error":
                s += ":red_circle: "
            s += f"`{p['command']}` \n{p['message']} \n\n"
        return discord.Embed(title="Commands", description=s)

    async def run_command(self, ctx, command_string):  # 任意のコマンドを実行
        splited_chain = command_string.split(' ')
        if splited_chain[0] == 'help':
            keywords = splited_chain[1:]
            await self.__help_command__(ctx, keywords)
        else:
            msg = copy.copy(ctx.message)
            msg.content = self.command_prefix + command_string
            new_ctx = await self.get_context(msg, cls=type(ctx))
            await new_ctx.reinvoke()

    async def __help_command__(self, ctx, keywords):  # ヘルプコマンド処理
        results = {}  # 検索結果
        kw_join = " ".join(keywords)  # キーワードの結合
        result_string = ""  # 検索結果を文字列にする。
        for key, value in self.help_data.items():
            if len(results) > 5:  # 長すぎる場合は省略
                break
            for kw in reversed(keywords):
                if kw in value.get("description", ""):  # コマンド概要内にキーワードが含まれていれば検索結果に追加。
                    results[key] = value
            if key in kw_join:  # ヘルプデータ内にコマンドのkeyがあれば追加。
                results[key] = value
        for key, value in results.items():  # 検索結果を文字列にする。
            result_string += f"__{key}__\n"
            result_string += "```css\n"
            result_string += f"概要: {value.get('description', '不明')}\n"

            # prefixを読み込み
            prefix = self.server_data.read(ctx.guild.id).prefixes[0]
            # 使用方法を取得
            usage = value.get('usage', None)
            if usage:
                result_string += f"使用方法: {prefix}{usage}\n"
            result_string += "```\n\n"
        if len(results) > 0:  # 結果があった場合のみ出力。
            embed = discord.Embed(title="検索結果", description=result_string)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=":red_circle: 検索失敗",
                                  description="`help <キーワード>` で検索できます。 パラメータに誤りがないか確認してください。")
            await ctx.send(embed=embed)


default_token_file = {
    'using': 'main',
    'main': '<YOUR BOT TOKEN HERE>'


}

def main():
    if not os.path.exists("token.yml"):
        # トークンファイルがない場合は自動的に作成。
        with open("token.yml", "w") as file:
            yaml.dump(default_token_file, file)
            print(
                """
                token.ymlファイルを編集して、botトークンを追加してください。
                デフォルトでは main: 項目に追加することでbotが使用可能になります。
                """
            )
            exit()
    else:
        # トークン読み込み処理
        with open("token.yml") as file:
            token_data = yaml.safe_load(file)
        using_token = token_data['using']
        token = token_data[using_token]
        print(f"{using_token} のトークンを使用します。")

        # cog読み込み処理
        with open("load_cogs.yml") as file:
            global INITIAL_EXTENSIONS
            INITIAL_EXTENSIONS = yaml.safe_load(file)['cogs']
        # 内部的なprefixをuuidにしてわかりにくくする処理
        uuidpref = str(uuid.uuid4())
        print(f"prefix: {uuidpref}")

        # UtilBotのインスタンス化及び起動処理。
        bot = UtilBot(command_prefix=uuidpref)
        bot.run(token)  # Botのトークンを入れて実行

if __name__ == "__main__":
    main()

