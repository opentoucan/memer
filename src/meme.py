from datetime import datetime

class Meme:
    def __init__(self, sender: str, timestamp: datetime, guild_id: str, channel_id: str, message_id: str):
        self.sender = sender
        self.timestamp = timestamp
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.message_id = message_id