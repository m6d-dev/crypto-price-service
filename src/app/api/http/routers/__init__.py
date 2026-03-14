from fastapi import APIRouter

from src.app.api.http.routers.v1.market.price_api import router as price_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(price_router)
