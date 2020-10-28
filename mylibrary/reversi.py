class Board:
    def __init__(self):
        # None: 石なし
        # 1: 黒
        # 2: 白
        self.board_data = []
        for i in range(0, 8):
            self.board_data.append([None] * 8)
        # 最初の４つの石の分を初期化する
        self.board_data[3][4] = 1
        self.board_data[4][3] = 1
        self.board_data[3][3] = 2
        self.board_data[4][4] = 2

    def get_board(self, color=None):  # ボード表示
        r = ""
        for y in self.board_data:
            for x in y:
                if x == None:
                    r += "."
                elif x == 1:
                    r += "b"
                elif x == 2:
                    r += "w"
            r += "\n"
        return r

    def get_board_discord_emojis(self, color=None):
        white = ":white_circle: "
        black = ":black_circle: "
        no_stone = ":green_square: "
        canput_no_stone = ":yellow_square: "
        r = ".\n:negative_squared_cross_mark: :regional_indicator_a: :regional_indicator_b: :regional_indicator_c: :regional_indicator_d: :regional_indicator_e: :regional_indicator_f: :regional_indicator_g: :regional_indicator_h:\n"
        nums = [":one:", ":two:", ":three:", ":four:",
                ":five:", ":six:", ":seven:", ":eight:"]
        for y, arr in enumerate(self.board_data):
            r += nums[y] + " "
            for x, stone in enumerate(arr):
                if stone == None:
                    if not color == None:
                        if self.check_can_put(color, x, y):
                            r += canput_no_stone
                        else:
                            r += no_stone
                    else:
                        r += no_stone
                elif stone == 1:
                    r += black
                elif stone == 2:
                    r += white
            r += "\n"
        return r

    # 設置可能であるかを取得 取得できた場合は方向[[x, y], [x, y], [x, y]...]が帰ってくる
    def check_can_put(self, color, x, y):
        print("CAN_PUT_ARGS")
        print(color, x, y)
        if self.get_color(x, y) != None:
            return False
        directions = [[1, 0], [1, 1], [0, 1], [1, -1],
                      [0, -1], [-1, 0], [-1, 1], [-1, -1]]  # チェックする８方向
        # 自分と違う色のマスがある方向を検索する
        another_color_find = [d for d in directions if self.get_color(
            x + d[0], y + d[1]) != None and self.get_color(x + d[0], y + d[1]) != color]
        if len(another_color_find) < 1:
            return False  # どこに自分と違う色のますがなければこの時点でfalse
        print(another_color_find)
        # 設置可能な方向を取得する
        can_put_direction = []
        for d in another_color_find:
            for i in range(1, 8):  # 調べるべき方向に7回分試行する
                c = self.get_color(x + d[0] * i, y + d[1] * i)
                if c == None:
                    break
                if c == color:
                    print(can_put_direction)
                    print(c, color)
                    can_put_direction.append(d)
                    break
                else:
                    continue
        if len(can_put_direction) < 1:
            return False
        else:
            return can_put_direction

    def check_can_put_any(self, color):  # 指定の色が、どれかのマスに配置できるか
        for y in range(0, 8):
            for x in range(0, 8):
                if self.check_can_put(color, x, y):
                    return True
                else:
                    pass
        return False

    def get_color(self, x, y):
        if x > 7 or x < 0:
            return None
        if y > 7 or y < 0:
            return None
        return self.board_data[y][x]

    def set_color(self, color, x, y):
        self.board_data[y][x] = color

    def put(self, color, x, y):
        directions = self.check_can_put(color, x, y)
        if not directions:
            return False  # 設置失敗　Falseを返す。
        self.set_color(color, x, y)
        for d in directions:
            col = None
            count = 1
            while col != color:
                col = self.get_color(x + d[0] * count, y + d[1] * count)
                self.set_color(color, x + d[0] * count, y + d[1] * count)
                print("SET COLOR")
                print(count)
                print(col, color)  # TODO: ループを抜ける処理を追加する
                count += 1
                if col == color:
                    return None

        return True

    def winner(self):  # 勝利者の色を出力する 黒: 1 白: 2 引き分け: 3 勝利者なし: None
        if self.check_can_put_any(1) or self.check_can_put_any(2):
            return None
        else:  # 誰もおけない
            if self.count(1) > self.count(2):
                return 1  # black
            if self.count(2) > self.count(1):
                return 2  # white
            return 3  # draw

    def count(self, color):  # 特定の色の石の数を数える
        cnt = 0
        for y in self.board_data:
            for x in y:
                if x == color:
                    cnt += 1
        return cnt
