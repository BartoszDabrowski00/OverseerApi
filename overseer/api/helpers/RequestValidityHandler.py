from typing import Optional
from flask import request
from flask_restx import abort
import string

from overseer.api.auth.authorization_service import AuthorizationService
from overseer.api.users.user_service import UserService


class RequestValidityHandler:

    authorization_service = AuthorizationService()
    user_service = UserService()
    id_valid_length = 24

    @classmethod
    def check_user_authorization(cls) -> Optional[str]:
        current_user_id = cls.authorization_service.check_if_authorized(request.headers)
        if current_user_id is None:
            abort(401, result='UNAUTHORIZED user must be logged in')

        return current_user_id

    @classmethod
    def check_user_existence(cls, user_id: str):
        if not cls.user_service.check_if_user_exists(user_id):
            abort(404, result='NOT FOUND user does not exist')

    @classmethod
    def check_if_valid_id(cls, *args):
        for user_id in args:
            is_hex_str = set(user_id).issubset(string.hexdigits)
            if len(user_id) != cls.id_valid_length or not is_hex_str:
                abort(404, result='BAD REQUEST id must be 24-character hex string')

