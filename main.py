import os
import yaml
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
            "./data/userl", default_data=dataformats.user_data.UserData())
        self._server_data = savedata.SaveData(
            "./data/server", default_data=dataformats.server_data.ServerData())

    # セーブデータオブジェクトのプロパティ
    @property
    def channel_data(self):
        self._channel_data

    @property
    def user_data(self):
        self._channel_data

    @property
    def server_data(self):
        self._setver_data

    # Botの準備完了時に呼び出されるイベント

    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print('-----')

    async def on_message(self, message):
        await super().on_message(message)  # スーパークラスのon_messageを呼び出し。
        uuidpref_len = len(self.command_prefix)
        ctx = await self.get_context(message)

    # async def invoke(self, ctx):
    #     await super().invoke(ctx)
    #     print("invoke:")
    #     print(ctx)

    # async def process_commands(self, message):
    #     result = await super().process_commands(message)
    #     print("process_commands:")
    #     print(message)
    #     print(result)

    async def on_command_error(self, ctx, err):
        await ctx.send(f":no_entry: `{ctx.command}` -> `{err}`")

    # async def on_command_completion(self, ctx):
    #     await ctx.send(f":white_check_mark: `{ctx.command}`")


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
        uuidpref = str(uuid.uuid4()) + "!"
        print(f"prefix: {uuidpref}")

        # UtilBotのインスタンス化及び起動処理。
        bot = UtilBot(command_prefix=uuidpref)
        bot.run(token)  # Botのトークンを入れて実行
