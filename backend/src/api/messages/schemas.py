import uuid
from typing import Self

from pydantic import BaseModel

from src.core.chat.entities.message import Message


class AddMessageSchema(BaseModel):
    text: str


class MessageResponse(BaseModel):
    message_id: uuid.UUID
    chat_id: uuid.UUID
    text: str
    sender: str
    rating: int

    @classmethod
    def from_entity(cls, message: Message) -> Self:
        return cls(
            message_id=message.message_id,
            chat_id=message.chat_id,
            text=message.text,
            sender=message.sender,
            rating=message.rating,
        )
