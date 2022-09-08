from typing import Optional
from werkzeug.security import check_password_hash

from overseer.utils.mongo.mongo_client import MongoClient


class AuthenticationService:

    def __init__(self):
        self.mongo = MongoClient

    def check_if_valid_user(self, email: str, password: str) -> Optional[str]:
        user = self.mongo.find_user(email=email)
        if user is None:
            return None

        is_password_valid = check_password_hash(user['password'], password)
        if is_password_valid:
            return str(user['_id'])

        return None
