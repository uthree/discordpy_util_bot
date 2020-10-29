from dataclasses import dataclass
from mylibrary import filesystem


class UserData:
    def __init__(self):
        self.filesystem = filesystem.FileSystem()
        self.profile = "未設定"