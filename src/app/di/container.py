from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.app.core.config import settings
from src.app.data_access.orm.market.repositories.price_orm_repository import (
    PriceOrmRepository,
)


class Container(containers.DeclarativeContainer):

    config = providers.Object(settings)

    # database
    engine = providers.Singleton(
        create_async_engine,
        settings.db.url,
        pool_pre_ping=True,
    )

    session_factory = providers.Singleton(
        async_sessionmaker,
        bind=engine,
        expire_on_commit=False,
    )

    # repositories
    price_repository = providers.Singleton(
        PriceOrmRepository, session_factory=providers.Callable(session_factory)
    )
