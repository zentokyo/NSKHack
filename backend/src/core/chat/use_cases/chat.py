import uuid

from src.core.chat.dto.chat import CreateChatDTO
from src.core.chat.entities.chat import Chat
from src.core.chat.exceptions.chat import ChatAlreadyExistException
from src.core.chat.repositories.chat import ChatRepository


class CreateChatUseCase:
    def __init__(self, chat_repository: ChatRepository):
        self._chat_repository = chat_repository

    async def __call__(self, create_chat_dto: CreateChatDTO) -> Chat:
        if await self._chat_repository.check_exist_chat_by_title(title=create_chat_dto.title):
            raise ChatAlreadyExistException(title=create_chat_dto.title)

        chat = Chat(title=create_chat_dto.title)

        await self._chat_repository.add_chat(chat)

        return chat


class GetChatListUseCase:
    def __init__(self, chat_repository: ChatRepository):
        self._chat_repository = chat_repository

    async def __call__(self) -> list[Chat]:
        return await self._chat_repository.get_chat_list()


class GetChatByIdUseCase:
    def __init__(self, chat_repository: ChatRepository):
        self._chat_repository = chat_repository

    async def __call__(self, chat_id: uuid.UUID) -> Chat:
        return await self._chat_repository.get_chat_by_id(chat_id=chat_id)
