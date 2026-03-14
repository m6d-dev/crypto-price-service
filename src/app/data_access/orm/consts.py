from enum import StrEnum
from uuid import UUID, uuid4

type ID_T = UUID


def generate_id() -> ID_T:
    return uuid4()


class DatabaseTable(StrEnum):
    # Market
    PRICE = "market_price"
