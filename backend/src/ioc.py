from typing import AsyncGenerator

from dishka import Provider, from_context, Scope, provide, make_async_container
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from src.config import Config, config
from src.core.chat.repositories.chat import SQLAlchemyChatRepository, ChatRepository
from src.core.chat.repositories.message import SQLAlchemyMessageRepository, MessageRepository
from src.core.chat.use_cases.chat import CreateChatUseCase, GetChatByIdUseCase, GetChatListUseCase
from src.core.chat.use_cases.message import CreateMessageUseCase, UpdateMessageUseCase


class SQLAlchemyProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_async_engine(self, _config: Config) -> AsyncEngine:
        return create_async_engine(_config.postgres.db_url, echo=False)

    @provide(scope=Scope.APP)
    def get_async_session_maker(
            self,
            engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
            self,
            session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session


class ChatProvider(Provider):
    scope = Scope.REQUEST

    chat_repository = provide(SQLAlchemyChatRepository, provides=ChatRepository)
    message_repository = provide(SQLAlchemyMessageRepository, provides=MessageRepository)

    create_chat_use_case = provide(CreateChatUseCase)
    get_chat_by_id_use_case = provide(GetChatByIdUseCase)
    get_chat_list_use_case = provide(GetChatListUseCase)

    create_message_use_case = provide(CreateMessageUseCase)
    update_message_use_case = provide(UpdateMessageUseCase)


container = make_async_container(
    SQLAlchemyProvider(),
    ChatProvider(),
    context={Config: config, }
)
