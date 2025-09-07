import uuid
from typing import Self

from pydantic import BaseModel

from src.api.messages.schemas import MessageResponse
from src.core.chat.entities.chat import Chat


class CreateChatSchema(BaseModel):
    title: str


class ChatShortResponse(BaseModel):
    chat_id: uuid.UUID
    title: str


class ChatResponse(ChatShortResponse):
    messages: list[MessageResponse]

    @classmethod
    def from_entity(cls, chat: Chat) -> Self:
        return cls(
            chat_id=chat.chat_id,
            title=chat.title,
            messages=[MessageResponse.from_entity(message) for message in chat.messages]
        )
