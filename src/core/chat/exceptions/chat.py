import uuid
from dataclasses import dataclass

from src.core.commons.exception import ApplicationException


@dataclass(frozen=True, eq=False)
class ChatException(ApplicationException):
    @property
    def message(self) -> str:
        return "Ошибка при работе с чатами!"


@dataclass(frozen=True, eq=False)
class ChatNotFoundException(ChatException):
    chat_id: uuid.UUID

    @property
    def message(self) -> str:
        return f"Чат с id='{self.chat_id}' не найден!"

@dataclass(frozen=True, eq=False)
class ChatAlreadyExistException(ChatException):
    title: str

    @property
    def message(self) -> str:
        return f"Чат с названием='{self.title}' уже существует!"