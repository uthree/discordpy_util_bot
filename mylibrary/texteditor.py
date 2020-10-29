
#Discord向けテキストエディタのようなもの
class CUIEditor:
    def __init__(self):
        self.lines = []
        self.cursor_line : int = 0
        self.cursor_column : int = 0
        self.syntax : str = "" 
        self.editor_height : int = 10
        self.editor_width : int = 32
        self.mode = "add"
        self.using = True

    def add_content(self,s :str): #文字入力
        if self.mode == "add":
            for msg in "\n".split(s):
                self.lines.append(msg)
                self.cursor_line += 1
    
    def insert_line(self,s :str): #行をラインカーソルのところに挿入。
        self.lines[self.cursor_line] = s
    
    
    def get_view(self): #エディタの全貌を取得
        s = "```\n" + self.syntax
        if self.mode == "add":
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
                    line_view = "{0:04d}".format(nowline+1)
                    if self.cursor_line == nowline: # カーソルと重なる行なら少し特殊な表現にする
                        l += f"{line_view} >>"
                    else:
                        l += f"{line_view} | "
                    if len(self.lines) > nowline:
                        l += self.lines[nowline]
                    nowline += 1
                else: #折り返し状態だったら
                    l += wrap_back # 折り返し行を追加
                    wrap_back = "" #折り返しを削除する
                
                # 折り返し処理
                if len(l) > self.editor_width:
                    wrap_back = l[self.editor_width:]
                    l = l[:self.editor_width]
                l += "\n" #\nを追加して改行
                s+=l
        #モード表記追加
        s += "＿" * self.editor_width + "\n"
        if self.mode == "add":
            s += "行追加"
        elif self.mode == "insert":
            s += "文字列挿入"
        
        # カーソル行, 列を表示
        s += f" L{self.cursor_line} C{self.cursor_column}"
        s += "\n```"
        return s