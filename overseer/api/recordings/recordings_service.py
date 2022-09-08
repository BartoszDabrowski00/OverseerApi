from typing import List, Any, Optional

from bson import Binary
from werkzeug.datastructures import FileStorage
from datetime import datetime
from overseer.utils.mongo.mongo_client import MongoClient
from overseer.utils.rabbitmq.rabbit_client import RabbitClient
from overseer.utils.mongo.formatter import format_collection, format_single_element


class RecordingsService:
    rabbit_client = RabbitClient()

    def __init__(self):
        self.mongo = MongoClient

    def send_recording_to_model(self, file: FileStorage, user_id: str, timestamp: datetime):
        file_binary = Binary(file.stream.read())
        document_id = self.mongo.insert_user_recording(file_binary, user_id, timestamp)

        self.rabbit_client.publish_new_recording(document_id)

    def get_all_recordings(self) -> List[dict[str, Any]]:
        recordings = self.mongo.find_all_recordings()

        return format_collection(recordings)

    def get_user_recording(self, user_id: str, recording_id: str) -> Optional[dict[str, Any]]:
        recording = self.mongo.find_user_recording(user_id, recording_id)
        if recording is None:
            return None

        return format_single_element(recording)

    def get_user_recordings(self, user_id: str) -> List[dict]:
        recordings = self.mongo.find_user_recordings(user_id)

        return format_collection(recordings)
