
#Discord向けテキストエディタのようなもの
class CUIEditor:
    def __init__(self):
        self.lines = [""]
        self.cursor_line : int = 0
        self.cursor_column : int = 0
        self.syntax : str = "" 
        self.editor_height : int = 10
        self.editor_width : int = 10
        self.mode = "add"

    def add_line(self,s :str): #行を末尾にに追加
        self.lines.append(s)
    
    def insert_line(self,s :str): #行をラインカーソルのところに挿入。
        self.lines[self.cursor_line] = s
    
    
    def get_view(self): #エディタの全貌を取得
        s = "```\n" + self.syntax
        if self.mode == "add" or self.mode == "insert":
            l = ""
            line_begin = self.cursor_line - self.editor_height/2 # 描画開始位置
            if line_begin < 0: # もしゼロ以下ならゼロにする。(マイナスから開始するとバグるから。)
                line_begin = 0
            nowline = line_begin
            line_end = line_begin + self.editor_height
            wrap_back = ""
            while nowline <= line_end:
                l=""
                if len(wrap_back) <= 0: # もし折り返し状態じゃないなら
                    line_view = "{0:04d}".format(nowline)
                    if self.cursor_line == nowline: # カーソルと重なる行なら少し特殊な表現にする
                        l += f"{line_view} >>"
                    else:
                        l += f"{line_view} | "
                    if len(self.lines) > nowline:
                        l += self.lines[nowline]
                else: #折り返し状態だったら
                    l += wrap_back # 折り返し行を追加
                
                # 折り返し処理
                if len(l) > self.editor_width:
                    wrap_back = l[self.editor_width:]
                    print(wrap_back)
                l += "\n" #\nを追加して改行
                s+=l
                nowline += 1
                # todo: 文字列の長さが2000を超えないように調整する
        s += "\n```"
        #print(s)
        return s