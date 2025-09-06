import uuid
from dataclasses import dataclass, field


@dataclass
class Message:
    message_id: uuid.UUID = field(default_factory=uuid.uuid4, kw_only=True)
    text: str
