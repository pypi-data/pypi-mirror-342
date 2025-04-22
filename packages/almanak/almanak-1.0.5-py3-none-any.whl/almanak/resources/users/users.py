from __future__ import annotations

from ..._compat import cached_property
from ..._resource import SyncAPIResource
from .user import User

__all__ = ["Users"]


class Users(SyncAPIResource):
    @cached_property
    def user(self) -> User:
        return User(self._client)
