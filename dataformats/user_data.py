from dataclasses import dataclass
from mylibrary.filesystem import *

class UserData:
    def __init__(self):
        self.filesystem = FileSystem()
        