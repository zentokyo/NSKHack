from src.core.chat.dto.message import CreateMessageDTO, UpdateMessageDTO
from src.core.chat.entities.message import Message
from src.core.chat.repositories.chat import ChatRepository
from src.core.chat.repositories.message import MessageRepository


class CreateMessageUseCase:
    def __init__(
            self,
            message_repository: MessageRepository,
            chat_repository: ChatRepository,
    ):
        self._message_repository = message_repository
        self._chat_repository = chat_repository

    async def __call__(self, create_message_dto: CreateMessageDTO) -> Message:
        message = Message(
            chat_id=create_message_dto.chat_id,
            text=create_message_dto.text,
            sender=create_message_dto.sender,
        )

        chat = await self._chat_repository.get_chat_by_id(chat_id=create_message_dto.chat_id)
        if not chat.messages:
            chat.title = create_message_dto.text
            await self._chat_repository.update_chat(chat)

        await self._message_repository.add_message(message)

        return message


class UpdateMessageUseCase:
    def __init__(self, message_repository: MessageRepository):
        self._message_repository = message_repository

    async def __call__(self, update_message_dto: UpdateMessageDTO):
        message = await self._message_repository.get_message_by_id(message_id=update_message_dto.message_id)

        message.rating = update_message_dto.rating

        await self._message_repository.update_message(message)

        return message
