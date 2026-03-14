from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from src.app.data_access.orm.consts import ID_T, generate_id


class SqlAlchemyBaseModel(DeclarativeBase):
    @declared_attr
    def id(cls) -> Mapped[ID_T]:
        return mapped_column(primary_key=True, default=generate_id)
