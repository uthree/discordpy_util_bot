from dataclasses import dataclass


@dataclass
class ChannelData:
    channel_command: str = "",

    thread_creater: bool = False,  # スレッド作成用チャンネルかどうか
    thread: bool = False,  # これ自身がスレッドであるかどうか。
    # config系
    adblock: bool = False,
