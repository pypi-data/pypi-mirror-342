from __future__ import annotations

from ..._compat import cached_property
from ..._resource import SyncAPIResource
from .api_keys import ApiKeys

__all__ = ["Auth"]


class Auth(SyncAPIResource):
    @cached_property
    def api_keys(self) -> ApiKeys:
        return ApiKeys(self._client)

    def check_jwt(self):
        response = self._client.post("/auth/check-jwt", None)
        if response.status_code != 200:
            raise ValueError("Invalid API key")
