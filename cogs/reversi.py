from discord.ext import commands  # Bot Commands Frameworkのインポート
import reversi as reversilib
import re

# コグとして用いるクラスを定義。


class Reversi(commands.Cog):

    # Reversiクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.boards = {}
        self.alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    @commands.group()
    async def reversi(self, ctx):
        pass

    @reversi.command()
    async def start(self, ctx):
        if not ctx.channel.id in self.boards:  # 新規にreversiを開始
            self.boards[ctx.channel.id] = {
                'board': reversilib.Board(),
                'now': 1,  # 黒のターン
                'black': ctx.author.id,
                'white': None,
            }
            await ctx.send(
                f"<@{ctx.author.id}> あなたは黒です。\nリバーシの対戦相手を募集します。参加する場合は`reversi start` コマンドを入力してください。")
        else:  # すでに開始しているリバーシに参加
            self.boards[ctx.channel.id]['white'] = ctx.author.id
            await ctx.send(f"<@{ctx.author.id}> リバーシに白で参加しました。")
            await ctx.send(f"<@{self.boards[ctx.channel.id]['black']}> 黒のターンです。")
            await ctx.send(self.boards[ctx.channel.id]
                           ['board'].get_board_discord_emojis())

    @reversi.command(aliases=['exit', 'end', 'leave'])  # リバーシを終了する。
    async def stop(self, ctx):
        del self.boards[ctx.channel.id]

    @reversi.command()
    async def put(self, ctx, pos):
        # 座標を特定する
        y = int(re.sub("\\D", "", str(pos))) - 1
        x = 0
        for a in self.alphabets:
            if a in pos:
                x = self.alphabets.index(a)
        # 設置する
        print(x, y)
        board_data = self.boards[ctx.channel.id]
        if board_data['board'].check_can_put(board_data['now'], x, y):
            board_data['board'].put(board_data['now'], x, y)
            # 次のターンは白黒どちらかを判定する
            if board_data['now'] == 1:  # さっき黒だったなら
                if board_data['board'].check_can_put_any(2):  # 白が設置可能なら
                    board_data['now'] = 2  # 次のターンは白
                else:
                    board_data['now'] = 1  # 次のターンは黒
            elif board_data['now'] == 2:  # さっき白だったなら
                if board_data['board'].check_can_put_any(1):  # 黒が設置可能なら
                    board_data['now'] = 1  # 次のターンは黒
                else:
                    board_data['now'] = 2  # 次のターンは白
            # ボード送信
            await ctx.send(board_data['board'].get_board_discord_emojis(color=board_data['now']))
            if board_data['board'].winner() != None:
                if board_data['board'].winner() == 1:  # black
                    await ctx.send(f":tada: 黒 <@{board_data['black']}> の勝利です。")
                elif board_data['board'].winner() == 2:  # white
                    await ctx.send(f":tada: 白 <@{board_data['white']}> の勝利です。")
                elif board_data['board'].winner() == 3:  # draw
                    await ctx.send(f"引き分けです！！！")
                # リバーシの盤面のデータを初期化する
            else:
                # 次のターンの人を呼び出す
                if board_data['now'] == 1:
                    await ctx.send(f"黒 <@{board_data['black']}> のターンです")
                else:
                    await ctx.send(f"白 <@{board_data['white']}> のターンです")
            self.boards[ctx.channel.id] = board_data
            print("board_now")
            print(board_data['now'])
        else:
            await ctx.send("そこには置けません！")

# Bot本体側からコグを読み込む際に呼び出される関数。


def setup(bot):
    bot.add_cog(Reversi(bot))  # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
