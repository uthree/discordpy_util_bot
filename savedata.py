import time
import os
import yaml
import copy
import threading


class SaveData:

    def __init__(self, dir_name, delete_count=60, default_data={}):
        self.delete_count = delete_count
        self.default_data = default_data
        self.dir_name = dir_name
        self.delete_counter = {}
        self.buffer = {}
        # ディレクトリのパスになるように補正
        if not self.dir_name[-1] == "/":
            self.dir_name += "/"

        # ディレクトリ作成
        if not os.path.exists(self.dir_name):
            os.makedirs(self.dir_name)

        # 自動セーブスレッド
        thread = threading.Thread(target=self.__loop)
        thread.start()

    def __loop(self):  # 呼び出し回数の少ないものを自動的にバッファから破棄してセーブする
        # print("ループ開始")
        while True:
            time.sleep(1)
            # print(self)
            for k in list(self.buffer.keys()):
                # print(k)
                # print(self.delete_counter)
                if self.delete_counter[k] > 1:
                    self.delete_counter[k] -= 1
                else:
                    # 保存してバッファから破棄
                    self.__save(k, self.buffer[k])
                    self.buffer.pop(k)

    def __load(self, key):  # ファイルから読み込む。
        # print(f"load {key}")
        path = self.dir_name + key + ".yml"
        if os.path.exists(path):
            with open(path) as file:
                obj = yaml.safe_load(file)
            return obj
        else:
            return None

    def __save(self, key, value):  # ファイルに書き込む
        # print(f"save {key} {value}")
        path = self.dir_name + key + ".yml"
        with open(path, "w") as file:
            yaml.dump(value, file)

    def read(self, key):
        if not key in self.buffer:
            load_result = __load(key)
            if load_result == None:
                return copy.copy(self.default_data)
            else:
                return load_result
        self.delete_counter[key] = self.delete_count
        return self.buffer[key]

    def write(self, key, value):
        self.delete_counter[key] = self.delete_count
        self.buffer[key] = value
        return value
