from pydantic import BaseModel

from src.app.data_access.orm.market.models.price_orm_model import PriceOrmModel


class PriceQueryQuery(BaseModel):
    ticker: PriceOrmModel.TickerEnum
    limit: int = 10
    offset: int = 0
    start: int | None = None
    end: int | None = None
    latest: bool | None = False
