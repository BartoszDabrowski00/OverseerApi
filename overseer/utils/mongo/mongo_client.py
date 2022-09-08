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
    overseer_users_collection = config.get('mongo', 'overseer_users_collection')

    @classmethod
    @retry(tries=3, delay=1)
    def connect(cls):
        cls.client = Client(cls.connection_string, username=cls.username, password=cls.password)

    @classmethod
    def insert_user_recording(cls, file: Binary, user_id: str, timestamp: datetime) -> ObjectId:
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

    @classmethod
    def insert_new_user(cls, email: str, name: str, surname: str, password: str) -> ObjectId:
        if not cls.client:
            cls.connect()

        db = cls.client.get_database(cls.overseer_db)
        collection = db.get_collection(cls.overseer_users_collection)

        document_id = collection.insert_one({
            'email': email,
            'name': name,
            'surname': surname,
            'password': password,
            'subordinates': []
        }).inserted_id

        return document_id

    @classmethod
    def find_user(cls, email: str = None, user_id: str = None):
        if not cls.client:
            cls.connect()

        if email is None and user_id is None:
            return None

        db = cls.client.get_database(cls.overseer_db)
        collection = db.get_collection(cls.overseer_users_collection)

        if user_id is not None:
            return collection.find_one({
                '_id': ObjectId(user_id)
            })

        return collection.find_one({
            'email': email
        })

    @classmethod
    def find_all_users(cls):
        if not cls.client:
            cls.connect()

        db = cls.client.get_database(cls.overseer_db)
        collection = db.get_collection(cls.overseer_users_collection)
        return collection.find()

    @classmethod
    def add_subordinate(cls, user_id: str, subordinate_id: str):
        if not cls.client:
            cls.connect()

        db = cls.client.get_database(cls.overseer_db)
        collection = db.get_collection(cls.overseer_users_collection)

        collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$push': {'subordinates': ObjectId(subordinate_id)}}
        )

    @classmethod
    def delete_subordinate(cls, user_id: str, subordinate_id: str):
        if not cls.client:
            cls.connect()

        db = cls.client.get_database(cls.overseer_db)
        collection = db.get_collection(cls.overseer_users_collection)

        collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$pull': {'subordinates': ObjectId(subordinate_id)}}
        )

    @classmethod
    def find_user_subordinates(cls, user_id: str):
        if not cls.client:
            cls.connect()

        db = cls.client.get_database(cls.overseer_db)
        collection = db.get_collection(cls.overseer_users_collection)

        return collection.aggregate([
            {'$match': {'_id': ObjectId(user_id)}},
            {'$graphLookup': {
                'from': cls.overseer_users_collection,
                'startWith': '$subordinates',
                'connectFromField': 'subordinates',
                'connectToField': '_id',
                'maxDepth': 0,
                'as': "user_subordinates"
                }
            },
            {'$project': {"user_subordinates": 1, "_id": 0}}
            ])

    @classmethod
    def find_all_recordings(cls):
        if not cls.client:
            cls.connect()

        db = cls.client.get_database(cls.overseer_db)
        collection = db.get_collection(cls.overseer_recordings_collection)

        return collection.find()

    @classmethod
    def find_user_recordings(cls, user_id: str):
        if not cls.client:
            cls.connect()

        db = cls.client.get_database(cls.overseer_db)
        collection = db.get_collection(cls.overseer_recordings_collection)

        return collection.find({
            'user_id': user_id
        })

    @classmethod
    def find_user_recording(cls, user_id: str, recording_id: str):
        if not cls.client:
            cls.connect()

        db = cls.client.get_database(cls.overseer_db)
        collection = db.get_collection(cls.overseer_recordings_collection)

        return collection.find_one({
            '_id': ObjectId(recording_id), 'user_id': user_id
        })

