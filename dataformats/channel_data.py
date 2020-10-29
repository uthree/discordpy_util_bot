from dataclasses import dataclass


@dataclass
class ChannelData:
    channel_command: str = "",
    # configで編集できるデータ
    adblock: bool = False,  # サーバー宣伝自動削除
    thread_creator: bool = False,  # スレッド作成用チャンネルかどうか
