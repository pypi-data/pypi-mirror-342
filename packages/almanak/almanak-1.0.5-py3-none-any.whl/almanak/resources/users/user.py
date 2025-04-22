from __future__ import annotations

import httpx

from ..._base_client import (
    make_request_options,
)
from ..._resource import SyncAPIResource
from ..._types import NOT_GIVEN, Body, Headers, NotGiven, Query
from ...types.user import AlmanakUser, AlmanakUserTeam

__all__ = ["User"]


class User(SyncAPIResource):
    def retrieve_team(
        self,
        user_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AlmanakUser:
        if not user_id:
            raise ValueError(f"Expected a non-empty value for `user_id` but received {user_id!r}")
        return self._post(
            f"/users/{user_id}/team",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=AlmanakUserTeam,
        )
