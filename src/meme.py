"""Module containing the Meme domain object"""
from pydantic import BaseModel

class Meme(BaseModel):
    """Constructor used by pydantic"""
    sender: str
    timestamp: str
    guild_id: str
    channel_id: str
    message_id: str
