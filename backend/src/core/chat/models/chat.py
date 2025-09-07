import uuid
from typing import Self

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.chat.entities.chat import Chat
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
