import uuid
from typing import Self

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.chat.entities.chat import Chat
from src.core.chat.entities.message import Message
from src.core.commons.model import BaseModel


class ChatModel(BaseModel):
    __tablename__ = "chat"
    chat_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    title: Mapped[str]

    messages: Mapped[list["MessageModel"]] = relationship()

    @classmethod
    def from_entity(cls, chat: Chat) -> Self:
        return cls(
            chat_id=chat.chat_id,
            title=chat.title,
            created_at=chat.created_at,
        )

    def to_entity(self) -> Chat:
        return Chat(
            chat_id=self.chat_id,
            messages=[message.to_entity() for message in self.messages],
            title=self.title,
            created_at=self.created_at
        )

    def to_entity_without_messages(self) -> Chat:
        return Chat(
            chat_id=self.chat_id,
            title=self.title,
            created_at=self.created_at
        )


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
