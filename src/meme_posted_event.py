"""Module containing the meme posted integration event"""
from pydantic import BaseModel

class MemePosted(BaseModel):
    """Constructor used by pydantic"""
    sender: str
    name_colour: str
    avatar: bytes
    meme: bytes
    guild_id: str
    channel_id: str
    message_id: str
