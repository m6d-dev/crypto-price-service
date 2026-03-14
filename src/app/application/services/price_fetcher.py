from typing import Any

from httpx import AsyncClient


class PriceFetcher:
    def __init__(self) -> None:
        self._base_url = "https://www.deribit.com/api/v2/public/get_index_price"
        self._parametr = "index_name"

    async def get_price(self, symbol: str) -> dict[str, Any]:
        async with AsyncClient(follow_redirects=True) as client:
            response = await client.get(
                url=f"{self._base_url}?{self._parametr}={symbol}"
            )
            data = response.json()
            return data
