from __future__ import annotations

from ..._compat import cached_property
from ..._resource import SyncAPIResource
from .jobs.jobs import Jobs

__all__ = ["Training"]


class Training(SyncAPIResource):
    @cached_property
    def jobs(self) -> Jobs:
        return Jobs(self._client)
