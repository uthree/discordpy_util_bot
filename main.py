import os
import yaml
import copy
import uuid

from discord.ext import commands
import discord as discord
import time

import savedata
import dataformats


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

        # SaveDataオブジェクトを初期化
        self._channel_data = savedata.SaveData(
            "./data/channel", default_data=dataformats.channel_data.ChannelData())
        self._user_data = savedata.SaveData(
            "./data/user", default_data=dataformats.user_data.UserData())
        self._server_data = savedata.SaveData(
            "./data/server", default_data=dataformats.server_data.ServerData())

        # コマンド実行中のユーザidを格納し、同時実行しないようにする。
        self.command_running_users = []

        # コマンド間で値を受け渡すためのメモリ(ユーザ別)
        self.command_memory = {}

    # セーブデータオブジェクトのプロパティ
    @property
    def channel_data(self):
        return self._channel_data

    @property
    def user_data(self):
        return self._channel_data

    @property
    def server_data(self):
        return self._server_data

    # Botの準備完了時に呼び出されるイベント

    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print('-----')

    def write_memory(self, ctx, data: str):
        self.command_memory[ctx.author.id] = data

    def read_memory(self, ctx):
        return self.command_memory[ctx.author.id]

    def reset_memory(self, ctx):
        self.command_memory[ctx.author.id] = ""

    async def on_message(self, message):
        await super().on_message(message)  # スーパークラスのon_messageを呼び出し。
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
                self.reset_memory(ctx)  # メモリをリセット
                commands = raw_command.split("\n")  # 改行で区切る
                # 進捗を辞書型に入れて、変化があり次第メッセージを更新する。
                progress = {}
                if len(commands) > 1:
                    progress_embed = await ctx.channel.send(embed=self.generate_progress_list(progress))
                i = 0
                for command_string in commands:
                    progress[i] = {
                        "command": command_string,
                        "status": "waiting",
                        "message": None,
                    }
                    i += 1

                # forで回して順番に実行
                i = 0
                for command_string in commands:
                    progress[i]["status"] = "running"
                    if len(commands) > 1:  # 複数件のコマンドの場合進捗を表示する
                        await progress_embed.edit(embed=self.generate_progress_list(progress))

                    if command_string == "":
                        continue
                    print(f"{command_string} を実行する。")
                    try:
                        await self.run_command(ctx, command_string)
                        progress[i]["status"] = "success"
                        progress[i]["message"] = f"完了 {self.read_memory(ctx)}"
                    except Exception as e:
                        print(type(e))
                        print(e)
                        progress[i]["status"] = "error"
                        progress[i]["message"] = "内部エラーが発生しました。"
                    if len(commands) > 1:  # 複数件のコマンドの場合進捗を表示する
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
            s += f"`{p['command']}` -> {p['message']} \n"
        return discord.Embed(title="進捗", description=s)

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
        for cmd in self.commands:
            print(cmd)
        pass


default_token_file = {
    'using': 'main',
    'main': '<YOUR BOT TOKEN HERE>'


}
if __name__ == "__main__":
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
            INITIAL_EXTENSIONS = yaml.safe_load(file)['cogs']
        # 内部的なprefixをuuidにしてわかりにくくする処理
        uuidpref = str(uuid.uuid4())
        print(f"prefix: {uuidpref}")

        # UtilBotのインスタンス化及び起動処理。
        bot = UtilBot(command_prefix=uuidpref)
        bot.run(token)  # Botのトークンを入れて実行


class CommandRunningError(Exception):
    pass
