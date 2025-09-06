from pydantic import BaseModel


class AddMessageSchema(BaseModel):
    text: str
