import re

from mylibrary.exception import BotCommandException

# ディレクトリ
class Directory:
    def __init__(self, name: str, parent, fs):
        self.contents = []
        self.name = name
        self.owner_id = None # オーナー権限を持つ人
        self.user_ids = [] # ユーザ権限を持つ人たち
        self.permissions = DirectoryPermission() #アクセス権限データオブジェクト
        

        self.parent = parent # 親ディレクトリ
        self._root_directory = fs # ファイルシステム

    
    def create_directory(self, name): #新規ディレクトリを作成
        if len([c for c in self.contents if c.name == name]) > 0: # 同じ名前のディレクトリがあったらエラーを吐く
            raise DirectoryCreationError(f"ディレクトリ :file_folder: {name} はすでに存在します。")
        self.contents.append(Directory(name, self.parent, self._root_directory))
    
    def delete_content(self, content_name): #特定のコンテンツを削除
        self.contents = [c for c in self.contents if c.name != content_name]
    
    def append(self, content):
        self.contents.append(content)
    
    @property
    def root_directory(self):
        return self._root_directory
    
    @property
    def path(self):# 自身のパスを取得
        now = self
        p = "/"
        while not now == self._root_directory: #ルートディレクトリになるまで繰り返す。
            p = ("/" + now.name + p)
            now = now.parent
        return p

# 模擬ファイルシステム。テキストデータのみを保存できる。
class FileSystem(Directory): 
    def __init__(self):
        super().__init__("/", self, self)
        self.current_path = "/"
        self.home_path = "/"
        self._root_directory = self
    
    
    def mkdir(self, dirname: str): # ディレクトリ作成
        self.get_content(self.current_path).create_directory(dirname)
    
    @property
    def current_directory(self): #　カレントディレクトリを取得
        return self.get_content(self.current_path)

    def check_content(self, path): #ファイル/ ディレクトリ存在確認
        try:
            self.get_content(path)
        except ContentNotFound:
            return False
        else:
            return True
    
    def get_content(self, path :str):
        now = self
        finding_directory = False
        finding_parent = False

        if path == "/":
            return self
        
        md = re.match("\.(/\|)(.+)", path) #相対パスの処理(./hogehoge の形) 
        if md:
            path = self.current_path + md[2]
        
        md = re.match("\.\.\/|\.\.", path) # カレントディレクトリの外( ..か../ )
        if md:
            return self.get_content(self.current_directory.path).parent

        md = re.match("\.\./(.*)", path) #相対パス(カレントディレクトリの外)
        if md:
            path = self.get_content(self.current_directory.path).parent.path
        
        if not "/" in path: #相対パスの処理(ファイル名だけ)
            path = self.current_path + path

        md = re.match("~/(.+)",path) #ホームディレクトリ相対パス
        if md:
            path = self.home_path + md[1]
        
        md = re.match("(.+)/",path) #ディレクトリを探している場合
        if md and len(path) > 1:
            path = md[1]
            finding_directory = True
        
        if path[0] == "/": #絶対パスの場合
            path = path[1:]

        for n in path.split("/"):
            now = self
            r = [d for d in now.contents if d.name == n]
            if len(r) <= 0: # 見つからなかった場合
                raise ContentNotFound(f"ファイルまたはディレクトリ \`{path}\` は存在しません。")
            else: #見つけることができた場合
                if finding_directory and type(r[0]) == Directory: #ディレクトリをお求めで、現在のものがディレクトリなら
                    now = r[0]
                elif type(r[0]) == TextFile:
                    now = r[0]
        return now
    

# ファイル
class TextFile:
    def __init__(self, name: str, parent: Directory, fs: FileSystem):
        self.author = "system"
        self.name = name
        self._text : str = ""
        self.parent = parent
        self.root_directory = fs
    
    @property
    def path(self):# 自身のパスを取得
        now = self
        p = "/"
        while not now == self._root_directory: #ルートディレクトリになるまで繰り返す。
            p = ("/" + now.name + p)
            now = now.parent
        return p
    
    @property
    def text(self): #内容
        return self._text

    def write(self, s): #書き込み
        self._text = s
    
    def read(self): # 読み込み
        return self._text


#　ディレクトリのアクセス権限
class DirectoryPermission:
    def __init__(self):
        self.owner = Permission(True, True, True, True)
        self.user = Permission(True, True, True, False)
        self.other = Permission(True, False, False, False)

class Permission:
    def __init__(self, r:bool, w:bool, e:bool, d:bool):
        self.read = r,
        self.write = w,
        self.execute = e,
        self.delete = d,
    

# 各種例外

class DirectoryCreationError(BotCommandException): # ディレクトリを作るときのエラー
    pass

class FileCreationError(BotCommandException): # ファイル作るときのエラー
    pass

class ContentNotFound(BotCommandException): # コンテンツが見つからなかったときのエラー
    pass

class NoPermissionError(BotCommandException): #アクセス権限がなかったときのエラー
    pass