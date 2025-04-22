from __future__ import annotations

from collections.abc import Iterable

import httpx

from ...._base_client import (
    make_request_options,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource
from ...._types import NOT_GIVEN, Body, Headers, NotGiven, Query
from ...._utils import (
    maybe_transform,
)
from ....pagination import SyncCursorPage
from ....types.training import (
    job_create_params,
    job_list_events_params,
    job_list_params,
)
from ....types.training.training_job import TrainingJob
from ....types.training.training_job_event import TrainingJobEvent
from .checkpoints import (
    Checkpoints,
)

__all__ = ["Jobs"]


class Jobs(SyncAPIResource):
    @cached_property
    def checkpoints(self) -> Checkpoints:
        return Checkpoints(self._client)

    def create(
        self,
        *,
        model: str,
        training_file: str,
        hyperparameters: job_create_params.Hyperparameters | NotGiven = NOT_GIVEN,
        integrations: Iterable[job_create_params.Integration] | None | NotGiven = NOT_GIVEN,
        seed: int | None | NotGiven = NOT_GIVEN,
        suffix: str | None | NotGiven = NOT_GIVEN,
        validation_file: str | None | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TrainingJob:
        return self._post(
            "/training/jobs",
            body=maybe_transform(
                {
                    "model": model,
                    "training_file": training_file,
                    "hyperparameters": hyperparameters,
                    "integrations": integrations,
                    "seed": seed,
                    "suffix": suffix,
                    "validation_file": validation_file,
                },
                job_create_params.JobCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=TrainingJob,
        )

    def retrieve(
        self,
        training_job_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TrainingJob:
        """
        Get info about a training job.

        [Learn more about training](https://platform.almanak.com/docs/guides/training)

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not training_job_id:
            raise ValueError(f"Expected a non-empty value for `training_job_id` but received {training_job_id!r}")
        return self._get(
            f"/training/jobs/{training_job_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=TrainingJob,
        )

    def list(
        self,
        *,
        after: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPage[TrainingJob]:
        """
        List your organization's training jobs

        Args:
          after: Identifier for the last job from the previous pagination request.

          limit: Number of training jobs to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/training/jobs",
            page=SyncCursorPage[TrainingJob],
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
                    job_list_params.JobListParams,
                ),
            ),
            model=TrainingJob,
        )

    def cancel(
        self,
        training_job_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TrainingJob:
        """
        Immediately cancel a train job.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not training_job_id:
            raise ValueError(f"Expected a non-empty value for `training_job_id` but received {training_job_id!r}")
        return self._post(
            f"/training/jobs/{training_job_id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=TrainingJob,
        )

    def list_events(
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
    ) -> SyncCursorPage[TrainingJobEvent]:
        """
        Get status updates for a training job.

        Args:
          after: Identifier for the last event from the previous pagination request.

          limit: Number of events to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not training_job_id:
            raise ValueError(f"Expected a non-empty value for `training_job_id` but received {training_job_id!r}")
        return self._get_api_list(
            f"/training/jobs/{training_job_id}/events",
            page=SyncCursorPage[TrainingJobEvent],
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
                    job_list_events_params.JobListEventsParams,
                ),
            ),
            model=TrainingJobEvent,
        )
