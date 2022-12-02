from typing import Any

from overseer.api.auth.roles import Role


class Rbac:

    @classmethod
    def has_access(cls, current: dict[str, Any], owner_id: str) -> bool:
        pass


class AdminOrOwner(Rbac):

    @classmethod
    def has_access(cls, current: dict[str, Any], owner_id: str) -> bool:
        if current["role"] == Role.admin.value:
            return True

        return current["_id"] == owner_id


class AdminOrLeaderOwner(Rbac):

    @classmethod
    def has_access(cls, current: dict[str, Any], owner_id: str) -> bool:
        if current["role"] == Role.admin.value:
            return True

        return current["role"] == Role.leader.value and current["_id"] == owner_id

class AdminOrLeaderOrOwner(Rbac):

    @classmethod
    def has_access(cls, current: dict[str, Any], owner_id: str) -> bool:
        if current["role"] == Role.admin.value or current["role"] == Role.leader.value:
            return True

        return current["_id"] == owner_id


class Admin(Rbac):

    @classmethod
    def has_access(cls, current: dict[str, Any], owner_id: str) -> bool:
        return current["role"] == Role.admin.value


class AdminOrLeader(Rbac):

    @classmethod
    def has_access(cls, current: dict[str, Any], owner_id: str) -> bool:
        return current["role"] == Role.admin.value or current["role"] == Role.leader.value


class AdminOrLeaderOrUser(Rbac):

    @classmethod
    def has_access(cls, current: dict[str, Any], owner_id: str) -> bool:
        return current["role"] == Role.admin.value or current["role"] == Role.leader.value \
               or current["role"] == Role.user.value





