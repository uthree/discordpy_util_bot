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
        self.append(Directory(name, self, self._root_directory))
    
    def remove_content(self, content): #特定のコンテンツを削除
        self.contents = [c for c in self.contents if c.name != content.name]
    
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

    def cd(self, path): #ディレクトリ移動
        self.current_path = self.get_content(path).path

    @property
    def current_directory(self):
        return self.get_content(self.current_path)

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
    
    def get_content(self, path :str): #パスからコンテンツを取得
        if path[0] == "/": #絶対パス
            return self.get_content_from_absolute_path(path)
        elif path.startswith("./"): #相対パス
            path = self.current_path + path[2:]
            return self.get_content_from_absolute_path(path)
        elif path == ".": # カレントディレクトリ
            return self.get_content_from_absolute_path(self.current_path)
        elif path.startswith("../"): # 一つ外側
            path = path[3:]
            return self.get_content(self.get_content_from_absolute_path(self.current_path).parent.path + path)
        elif path == "..": # 一つ外側のディレクトリ
            return self.get_content(self.get_content_from_absolute_path(self.current_path).parent.path)
        return self.get_content_from_absolute_path(self.current_path + path)



    def get_content_from_absolute_path(self, path: str): # 絶対パスからコンテンツを取得
        if path[0] == "/" and len(path) > 1: # 最初のスラッシュを削除する
            path = path[1:]
        if path[-1] == "/" and len(path) > 1: # 最後のスラッシュを削除する
            path = path[:-1]

        if path == "/":
            return self
        
        now = self
        for name in path.split("/"):
            result = [c for c in now.contents if c.name == name]
            if len(result) > 0:
                now = result[0]
            else:
                raise ContentNotFound(f"{path} は存在しません。")
        return now

    

# ファイル
class TextFile:
    def __init__(self, name: str, parent: Directory, fs: FileSystem):
        self.author = "system"
        self.name = name
        self._text : str = ""
        self.parent = parent
        self._root_directory = fs
    
    @property
    def path(self):# 自身のパスを取得
        now = self
        p = ""
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