from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from src.app.data_access.orm.market.repositories.price_orm_repository import (
    PriceOrmRepository,
)
from src.app.di.container import Container


@inject
def get_price_repo(
    repository: PriceOrmRepository = Depends(Provide[Container.price_repository]),
) -> PriceOrmRepository:
    return repository
