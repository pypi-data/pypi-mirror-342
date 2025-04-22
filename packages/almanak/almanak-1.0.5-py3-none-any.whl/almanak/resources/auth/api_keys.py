from __future__ import annotations

import httpx

from ..._base_client import (
    make_request_options,
)
from ..._resource import SyncAPIResource
from ..._types import NOT_GIVEN, Body, Headers, NotGiven, Query
from ...types.api_key import ApiKey

__all__ = ["ApiKeys"]


class ApiKeys(SyncAPIResource):
    def retrieve(
        self,
        api_key: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApiKey:
        if not api_key:
            raise ValueError(f"Expected a non-empty value for `api_key_id` but received {api_key!r}")
        return self._get(
            f"/auth/api_keys/{api_key}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=ApiKey,
        )
