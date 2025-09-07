import uuid
from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.chat.entities.chat import Chat
from src.core.chat.exceptions.chat import ChatNotFoundException
from src.core.chat.models.chat import ChatModel


class ChatRepository(ABC):
    @abstractmethod
    async def add_chat(self, chat: Chat) -> None:
        pass

    @abstractmethod
    async def get_chat_by_id(self, chat_id: uuid.UUID) -> Chat:
        pass

    @abstractmethod
    async def check_exist_chat_by_title(self, title) -> bool:
        pass

    @abstractmethod
    async def get_chat_list(self) -> list[Chat]:
        pass


class SQLAlchemyChatRepository(ChatRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_chat(self, chat: Chat) -> None:
        model = ChatModel.from_entity(chat)
        self._session.add(model)
        await self._session.commit()

    async def get_chat_by_id(self, chat_id: uuid.UUID) -> Chat:
        query = select(ChatModel).where(ChatModel.chat_id == chat_id).options(selectinload(ChatModel.messages))
        model = await self._session.scalar(query)

        if model is None:
            raise ChatNotFoundException(chat_id)

        return model.to_entity()

    async def check_exist_chat_by_title(self, title) -> bool:
        query = select(ChatModel).where(ChatModel.title == title)
        model = await self._session.scalar(query)

        return bool(model)

    async def get_chat_list(self) -> list[Chat]:
        query = select(ChatModel).order_by(ChatModel.created_at.desc())
        model_list = await self._session.scalars(query)
        return [model.to_entity_without_messages() for model in model_list.all()]
