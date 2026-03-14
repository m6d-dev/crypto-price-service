from enum import StrEnum

from sqlalchemy import BigInteger, Column, Numeric, String

from src.app.data_access.orm.base.base_orm_models import SqlAlchemyBaseModel
from src.app.data_access.orm.consts import DatabaseTable


class PriceOrmModel(SqlAlchemyBaseModel):
    class TickerEnum(StrEnum):
        BTC = "btc_usd"
        ETH = "eth_usd"

    __tablename__ = DatabaseTable.PRICE

    ticker = Column(String, index=True, nullable=False)
    price = Column(Numeric, nullable=False)
    timestamp = Column(BigInteger, nullable=False)
