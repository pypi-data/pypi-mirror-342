from faststream.rabbit import RabbitBroker
from pydantic import AmqpDsn
from faststream.rabbit import RabbitExchange, RabbitQueue, RabbitBroker

from .schemas import DataSchema, DataRow


class RabbitmqPersistence:
    def __init__(
            self, 
            rabbitmq_dsn: AmqpDsn,
            exch: RabbitExchange | None = None,
            queue_save_row: RabbitQueue | None = None,
            queue_create_data_schema: RabbitQueue | None = None,
        ):
        self.exch = exch or RabbitExchange("scraping", auto_delete=True)
        self.queue_save_row = queue_save_row or RabbitQueue("save_row", auto_delete=True)
        self.queue_create_data_schema = queue_create_data_schema or RabbitQueue("create_data_schema", auto_delete=True)
        self.broker = RabbitBroker(
            str(rabbitmq_dsn)
        )

    async def create_data_schema(self, data_schema: DataSchema):
        async with self.broker:
            await self.broker.publish(
                data_schema,
                self.queue_create_data_schema,
                self.exch,
            )

    async def save(self, rows: list[DataRow]) -> None:
        async with self.broker:
            for row in rows:
                await self.broker.publish(
                    row,
                    self.queue_save_row,
                    self.exch,
                )
