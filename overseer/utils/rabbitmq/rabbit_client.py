from bson import ObjectId
from pika import BlockingConnection, ConnectionParameters, PlainCredentials

from overseer.utils.config.config import Config


class RabbitClient:
    ENCODING = 'UTF-8'
    config = Config()

    def __init__(self) -> None:
        self.connection = BlockingConnection(ConnectionParameters(
            host=self.config.get("amqp", "host"),
            port=self.config.get("amqp", "port"),
            virtual_host=self.config.get("amqp", "vhost"),
            credentials=PlainCredentials(self.config.get("amqp", "username"), self.config.get("amqp", "password"))
        ))
        self.recordings_exchange = self.config.get("amqp", "recordings_exchange")
        self.recordings_exchange_type = self.config.get("amqp", "recordings_exchange_type")
        self.recordings_route = self.config.get("amqp", "recordings_route")
        self.recordings_new_queue = self.config.get("amqp", "recordings_new_queue")
        self.recordings_new_queue_type = self.config.get("amqp", "recordings_new_queue_type")
        self.channel = self.connection.channel()

        self.declare_amqp()

    def declare_amqp(self) -> None:
        self.channel.exchange_declare(exchange=self.recordings_exchange,
                                      durable=True,
                                      exchange_type=self.recordings_exchange_type)

        self.channel.queue_declare(queue=self.recordings_new_queue, durable=True,
                                   arguments={'x-queue-type': self.recordings_new_queue_type})

        self.channel.queue_bind(self.recordings_new_queue, self.recordings_exchange, routing_key=self.recordings_route)

    def publish_new_recording(self, document_id: ObjectId) -> None:
        self.channel.basic_publish(exchange=self.recordings_exchange,
                                   routing_key=self.recordings_route,
                                   body=str(document_id).encode(self.ENCODING))
