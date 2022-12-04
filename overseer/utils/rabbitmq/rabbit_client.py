import logging
import os

from bson import ObjectId
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from retry import retry

from overseer.utils.config.config import Config

log = logging.getLogger(__name__)


class RabbitClient:
    ENCODING = 'UTF-8'
    config = Config()

    def __init__(self) -> None:
        self.connection = None
        self.channel = None
        self.recordings_exchange = self.config.get("amqp", "recordings_exchange")
        self.recordings_exchange_type = self.config.get("amqp", "recordings_exchange_type")
        self.recordings_route = self.config.get("amqp", "recordings_route")
        self.recordings_new_queue = self.config.get("amqp", "recordings_new_queue")
        self.recordings_new_queue_type = self.config.get("amqp", "recordings_new_queue_type")

        self.connect_to_rmq()
        self.declare_amqp()

    @retry(tries=5, delay=2)
    def connect_to_rmq(self):
        host = os.getenv("RABBIT_HOST", self.config.get("amqp", "host"))
        log.info(f'Connecting to rabbit on host {host}')

        self.connection = BlockingConnection(ConnectionParameters(
            host=host,
            port=self.config.get("amqp", "port"),
            virtual_host=self.config.get("amqp", "vhost"),
            credentials=PlainCredentials(self.config.get("amqp", "username"), self.config.get("amqp", "password"))
        ))
        self.channel = self.connection.channel()

    def declare_amqp(self) -> None:
        log.info(f'Declare exchange {self.recordings_exchange}')
        self.channel.exchange_declare(exchange=self.recordings_exchange,
                                      durable=True,
                                      exchange_type=self.recordings_exchange_type)

        log.info(f'Declaring queue {self.recordings_new_queue}')
        self.channel.queue_declare(queue=self.recordings_new_queue, durable=True,
                                   arguments={'x-queue-type': self.recordings_new_queue_type})

        self.channel.queue_bind(self.recordings_new_queue, self.recordings_exchange, routing_key=self.recordings_route)

    def publish_new_recording(self, document_id: ObjectId) -> None:
        log.info(f'Publishing new recording message to'
                 f' exchange {self.recordings_exchange} route {self.recordings_route} queue {self.recordings_new_queue}')
        if self.channel.is_closed:
            log.info(f'RMQ Connection closed, reconnecting')
            self.connect_to_rmq()

        self.channel.basic_publish(exchange=self.recordings_exchange,
                                   routing_key=self.recordings_route,
                                   body=str(document_id).encode(self.ENCODING))
