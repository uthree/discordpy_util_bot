from dataclasses import dataclass
from mylibrary.config_data import *

class ChannelData:
    def __init__(self):
        self.prefixes = ["u!"]
        self.config = ChannelConfig()
