from __future__ import annotations

import asyncio
import builtins
import os

from almanak._base_client import make_request_options
from almanak._files import upload_files
from almanak._resource import SyncAPIResource
from almanak._utils import maybe_transform
from almanak.pagination import SyncPage
from almanak.types.artifact import ArtifactDeleted
from almanak.types.artifact_version import (
    ArtifactDownloadUrl,
    ArtifactFileReturn,
    ArtifactUploadUrl,
    ArtifactVersion,
    ArtifactVersionRetrieved,
    ArtifactVersionUpdated,
    ArtifactVersionUpdateParams,
)

__all__ = ["Versions"]


class Versions(SyncAPIResource):
    def list(self, artifact_name: str, *, limit: int = 100, offset: int = 0, **kwargs) -> SyncPage[ArtifactVersion]:
        return self._get_api_list(
            f"/library/artifacts/{artifact_name}/versions",
            page=SyncPage[ArtifactVersion],
            options=make_request_options(**kwargs),
            model=ArtifactVersion,
            body={"limit": limit, "offset": offset},
            unpack_by_keys=["data"],
            page_key="artifact_id_version",
        )

    def retrieve(self, artifact_name: str, version: str, **kwargs) -> ArtifactVersion:
        return self._get(
            f"/library/artifacts/{artifact_name}/versions/{version}",
            options=make_request_options(**kwargs),
            cast_to=ArtifactVersionRetrieved,
            unpack_by_keys=["data"],
            page_key="artifact_id_version",
        )

    def download(self, artifact_name: str, version: str, **kwargs) -> ArtifactDownloadUrl:
        return self._get(
            f"/library/artifacts/{artifact_name}/versions/{version}/url",
            options=make_request_options(**kwargs),
            cast_to=ArtifactDownloadUrl,
            unpack_by_keys=["data", "generateArtifactDownloadUrl"],
        )

    def get_uris(self, artifact_name: str, version: str, **kwargs) -> ArtifactFileReturn:
        return self._get(
            f"/library/artifacts/{artifact_name}/versions/{version}/uri",
            options=make_request_options(**kwargs),
            cast_to=ArtifactFileReturn,
            unpack_by_keys=["data"],
            page_key="artifact_files",
        )

    def upload(self, artifact_name: str, version: str, files: builtins.list[str], **kwargs) -> ArtifactUploadUrl:
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
            file = file.replace("\\", "/")

        response = self._post(
            f"/library/artifacts/{artifact_name}/versions/{version}/upload",
            body={"files": files},
            options=make_request_options(**kwargs),
            cast_to=ArtifactUploadUrl,
            unpack_by_keys=["data", "generateArtifactUploadUrls"],
        )

        upload_results = asyncio.run(upload_files(response.urls, all_files))

        if all(status == 200 for status in upload_results):
            return response
        else:
            raise Exception(f"Failed to upload one or more files, {response}")

    def update(
        self,
        artifact_name: str,
        version: str,
        *,
        updates: dict,
        **kwargs,
    ) -> ArtifactVersionUpdated:
        body = {
            "updates": updates,
        }
        return self._post(
            f"/library/artifacts/{artifact_name}/versions/{version}",
            body=maybe_transform(body, ArtifactVersionUpdateParams),
            options=make_request_options(**kwargs),
            cast_to=ArtifactVersionUpdated,
            unpack_by_keys=["data", "update_artifact_id_version"],
            page_key="returning",
        )

    def delete(self, artifact_name: str, version: str, **kwargs) -> ArtifactDeleted:
        return self._delete(
            f"/library/artifacts/{artifact_name}/versions/{version}",
            options=make_request_options(**kwargs),
            cast_to=ArtifactDeleted,
            unpack_by_keys=["data", "delete_artifact_id_version"],
            page_key="returning",
        )
