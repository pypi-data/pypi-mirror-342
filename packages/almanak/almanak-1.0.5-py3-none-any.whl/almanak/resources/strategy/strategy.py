from __future__ import annotations

import asyncio
import json
import os
from typing import TYPE_CHECKING

from almanak._files import upload_files
from almanak.types.artifact_version import ArtifactVersionUploaded, PresignedUrl

if TYPE_CHECKING:
    from almanak._client import Almanak

from ..._base_client import make_request_options
from ..._resource import SyncAPIResource

__all__ = ["Strategy"]


class Strategy(SyncAPIResource):
    """
    High Level Strategy API Client
    """

    _client: Almanak

    def get_strategy(self, strategy_id: str, **kwargs) -> Strategy:
        return self._get(
            f"/strategies/{strategy_id}",
            options=make_request_options(**kwargs),
            cast_to=Strategy,
        )

    def upload_strategy(self, strategy_id: str, **kwargs) -> Strategy:
        return self._post(
            f"/strategies/{strategy_id}",
            options=make_request_options(**kwargs),
            cast_to=Strategy,
        )

    def delete_strategy(self, strategy_id: str, **kwargs) -> Strategy:
        return self._delete(
            f"/strategies/{strategy_id}",
            options=make_request_options(**kwargs),
            cast_to=Strategy,
        )

    def update_strategy(self, strategy_id: str, **kwargs) -> Strategy:
        return self._put(
            f"/strategies/{strategy_id}",
            options=make_request_options(**kwargs),
            cast_to=Strategy,
        )

    def download_strategy(self, strategy_name: str, strategy_id: str, version_id: str, output_dir) -> Strategy:
        response = self._client._hasura_client.generate_strategy_download_by_strategy_id(strategy_id, version_id)
        if "errors" in response:
            raise Exception(response["errors"])

        json_schema = response["data"]["generateArtifactFilesDownloadUrl"]["files"]
        if len(json_schema) == 0:
            return None

        result = json.loads(json_schema)

        folder_dir = output_dir
        if output_dir == ".":
            folder_dir = os.path.join(output_dir, strategy_name)

        all_files = []
        folders_to_process = [result]

        while folders_to_process:
            current_folder = folders_to_process.pop()
            all_files.extend(current_folder["files"])
            if "folders" in current_folder:
                folders_to_process.extend(current_folder["folders"])

        for _file in all_files:
            result = self._get(_file["metadata"]["presigned_url"], cast_to=bytes)

            # Remove the first slash and join the rest of the path
            full_path = os.path.join(folder_dir, _file["path"])

            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "wb") as f:
                f.write(result)

        return os.path.abspath(folder_dir)

    def trigger_scan(self, artifact_version_id: str) -> dict:
        response = self._client._hasura_client.trigger_scan(artifact_version_id=artifact_version_id)
        if "errors" in response:
            raise Exception(response["errors"])
        return response["data"]["scanArtifactVersion"]

    def get_version_id_by_name(self, strategy_id: str, version_name: str) -> str:
        response = self._client._hasura_client.get_version_id_by_name(strategy_id, version_name)
        if "errors" in response:
            raise Exception(response["errors"])
        if len(response["data"]["artifact_id_version"]) == 0:
            raise Exception(f"Version {version_name} not found")
        return response["data"]["artifact_id_version"][0]["id"]

    def upload_new_version(self, strategy_id: str, files: list[str]) -> ArtifactVersionUploaded:
        all_files = []

        for file in files:
            # Check if the provided path is a directory
            file = file.replace("\\", "/") # this is to ensure that the file path is correct for windows
            if os.path.isdir(file):
                for root, _, filenames in os.walk(file):
                    for filename in filenames:
                        # Preserve the tree structure
                        relative_path = os.path.relpath(os.path.join(root, filename), file)
                        all_files.append(relative_path)
            else:
                all_files.append(file)

        response = self._client._hasura_client.generate_strategy_version_id_upload_url(strategy_id, all_files)
        if "errors" in response:
            raise Exception(response["errors"])

        response_data = response["data"]["generateStrategyVersionIdUploadUrl"]
        artifact_version_uploaded = ArtifactVersionUploaded(
            success=response_data["success"],
            rootUri=response_data["rootUri"],
            version=response_data["version"],
            versionId=response_data["versionId"],
        )

        urls = response["data"]["generateStrategyVersionIdUploadUrl"]["urls"]

        mapped_urls: list[PresignedUrl] = []
        for url in urls:
            mapped_urls.append(PresignedUrl(presigned_url=url["presigned_url"], relative_path=url["relative_path"]))
        artifact_version_uploaded.urls = mapped_urls

        asyncio.run(upload_files(mapped_urls, all_files))

        if response["data"]["generateStrategyVersionIdUploadUrl"]["success"]:
            return artifact_version_uploaded
        else:
            raise Exception(f"Failed to upload one or more files, {response}")

    def update_strategy_version(self, strategy_id: str, version_id: str, metadata: dict, description: str):
        response = self._client._hasura_client.update_strategy_version(strategy_id, version_id, metadata, description)
        if "errors" in response:
            raise Exception(response["errors"])
        return response["data"]["update_artifact_id_version"]
