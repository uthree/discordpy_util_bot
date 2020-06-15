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
                    r += "o"
                elif x == 1:
                    r += "b"
                elif x == 2:
                    r += "w"
            r += "\n"
        return r

    # 設置可能であるかを取得 取得できた場合は方向[[x, y], [x, y], [x, y]...]が帰ってくる
    def check_can_put(self, color, x, y):
        if self.get_color(x, y) != None:
            return False
        directions = [[1, 0], [1, 1], [0, 1], [1, -1],
                      [0, -1], [-1, 0], [-1, 1], [-1, -1]]  # チェックする８方向
        # 自分と違う色のマスがある方向を検索する
        another_color_find = [d for d in directions if self.get_color(
            x + d[0], y + d[1]) != None and self.get_color(x + d[0], y + d[0]) != color]
        if len(another_color_find) < 1:
            return False  # どこに自分と違う色のますがなければこの時点でfalse
        # 設置可能な方向を取得する
        can_put_direction = []
        for d in another_color_find:
            for i in range(1, 7):  # 調べるべき方向に7回分試行する
                c = self.get_color(x + d[0] * i, y + d[1] * i)
                if c == None:
                    break
                else:
                    if c != color:
                        can_put_direction.append(d)
                        break
        if len(can_put_direction) < 1:
            return False
        else:
            return can_put_direction

    def check_can_put_any(color):  # 指定の色が、どれかのマスに配置できるか
        for y in range(0, 7):
            for x in range(0, 7):
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
            while not col == color:
                col = self.get_color(x + d[0] * count, y + d[1] * count)
                self.set_color(color, x + d[0] * count, y + d[1] * count)
                count += 1
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


# テスト用コード
b = Board()
print(b.check_can_put(2, 2, 4))
print(b.get_board())
