# コンフィグオブジェクト
import re
from mylibrary.exception import BotCommandException

class ConfigData:
    def __init__(self):
        self.configs = []
    
    def get_view(self):
        r = ""
        for config in self.configs:
            r += f"{config.name} : `{config.value}`\n"
        return r
    
    def get_config(self, name):
        f = [c for c in self.configs if c.name == name]
        if len(f) > 0:
            return f[0]
        else:
            raise ConfigNotFound(f"コンフィグ {name} は存在しません。")

    def set_config(self, name, value):
        self.get_config(name).set_value(value)

class ChannelConfig(ConfigData): # チャンネルようコンフィグデータ
    def __init__(self):
        super().__init__()
        self.configs.append(BoolConfigValue("adblock", False))
        self.configs.append(BoolConfigValue("thread_creator", False))

    
class ConfigValue:
    def __init__(self, name, default_value, description = "説明が設定されていません"):
        self.name = name
        self.value = default_value
        self.description = description

    def set_value(self, value):
        if type(value) == type(self.value):
            self.value = value
        else:
            raise ConfigTypeError("コンフィグの型が一致しません")

class BoolConfigValue(ConfigValue): # bool型コンフィグ
    def __init__(self, name, defautl_value : bool):
        super().__init__(name, defautl_value) # 初期化
    
    def set_value(self, value:str):
        if re.match("yes|on|true|Yes|YES|On|ON|True|TRUE|有効|ゆうこう", value):
            super().set_value(True)
        elif re.match("no|off|false|No|NO|Off|False|FALSE|無効|むこう", value):
            super().set_value(False)
        else:
            raise ConfigTypeError("コンフィグの型が一致しません")




class ConfigNotFound(BotCommandException):
    pass

class ConfigTypeError(BotCommandException):
    pass