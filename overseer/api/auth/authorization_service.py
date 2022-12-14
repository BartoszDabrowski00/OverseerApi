import jwt
from datetime import datetime, timedelta
from typing import Optional, Any

from overseer.api.auth.roles import Role
from overseer.utils.config.config import Config
from overseer.utils.mongo.mongo_client import MongoClient


class AuthorizationService:

    def __init__(self):
        self.mongo = MongoClient
        self.secret_key = Config().get('server', 'secret_key')

    def generate_user_token(self, user_id: str) -> str:
        return jwt.encode({'id': user_id, 'exp': datetime.utcnow() + timedelta(minutes=30)}, self.secret_key,
                          algorithm="HS256")

    def check_if_valid_token(self, headers: dict[str, Any]) -> Optional[str]:
        if 'x-access-token' not in headers:
            return None

        token = headers['x-access-token']

        try:
            data = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            current_user = self.mongo.find_user(user_id=data['id'])
            if current_user is None:
                return None

            return data['id']
        except Exception:
            return None

    def change_role(self, user_id: str, new_role: Role):
        self.mongo.change_user_role(user_id, new_role)
