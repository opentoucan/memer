"""Module containing the meme posted integration event"""

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel


class MemePosted(BaseModel):
    """Constructor used by pydantic"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
    sender: str
    name_colour: str
    avatar: str
    meme: str
    guild_id: str
    channel_id: str
    message_id: str
