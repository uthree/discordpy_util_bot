from dataclasses import dataclass


@dataclass
class ChannelData:
    channel_command: str = "",
    adblock: bool = False,
