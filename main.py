import os
import yaml
import copy
import uuid

from discord.ext import commands

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
                commands = raw_command.split("\n")  # 改行で区切る
                for command_chain in commands:
                    print(f"{command_chain} を実行する。")
                    await self.run_command(ctx, command_chain)

            self.command_running_users.remove(
                message.author.id)  # コマンド実行中のユーザから削除

    async def run_command(self, ctx, command_chain):  # 任意のコマンドを実行
        msg = copy.copy(ctx.message)
        msg.content = self.command_prefix + command_chain
        new_ctx = await self.get_context(msg, cls=type(ctx))
        await new_ctx.reinvoke()


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
