from __future__ import annotations

import httpx

from ...._base_client import (
    make_request_options,
)
from ...._resource import SyncAPIResource
from ...._types import NOT_GIVEN, Body, Headers, NotGiven, Query
from ...._utils import maybe_transform
from ....pagination import SyncCursorPage
from ....types.training.jobs import checkpoint_list_params
from ....types.training.jobs.training_job_checkpoint import FineTuningJobCheckpoint

__all__ = [
    "Checkpoints",
]


class Checkpoints(SyncAPIResource):
    def list(
        self,
        training_job_id: str,
        *,
        after: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[FineTuningJobCheckpoint]:
        """
        List checkpoints for a training job.

        Args:
          after: Identifier for the last checkpoint ID from the previous pagination request.

          limit: Number of checkpoints to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not training_job_id:
            raise ValueError(f"Expected a non-empty value for `training_job_id` but received {training_job_id!r}")
        return self._get_api_list(
            f"/training/jobs/{training_job_id}/checkpoints",
            page=SyncCursorPage[FineTuningJobCheckpoint],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after": after,
                        "limit": limit,
                    },
                    checkpoint_list_params.CheckpointListParams,
                ),
            ),
            model=FineTuningJobCheckpoint,
        )
