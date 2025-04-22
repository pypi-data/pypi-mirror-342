import os
from pathlib import Path

import requests
from pydantic import BaseModel

DEBUG = True

SIGNING_SERVICE_URL = "https://functions.stage.almanak.co/v1/mlops_training_artifacts_presigned_urls_creation"


class LocalFilePath(str):
    """A string that represents a local file path."""


class GCSSignedURL(str):
    """A string that represents a signed URL for a GCS object."""


def generate_file_tree(local_directory: Path) -> dict:
    file_tree = [str(file.relative_to(local_directory)) for file in local_directory.rglob("*") if file.is_file()]
    return file_tree


class SignedUrlResponse(BaseModel):
    preSignedUrlsMappings: dict[LocalFilePath, GCSSignedURL]
    gcsBaseDir: str


def create_signed_urls_for_file_tree(
    file_tree: list[str],
) -> dict:
    payload = {
        "filePaths": file_tree,
    }
    post_request_args = dict(url=SIGNING_SERVICE_URL, json=payload)
    if DEBUG:
        post_request_args["headers"] = {"PLATFORM_SECRET_ACCESS_KEY": os.getenv("PLATFORM_SECRET_ACCESS_KEY")}
    response = requests.post(**post_request_args, timeout=60)
    response.raise_for_status()
    response_payload = response.json()

    return response_payload


def upload_file_to_presigned_url(file_path, url, fields):
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f)}
        response = requests.post(url, data=fields, files=files, timeout=60)
        return response


def upload_training_artifacts(directory_to_upload: Path):
    file_tree: list[str] = generate_file_tree(directory_to_upload)
    pre_signed_urls_response = create_signed_urls_for_file_tree(file_tree)

    # Loop through the preSignedUrlsMappings and upload files
    pre_signed_urls_mappings = pre_signed_urls_response["preSignedUrlsMappings"]

    for file_name, url_info in pre_signed_urls_mappings.items():
        local_file_path = str(directory_to_upload / file_name)
        upload_url = url_info["url"]
        upload_fields = url_info["fields"]

        response = upload_file_to_presigned_url(local_file_path, upload_url, upload_fields)
        if response.status_code == 204:
            print(f"Successfully uploaded {file_name}")
        else:
            print(f"Failed to upload {file_name}: {response.text}")
    return pre_signed_urls_response["gcsBaseDir"]


if __name__ == "__main__":
    upload_training_artifacts(Path("./test_upload_dir"))
