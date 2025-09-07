import uuid
from typing import Self

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.chat.entities.message import Message
from src.core.chat.models.chat import ChatModel
from src.core.commons.model import BaseModel


class MessageModel(BaseModel):
    __tablename__ = "message"
    message_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    chat_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(ChatModel.chat_id, ondelete="CASCADE"))
    text: Mapped[str]
    sender: Mapped[str]
    rating: Mapped[int] = mapped_column(nullable=True)

    @classmethod
    def from_entity(cls, message: Message) -> Self:
        return cls(
            message_id=message.message_id,
            chat_id=message.chat_id,
            text=message.text,
            sender=message.sender,
            rating=message.rating,
            created_at=message.created_at,
        )

    def to_entity(self) -> Message:
        return Message(
            message_id=self.message_id,
            chat_id=self.chat_id,
            text=self.text,
            sender=self.sender,
            rating=self.rating,
            created_at=self.created_at,
        )
