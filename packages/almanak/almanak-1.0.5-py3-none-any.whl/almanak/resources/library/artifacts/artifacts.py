from __future__ import annotations

import asyncio
import builtins
import os

from almanak._base_client import make_request_options
from almanak._files import upload_files
from almanak._resource import SyncAPIResource
from almanak._utils import maybe_transform
from almanak.pagination import SyncPage
from almanak.resources.library.artifacts.versions import Versions
from almanak.types.artifact import (
    Artifact,
    ArtifactCreated,
    ArtifactCreateParams,
    ArtifactDeleted,
    ArtifactQueryResult,
    ArtifactUpdated,
    ArtifactUpdateParams,
    ArtifactVersionLatestReturn,
)
from almanak.types.artifact_version import ArtifactVersionUploaded

__all__ = ["Artifacts"]


class Artifacts(SyncAPIResource):
    @property
    def versions(self) -> Versions:
        return Versions(self._client)

    def create(
        self,
        *,
        artifact_name: str,
        description: str | None = None,
        type: str,
        metadata: dict | None = None,
        is_public: bool = False,
    ) -> ArtifactCreated:
        body = {
            "name": artifact_name,
            "description": description,
            "type": type,
            "metadata": metadata,
            "is_public": is_public,
        }
        return self._post(
            "library/artifacts",
            body=maybe_transform(body, ArtifactCreateParams),
            options=make_request_options(),
            cast_to=ArtifactCreated,
            unpack_by_keys=["data", "insert_artifacts_one"],
        )

    def retrieve(self, artifact_name: str, **kwargs) -> ArtifactQueryResult:
        return self._get(
            f"/library/artifacts/{artifact_name}",
            options=make_request_options(**kwargs),
            cast_to=ArtifactQueryResult,
            unpack_by_keys=["data"],
            page_key="artifacts",
        )

    def retrieve_latest(self, artifact_name: str, **kwargs) -> ArtifactVersionLatestReturn:
        return self._get(
            f"/library/artifacts/{artifact_name}/latest",
            options=make_request_options(**kwargs),
            cast_to=ArtifactVersionLatestReturn,
            unpack_by_keys=["data"],
            page_key="artifacts",
        )

    def upload_new_version(self, artifact_name: str, files: builtins.list[str], **kwargs) -> ArtifactVersionUploaded:
        all_files = []

        for file in files:
            # Check if the provided path is a directory
            if os.path.isdir(file):
                for root, _, filenames in os.walk(file):
                    for filename in filenames:
                        # Preserve the tree structure
                        relative_path = os.path.relpath(os.path.join(root, filename), file)
                        all_files.append(relative_path)
            else:
                all_files.append(file)

        response = self._post(
            f"/library/artifacts/{artifact_name}/versions",
            body={"files": all_files},
            options=make_request_options(**kwargs),
            cast_to=ArtifactVersionUploaded,
            unpack_by_keys=["data", "generateArtifactVersionUploadUrl"],
        )

        upload_results = asyncio.run(upload_files(response.urls, all_files))

        if all(status == 200 for status in upload_results):
            return response
        else:
            raise Exception(f"Failed to upload one or more files, {response}")

    def list(self, *, limit: int = 100, offset: int = 0, **kwargs) -> SyncPage[Artifact]:
        return self._get_api_list(
            "/library/artifacts/",
            page=SyncPage[Artifact],
            options=make_request_options(**kwargs),
            model=Artifact,
            body={"limit": limit, "offset": offset},
            unpack_by_keys=["data"],
            page_key="artifacts",
        )

    def delete(self, artifact_name: str, **kwargs) -> ArtifactDeleted:
        return self._delete(
            f"/library/artifacts/{artifact_name}",
            options=make_request_options(**kwargs),
            cast_to=ArtifactDeleted,
            unpack_by_keys=["data", "delete_artifacts"],
            page_key="returning",
        )

    def update(
        self,
        artifact_name: str,
        *,
        updates: dict,
        **kwargs,
    ) -> ArtifactUpdated:
        body = {"updates": updates}
        return self._post(
            f"/library/artifacts/{artifact_name}",
            body=maybe_transform(body, ArtifactUpdateParams),
            options=make_request_options(**kwargs),
            cast_to=ArtifactUpdated,
            unpack_by_keys=["data", "update_artifacts"],
            page_key="returning",
        )
