from datetime import datetime, UTC
import uuid
from dataclasses import dataclass, field


@dataclass
class Message:
    message_id: uuid.UUID = field(default_factory=uuid.uuid4, kw_only=True)
    chat_id: uuid.UUID
    text: str
    sender: str
    rating: int = field(default=3, kw_only=True)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC), kw_only=True)
