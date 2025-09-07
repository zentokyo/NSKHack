from datetime import datetime, UTC
import uuid
from dataclasses import dataclass, field

from src.core.chat.entities.message import Message


@dataclass
class Chat:
    chat_id: uuid.UUID = field(default_factory=uuid.uuid4, kw_only=True)
    title: str
    messages: list[Message]
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)
