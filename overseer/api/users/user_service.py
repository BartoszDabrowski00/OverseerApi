from typing import Optional, Any, List

from overseer.utils.mongo.mongo_client import MongoClient
from overseer.utils.mongo.formatter import format_collection, format_single_element


class UserService:

    def __init__(self):
        self.mongo = MongoClient

    def check_if_user_exists(self, user_id: str) -> bool:
        user = self.mongo.find_user(user_id=user_id)
        if user is None:
            return False

        return True

    def get_user(self, user_id: str) -> Optional[dict[str, Any]]:
        user = self.mongo.find_user(user_id=user_id)
        if user is None:
            return None

        return format_single_element(user)

    def get_all_users(self) -> List[dict[str, Any]]:
        users = self.mongo.find_all_users()

        return format_collection(users)

    def get_user_subordinates(self, user_id: str) -> List[dict[str, Any]]:
        subordinates = list(self.mongo.find_user_subordinates(user_id))[0]['user_subordinates']

        return format_collection(subordinates)

    def add_subordinate(self, user_id: str, subordinate_id: str) -> None:
        self.mongo.add_subordinate(user_id, subordinate_id)

    def delete_subordinate(self, user_id: str, subordinate_id: str) -> None:
        self.mongo.delete_subordinate(user_id, subordinate_id)


