from abc import ABC
from typing import TypeVar

from sqlalchemy.ext.asyncio import async_sessionmaker

from src.app.data_access.orm.base.base_orm_models import SqlAlchemyBaseModel

TModel = TypeVar("TModel", bound=SqlAlchemyBaseModel)


class SqlAlchemyRepository[TModel](ABC):
    model: type[TModel]

    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory
