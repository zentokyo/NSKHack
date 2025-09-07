from dataclasses import dataclass


@dataclass(frozen=True)
class CreateChatDTO:
    title: str
