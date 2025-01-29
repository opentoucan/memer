from typing import List

from pydantic import BaseModel

class Link(BaseModel):
    guild_id: str
    channel_id: str
    message_id: str

class RepostEvent(BaseModel):
    channel_id: str
    reply_image: bytes
    links: List[Link]
