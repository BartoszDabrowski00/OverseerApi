from typing import Optional, Any

from overseer.utils.mongo.mongo_client import MongoClient


class UserService:

    def __init__(self):
        self.mongo = MongoClient

    def get_user(self, user_id: str) -> Optional[dict[str, Any]]:
        user = self.mongo.find_user(user_id=user_id)
        user['_id'] = str(user['_id'])
        return user

    def get_all_users(self):
        users = self.mongo.find_all_users()
        users_list = []
        for user in users:
            user['_id'] = str(user['_id'])
            users_list.append(user)

        return users_list
