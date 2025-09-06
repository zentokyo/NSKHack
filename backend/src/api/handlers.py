from fastapi import APIRouter

from src.api.schemas import AddMessageSchema

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/")
async def add_message(schema: AddMessageSchema):
    return schema.text + "asdasd"
