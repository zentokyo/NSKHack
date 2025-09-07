import uuid
from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.chat.entities.message import Message
from src.core.chat.exceptions.message import MessageNotFoundException
from src.core.chat.models.chat import MessageModel


class MessageRepository(ABC):
    @abstractmethod
    async def add_message(self, message: Message) -> None:
        pass

    @abstractmethod
    async def update_message(self, message: Message) -> None:
        pass

    @abstractmethod
    async def get_message_by_id(self, message_id: uuid.UUID) -> Message:
        pass


class SQLAlchemyMessageRepository(MessageRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, message: Message) -> None:
        model = MessageModel.from_entity(message)
        self._session.add(model)
        await self._session.commit()

    async def update_message(self, message: Message) -> None:
        model = MessageModel.from_entity(message)
        await self._session.merge(model)
        await self._session.commit()

    async def get_message_by_id(self, message_id: uuid.UUID) -> Message:
        query = select(MessageModel).where(MessageModel.message_id == message_id)
        model = await self._session.scalar(query)

        if model is None:
            raise MessageNotFoundException(message_id)

        return model.to_entity()