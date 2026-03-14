from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ListQueryResponse[T](BaseModel):
    count: int
    rows: list[T]
