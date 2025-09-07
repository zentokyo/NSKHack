import uuid
from dataclasses import dataclass

from src.core.commons.exception import ApplicationException


@dataclass(frozen=True, eq=False)
class MessageException(ApplicationException):
    @property
    def message(self) -> str:
        return "Ошибка при работе с сообщениями"


@dataclass(frozen=True, eq=False)
class MessageNotFoundException(MessageException):
    message_id: uuid.UUID

    @property
    async def message(self) -> str:
        return f"Сообщение с id='{self.message_id}' не найдено!"
