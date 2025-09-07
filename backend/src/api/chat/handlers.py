import uuid

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.api.chat.schemas import CreateChatSchema, ChatShortResponse, ChatResponse
from src.core.chat.dto.chat import CreateChatDTO
from src.core.chat.use_cases.chat import CreateChatUseCase, GetChatListUseCase, GetChatByIdUseCase

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.post("/")
@inject
async def create_chat_handler(
        schema: CreateChatSchema,
        use_case: FromDishka[CreateChatUseCase],
) -> ChatShortResponse:
    dto = CreateChatDTO(
        title=schema.title,
    )

    chat = await use_case.__call__(dto)

    return ChatShortResponse.model_validate(chat, from_attributes=True)


@router.get("/")
@inject
async def get_chat_list_handler(use_case: FromDishka[GetChatListUseCase]) -> list[ChatShortResponse]:
    chat_list = await use_case()

    return [ChatShortResponse.model_validate(chat, from_attributes=True) for chat in chat_list]


@router.get("{chat_id}/")
@inject
async def get_chat_by_id(
        chat_id: uuid.UUID,
        use_case: FromDishka[GetChatByIdUseCase],
) -> ChatResponse:
    chat = await use_case.__call__(chat_id=chat_id)

    return ChatResponse.from_entity(chat)
