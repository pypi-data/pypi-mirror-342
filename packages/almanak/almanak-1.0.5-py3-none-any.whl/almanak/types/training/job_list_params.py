from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["JobListParams"]


class JobListParams(TypedDict, total=False):
    after: str
    """Identifier for the last job from the previous pagination request."""

    limit: int
    """Number of training jobs to retrieve."""
