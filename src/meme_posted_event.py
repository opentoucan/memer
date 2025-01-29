from pydantic import BaseModel

class MemePosted(BaseModel):
    sender: str
    name_colour: str
    avatar: bytes
    meme: bytes
    guild_id: str
    channel_id: str
    message_id: str