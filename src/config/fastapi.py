from fastapi import FastAPI

from src.app.api.http.routers import api_v1_router
from src.app.di.container import Container

container = Container()

container.wire(
    packages=[
        "src.app.api.http.routers.v1",
        "src.app.api.http.routers.v1.market.price_api",
        "src.app.tasks.fetch_index_prices",
    ]
)


def fastapi_app_factory() -> FastAPI:
    app = FastAPI(title="Crypto Price Service")
    app.include_router(api_v1_router)

    @app.get("/healthcheck/")
    async def healthcheck():
        return {"status": "ok"}

    return app
