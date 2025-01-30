"""Module containing the repost integration event"""

from typing import List
from pydantic import BaseModel


class Link(BaseModel):
    """Constructor used by pydantic"""

    guild_id: str
    channel_id: str
    message_id: str


class RepostEvent(BaseModel):
    """Constructor used by pydantic"""

    channel_id: str
    reply_image: bytes
    links: List[Link]
