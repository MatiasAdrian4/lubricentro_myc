from typing import Annotated

from pydantic import TypeAdapter, Field
from pydantic_ai.messages import Message

MessageTypeAdapter: TypeAdapter[Message] = TypeAdapter(
    Annotated[Message, Field(discriminator="role")]
)
