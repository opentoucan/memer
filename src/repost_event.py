"""Module containing the repost integration event"""

from typing import List
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel


class Link(BaseModel):
    """Constructor used by pydantic"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
    guild_id: str
    channel_id: str
    message_id: str
    score: float


class RepostEvent(BaseModel):
    """Constructor used by pydantic"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
    guild_id: str
    channel_id: str
    reply_image: bytes
    links: List[Link]
