import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.app.core.config import DatabaseSettings
from src.app.data_access.orm.base.base_orm_models import SqlAlchemyBaseModel

# Not remove 'noqa' from this line. It need to alembic could find all tables.
from src.app.data_access.orm.models import *  # noqa

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SqlAlchemyBaseModel.metadata

db_config = DatabaseSettings()
config.set_main_option("sqlalchemy.url", db_config.url)


async def _async_session_factory() -> AsyncSession:
    bind = create_async_engine(db_config.url, pool_pre_ping=True)
    return async_sessionmaker(
        bind=bind,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    engine = create_async_engine(
        db_config.url,
        echo=True,
        pool_pre_ping=True,
    )

    async with engine.connect() as connection:
        await connection.run_sync(do_migrations)

    await engine.dispose()


def do_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# --- CRITICAL ENTRY POINT LOGIC ---

if context.is_offline_mode():
    run_migrations_offline()
else:
    # This is the entry point for "online" (connected to DB) mode
    # It runs the async function using asyncio
    asyncio.run(run_migrations_online())
