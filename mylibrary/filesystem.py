import re

# ディレクトリ
class Directory:
    def __init__(self, name: str, parent, fs):
        self.contents = []
        self.name = name
        self.owner_id = None # オーナー権限を持つ人
        self.user_ids = [] # ユーザ権限を持つ人たち
        self.permissions = DirectoryPermission() #アクセス権限データオブジェクト

        self.parent = parent # 親ディレクトリ
        self.firesystem = fs # ファイルシステム

    
    def create_directory(self, name): #新規ディレクトリを作成
        self.contents.append(self.__init__(name, self, self.firesystem))
    
    def delete_content(self, content_name): #特定のコンテンツを削除
        self.contents = [c for c in self.contents if c.name != content_name]
    
    def append(self, content):
        self.contents.append(content)

        

# 模擬ファイルシステム。テキストデータのみを保存できる。
class FileSystem(Directory): 
    def __init__(self):
        super().__init__("/", self, self)
        self.current_path = "/"
        self.home_path = "/"
    
    def get(self, path):
        now = self
        finding_directory = False
        md = re.match("\.(/\|)(.+)",path) #相対パスの処理
        if md:
            path = self.current_path + md[2]

        md = re.match("~/(.+)",path) #ホームディレクトリ相対パス
        if md:
            path = self.home_path + md[1]
        
        md = re.match("(.+)/",path) #ディレクトリを探している場合
        if md:
            path = md[1]
            finding_directory = True

        for n in path.split("/"):
            now = self
            r = [d for d in now.contents if d.name == n]
            if len(r) <= 0: # 見つからなかった場合
                return None
            else: #見つけることができた場合
                if finding_directory and type(r[0]) == Directory: #ディレクトリをお求めで、現在のものがディレクトリなら
                    now = r
                elif type(r[0]) == TextFile:
                    now = r
        return now
    

# ファイル
class TextFile:
    def __init__(self, name: str, parent: Directory):
        self.author = "system"
        self.name = name
        self.content : str = ""
        self.parent = parent

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
    