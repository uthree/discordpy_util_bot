from mylibrary.filesystem import *
#Discord向けテキストエディタのようなもの
class EditorInstance: # エディタインスタンス。 タブ一つ分
    def __init__(self):
        self.lines = []
        self.cursor_line : int = 0
        self.cursor_column : int = 0
        self.syntax : str = "text" 
        self.file_name: str = "new_file"
        self.directory_path: str = "~/"
        self.height : int = 18
        self.width : int = 32
        self.mode = "add_line"
        self.edited = False

    def add_content(self,content :str): #文字入力
        if self.mode == "add_line":
            for s in content.split("\n"):
                self.lines.append(s)
                self.cursor_line = len(self.lines)
        elif self.mode == "overwrite_line":
            for s in content.split("\n"):
                self.overwrite_line(s)
                self.cursor_line += 1
        elif self.mode == "insert_line":
            for s in content.split("\n"):
                self.insert_line(s)
                self.cursor_line += 1
            self.cursor_line -= 1
        self.edited = True
    
    def insert_line(self,s :str): #行をラインカーソルのところに挿入
        if self.cursor_line > 9999: #行数制限
            self.cursor_line = 9999

        if len(self.lines) > self.cursor_line: # 存在する行であれば
            self.lines.insert(self.cursor_line, s) # 挿入
        else: # 存在しない行なら
            while len(self.lines) <= self.cursor_line: # 十分な行数になるまで繰り返す
                self.lines.append("")
            self.lines.insert(self.cursor_line, s) # 挿入
    
    def overwrite_line(self,s :str): #行をラインカーソルのところに上書き
        if self.cursor_line > 9999: #行数制限
            self.cursor_line = 9999

        if len(self.lines) > self.cursor_line: # 存在する行であれば
            self.lines[self.cursor_line] = s # 上書き処理
        else: # 存在しない行なら
            while len(self.lines) <= self.cursor_line: # 十分な行数になるまで繰り返す
                self.lines.append("")
            self.lines[self.cursor_line] = s # 上書き処理
    
    
    def write_file(self, fs: FileSystem, author): #自信をファイルに保存
        d = fs.get_content(self.directory_path)
        if not fs.check_content(self.directory_path + self.file_name): # ファイルが存在しない場合は新規作成
            d.append(TextFile(self.file_name, d, fs))
        f = fs.get_content(self.directory_path + self.file_name)
        f.write("\n".join(self.lines))
        self.edited = False
    
    def read_file(self, fs: FileSystem, path: str): #自信をファイルから読み込み
        f = fs.get_content(path) #ファイルオブジェクト
        self.lines = f.text.split("\n") # 読み込み

    def get_view(self): #エディタの全貌を取得
        s = ""
        if self.mode == "add_line" or self.mode == "overwrite_line" or self.mode == "insert_line":
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
        self.log = ["編集を開始しました。"]
    
    def add_content(self, content: str): # エディターインスタンスに新しいコンテンツを追加
        self.instances[self.now_editing_instance].add_content(content)
        self.log.append(f"{content} を追加。")
    
    def set_cursor_line(self, line: int): # 行カーソルを代入
        self.instances[self.now_editing_instance].cursor_line = line
        self.log.append(f"{line+1} 行に移動しました")

    def set_mode(self, mode: str):
        self.instances[self.now_editing_instance].mode = mode
        self.log.append(f"{mode} モードに変更しました。")

    def quit_editor(self):
        del self.instances[self.now_editing_instance]
        if len(self.instances) == 0: #エディタが全部終了したら
            self.using = False
    
    def write_file(self, fs: FileSystem,  author):
        self.instances[self.now_editing_instance].write_file(fs, author)
        self.log.append(f"WRITE: {self.instances[self.now_editing_instance].file_name} を保存しました。")
    
    def change_edit_file(self, index: int): #編集するファイルを切り替える。
        if len(self.instances) > index:
            self.now_editing_instance = index
    
    def read_file(self, fs: FileSystem, path: str): #ファイルを読み込んでエディタインスタンスを追加
        if fs.check_content(path):
            f = fs.get_content(path)
            instance = EditorInstance()
            instance.read_file(fs, path)
            instance.file_name = f.name
            instance.directory_path = f.parent.path
            self.instances.append(instance)
            self.log.append(f"READ: {f.path} を読み込みました。")
        else: #読み込めない場合はスルー
            self.log.append(f"READ: {path} が見つかりませんでした。")


    def get_view(self): #エディタを描画
        if len(self.instances) <= self.now_editing_instance: # 編集中のエディタが存在しない場合
            if len(self.instances) == 0 : # 終了されていたら
                return "```\nテキストエディタは終了されました。\n```"
            else: #終了されていなかったら
                self.now_editing_instance = len(self.instances) - 1 # 最後のindexにする。
        editor = self.instances[self.now_editing_instance]
        # サイズ補正
        editor.width = self.editor_width
        editor.height = self.editor_height

        s = "```" + editor.syntax + "\n"
        tabs = ""
        #タブ表記
        for idx, instance in enumerate(self.instances):
            if len(tabs) < editor.width - (3 + len(instance.file_name)): # 十分な空きスペースがあるなら
                if instance == editor:
                    tabs += f"<c{idx} {instance.file_name}>"
                else:
                    tabs += f" c{idx} {instance.file_name} "
        s += tabs + "\n"


        #上の線
        s += "＿" * editor.width + "\n"

        #編集中のエディタ
        s += editor.get_view()

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
        if editor.mode == "add_line":
            s += "行追加"
        elif editor.mode == "insert_line":
            s += "行挿入"
        elif editor.mode == "overwrite_line":
            s += "行上書き"
        
        # カーソル行, 列を表示
        s += f" L{editor.cursor_line} C{editor.cursor_column}"

        # syntax表示
        s += " 種類: " + editor.syntax

        #最後のログ表示
        last_log = self.log[-1]
        if len(last_log) > 20:
            last_log = last_log[0:15] + "..." 
        s += f" | {last_log}"

        #枠を閉じる
        s += "\n```"
        return s

