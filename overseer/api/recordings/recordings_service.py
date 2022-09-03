from bson import Binary
from werkzeug.datastructures import FileStorage
from datetime import datetime
from overseer.utils.mongo.mongo_client import MongoClient
from overseer.utils.rabbitmq.rabbit_client import RabbitClient


class RecordingsService:
    rabbit_client = RabbitClient()

    def __init__(self):
        self.mongo = MongoClient

    def send_recording_to_model(self, file: FileStorage, user_id: int, timestamp: datetime):
        file_binary = Binary(file.stream.read())
        document_id = self.mongo.insert_user_recording(file_binary, user_id, timestamp)

        self.rabbit_client.publish_new_recording(document_id)
