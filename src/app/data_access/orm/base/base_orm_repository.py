from typing import Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC

from src.app.data_access.orm.base.base_orm_models import SqlAlchemyBaseModel
TModel = TypeVar("TModel", bound=SqlAlchemyBaseModel)

class SqlAlchemyRepository(ABC, Generic[TModel]):
    model: Type[TModel]

    def __init__(self, db: AsyncSession):
        self.db = db
