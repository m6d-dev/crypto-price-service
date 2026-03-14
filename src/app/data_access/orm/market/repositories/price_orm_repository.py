from sqlalchemy import Result, desc, func, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.app.application.dto.price_commands import PriceCommand, PriceCreateCommand
from src.app.application.dto.price_dtos import PriceListDTO
from src.app.core.types.cqrs import ListQueryResponse
from src.app.data_access.orm.base.base_orm_repository import SqlAlchemyRepository
from src.app.data_access.orm.market.models.price_orm_model import PriceOrmModel


class PriceOrmRepository(SqlAlchemyRepository[PriceOrmModel]):
    model = PriceOrmModel

    def __init__(self, session_factory: async_sessionmaker):
        super().__init__(session_factory)

    async def get_all(self, cmd: PriceCommand) -> ListQueryResponse[PriceListDTO]:
        async with self.session_factory() as session:
            stmt = select(self.model).filter(self.model.ticker == cmd.ticker)

            if cmd.start:
                stmt = stmt.filter(self.model.timestamp >= cmd.start)
            if cmd.end:
                stmt = stmt.filter(self.model.timestamp <= cmd.end)

            if cmd.latest:
                stmt = stmt.order_by(desc(self.model.timestamp)).limit(1)
            else:
                stmt = (
                    stmt.limit(cmd.limit)
                    .offset(cmd.offset)
                    .order_by(self.model.timestamp)
                )

            result: Result[PriceOrmModel] = await session.execute(stmt)
            res: list[PriceOrmModel] = result.scalars().all()

            count_stmt = select(func.count(self.model.id)).filter(
                self.model.ticker == cmd.ticker
            )
            if cmd.start:
                count_stmt = count_stmt.filter(self.model.timestamp >= cmd.start)
            if cmd.end:
                count_stmt = count_stmt.filter(self.model.timestamp <= cmd.end)

            count_result: Result[int] = await session.execute(count_stmt)

            return ListQueryResponse(
                count=count_result.scalar_one() if not cmd.latest else len(res),
                rows=[
                    PriceListDTO(
                        id=r.id, ticker=r.ticker, price=r.price, timestamp=r.timestamp
                    )
                    for r in res
                ],
            )

    async def create(self, cmd: PriceCreateCommand) -> None:
        model = self.model(ticker=cmd.ticker, price=cmd.price, timestamp=cmd.timestamp)

        async with self.session_factory() as session:
            session.add(model)
            await session.commit()
