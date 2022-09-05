from overseer.utils.mongo.mongo_client import MongoClient
from werkzeug.security import generate_password_hash


class RegistrationService:

    def __init__(self):
        self.mongo = MongoClient

    def register(self, email: str, name: str, surname: str, password: str) -> bool:
        user = self.mongo.find_user(email=email)
        if user is not None:
            return False

        password_hash = generate_password_hash(password)
        MongoClient.insert_new_user(email, name, surname, password_hash)
        return True



