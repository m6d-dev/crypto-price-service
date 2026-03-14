from pydantic import BaseModel

from src.app.data_access.orm.consts import ID_T


class PriceListDTO(BaseModel):
    id: ID_T
    ticker: str
    price: float
    timestamp: int
