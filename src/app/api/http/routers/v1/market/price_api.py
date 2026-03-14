from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends

from src.app.api.deps.api_deps import get_price_repo
from src.app.application.dto.price_commands import PriceCommand
from src.app.application.dto.price_dtos import PriceListDTO
from src.app.application.dto.price_queries import PriceQueryQuery
from src.app.core.types.cqrs import ListQueryResponse
from src.app.data_access.orm.market.repositories.price_orm_repository import (
    PriceOrmRepository,
)

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/", response_model=ListQueryResponse[PriceListDTO])
@inject
async def get_prices(
    query: PriceQueryQuery = Depends(),
    repo: PriceOrmRepository = Depends(get_price_repo),
):
    """
    Получение цен по фильтрам:
    - `ticker` обязателен
    - `limit` / `offset` для постраничной выборки
    - `start` / `end` — фильтр по времени
    - `latest = True` — только последняя запись
    """
    cmd = PriceCommand(
        ticker=query.ticker,
        limit=query.limit,
        offset=query.offset,
        start=query.start,
        end=query.end,
        latest=query.latest,
    )
    return await repo.get_all(cmd=cmd)
