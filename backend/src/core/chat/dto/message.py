import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateMessageDTO:
    chat_id: uuid.UUID
    text: str
    sender: str


@dataclass(frozen=True)
class UpdateMessageDTO:
    message_id: uuid.UUID
    rating: int
