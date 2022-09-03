from datetime import datetime
from typing import Optional

from bson import Binary, ObjectId
from pymongo import MongoClient as Client
from retry import retry

from overseer.utils.config.config import Config


class MongoClient:
    config = Config()
    client: Optional[Client] = None
    connection_string = config.get('mongo', 'connection_string')
    username = config.get('mongo', 'username')
    password = config.get('mongo', 'password')
    overseer_db = config.get('mongo', 'overseer_db')
    overseer_recordings_collection = config.get('mongo', 'overseer_recordings_collection')

    @classmethod
    @retry(tries=3, delay=1)
    def connect(cls):
        cls.client = Client(cls.connection_string, username=cls.username, password=cls.password)

    @classmethod
    def insert_user_recording(cls, file: Binary, user_id: int, timestamp: datetime) -> ObjectId:
        if not cls.client:
            cls.connect()

        db = cls.client.get_database(cls.overseer_db)
        collection = db.get_collection(cls.overseer_recordings_collection)

        document_id = collection.insert_one({
            'user_id': user_id,
            'recording': file,
            'timestamp': timestamp,
            'features': {}
        }).inserted_id

        return document_id
