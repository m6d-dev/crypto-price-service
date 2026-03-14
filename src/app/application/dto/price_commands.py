from pydantic import BaseModel


class PriceCommand(BaseModel):
    limit: int
    offset: int
    ticker: str
    latest: bool | None = None
    start: int | None = None
    end: int | None = None


class PriceCreateCommand(BaseModel):
    ticker: str
    price: float
    timestamp: int
