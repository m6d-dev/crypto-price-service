from celery import Celery

from src.app.core.config import settings

app = Celery(
    "deribit_tasks",
    broker=settings.redis.broker_url,
    backend=settings.redis.backend_url,
    include=["src.app.tasks.fetch_index_prices"],
)

app.conf.beat_schedule = {
    "fetch-btc-eth-price-every-minute": {
        "task": "src.app.tasks.fetch_index_prices.save_index_prices",
        "schedule": 5.0,
    },
}
app.conf.timezone = "UTC"


@app.on_after_configure.connect
def setup_imports(sender, **kwargs):
    pass
