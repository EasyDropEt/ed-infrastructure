import time
from typing import Generic, TypeVar

import jsons
from ed_domain.common.logging import get_logger
from ed_domain.queues.common.abc_producer import ABCProducer
from pika.adapters import BlockingConnection
from pika.connection import ConnectionParameters, URLParameters

LOG = get_logger()
TMessageSchema = TypeVar("TMessageSchema")


class RabbitMQProducer(Generic[TMessageSchema], ABCProducer[TMessageSchema]):
    def __init__(self, url: str, queue: str) -> None:
        self._queue = queue
        self._connection = self._connect_with_url_parameters(url)

    def start(self) -> None:
        LOG.info("Starting producer...")
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue, durable=True)

    def stop(self) -> None:
        LOG.info("Stopping producer...")
        if self._connection.is_open:
            self._connection.close()

    def publish(self, message: TMessageSchema) -> None:
        assert "_channel" in self.__dict__, "Producer has not been started"
        try:
            self._channel.basic_publish(
                exchange="", routing_key=self._queue, body=jsons.dumps(message)
            )
            LOG.info(f" [x] Sent '{message}'")
        except Exception as e:
            LOG.error(f"Failed to publish message: {e}")

    def _connect_with_connection_parameters(
        self, host: str, port: int
    ) -> BlockingConnection:
        connection_parameters = ConnectionParameters(host, port)
        return BlockingConnection(connection_parameters)

    def _connect_with_url_parameters(self, url: str) -> BlockingConnection:
        connection_parameters = URLParameters(url)
        retry_attempts = 5
        for attempt in range(retry_attempts):
            try:
                return BlockingConnection(connection_parameters)
            except Exception as e:
                LOG.error(f"Connection attempt {attempt + 1} failed: {e}")
                time.sleep(2**attempt)  # Exponential backoff

        raise ConnectionError(
            "Failed to connect to RabbitMQ after several attempts")
