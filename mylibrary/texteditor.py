
#Discord向けテキストエディタのようなもの
class EditorInstance: # エディタインスタンス。 タブ一つ分
    def __init__(self):
        self.lines = []
        self.cursor_line : int = 0
        self.cursor_column : int = 0
        self.syntax : str = "text" 
        self.file_name: str = "new file"
        self.height : int = 18
        self.width : int = 32
        self.mode = "add"
        self.edited = False

    def add_content(self,s :str): #文字入力
        if self.mode == "add":
            for msg in s.split("\n"):
                self.lines.append(msg)
                self.cursor_line = len(self.lines)
        self.edited = True
    
    def insert_line(self,s :str): #行をラインカーソルのところに挿入。
        self.lines[self.cursor_line] = s
    
    
    def get_view(self): #エディタの全貌を取得
        s = "```" + self.syntax + "\n"
        if self.mode == "add":
            l = ""
            line_begin = self.cursor_line - int(self.height/2) # 描画開始位置
            if line_begin < 0: # もしゼロ以下ならゼロにする。(マイナスから開始するとバグるから。)
                line_begin = 0
            nowline = line_begin
            line_end = line_begin + self.height
            wrap_back = ""
            wrap_back_count = 0
            while nowline + wrap_back_count <= line_end:
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
                    if wrap_back_count < int(self.height/3):#折り返しが過剰じゃ無ければ 
                        l += "     | "+ wrap_back # 折り返し行を追加
                    wrap_back = "" #折り返しを削除する
                    wrap_back_count += 1 #折り返しカウンタを追加
                
                # 折り返し処理
                if len(l) > self.width:
                    wrap_back = l[self.width:]
                    l = l[:self.width]
                l += "\n" #\nを追加して改行
                s+=l
        return s


class CUIEditor: #エディタ本体
    def __init__(self):
        self.using = True
        self.instances = [EditorInstance()]
        self.now_editing_instance = 0
        self.editor_height : int = 18
        self.editor_width : int = 32
    
    def add_content(self, content : str): # エディターインスタンスに新しいコンテンツを追加
        self.instances[self.now_editing_instance].add_content(content)
    
    def get_view(self): #エディタを描画
        editor = self.instances[self.now_editing_instance]
        # サイズ補正
        editor.width = self.editor_width
        editor.height = self.editor_height
        s = editor.get_view()

        #下の線
        s += "＿" * editor.width + "\n"

        #編集したかどうか
        if editor.edited:
            s += "*"
        else:
            s += " "

        #ファイル名
        s += editor.file_name + " | "

        # モード表記
        if editor.mode == "add":
            s += "行追加"
        elif editor.mode == "insert":
            s += "文字列挿入"
        
        # カーソル行, 列を表示
        s += f" L{editor.cursor_line} C{editor.cursor_column}"

        # syntax表示
        s += " 種類: " + editor.syntax

        #枠を閉じる
        s += "\n```"
        return s
