from __future__ import annotations

from ..._base_client import make_request_options
from ..._compat import cached_property
from ..._resource import SyncAPIResource
from ...types.library import FileDeleted
from .artifacts import Artifacts
from .strategies import Strategies

__all__ = ["Library"]


class Library(SyncAPIResource):
    """
    Low-level library API client to get Almanak resources directly
    """

    @cached_property
    def artifacts(self) -> Artifacts:
        return Artifacts(self._client)

    @cached_property
    def strategies(self) -> Strategies:
        return Strategies(self._client)

    def delete_file(self, file_id: str, **kwargs) -> FileDeleted:
        return self._delete(
            "/library/delete_artifact_file_by_id",
            body={"fileId": file_id},
            options=make_request_options(**kwargs),
            cast_to=FileDeleted,
            unpack_by_keys=["data", "delete_artifact_files"],
        )
