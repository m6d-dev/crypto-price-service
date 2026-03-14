import asyncio

from dependency_injector.wiring import inject

from src.app.application.dto.price_commands import PriceCreateCommand
from src.app.application.services.price_fetcher import PriceFetcher
from src.app.data_access.orm.market.models.price_orm_model import PriceOrmModel
from src.app.di.container import Container
from src.app.tasks.celery_app import app


@app.task
@inject
def save_index_prices():
    fetcher = PriceFetcher()

    async def main():
        container = Container()
        repo = container.price_repository()
        btc = await fetcher.get_price(PriceOrmModel.TickerEnum.BTC)
        await repo.create(
            cmd=PriceCreateCommand(
                ticker=PriceOrmModel.TickerEnum.BTC,
                price=btc["result"]["index_price"],
                timestamp=int(btc["usIn"] / 1_000_000),
            )
        )
        eth = await fetcher.get_price(PriceOrmModel.TickerEnum.ETH)
        await repo.create(
            cmd=PriceCreateCommand(
                ticker=PriceOrmModel.TickerEnum.ETH,
                price=eth["result"]["index_price"],
                timestamp=int(eth["usIn"] / 1_000_000),
            )
        )

    asyncio.run(main())
