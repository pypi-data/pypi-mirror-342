from __future__ import annotations

import asyncio
import io
import logging
import os
import pathlib
from typing import TypeGuard, overload

import aiofiles
import aiohttp
import anyio
from aiohttp import ClientTimeout

from ._types import (
    Base64FileInput,
    FileContent,
    FileTypes,
    HttpxFileContent,
    HttpxFileTypes,
    HttpxRequestFiles,
    RequestFiles,
)


def is_base64_file_input(obj: object) -> TypeGuard[Base64FileInput]:
    return isinstance(obj, io.IOBase) or isinstance(obj, os.PathLike)


def is_file_content(obj: object) -> TypeGuard[FileContent]:
    return isinstance(obj, bytes) or isinstance(obj, tuple) or isinstance(obj, io.IOBase) or isinstance(obj, os.PathLike) or (isinstance(obj, str) and os.path.exists(obj))


def assert_is_file_content(obj: object, *, key: str | None = None) -> None:  # nosec
    if not is_file_content(obj):
        prefix = f"Expected entry at `{key}`" if key is not None else f"Expected file input `{obj!r}`"
        raise RuntimeError(f"{prefix} to be bytes, an io.IOBase instance, PathLike or a tuple but received {type(obj)} instead. See https://github.com/almanak/almanak-python/tree/main#file-uploads") from None


@overload
def to_httpx_files(files: None) -> None: ...


@overload
def to_httpx_files(files: RequestFiles) -> HttpxRequestFiles: ...


def to_httpx_files(files: RequestFiles | None) -> HttpxRequestFiles | None:
    if files is None:
        return None
    from ._utils import is_mapping_t, is_sequence_t

    if is_mapping_t(files):
        files = {key: _transform_file(file) for key, file in files.items()}
    elif is_sequence_t(files):
        files = [(key, _transform_file(file)) for key, file in files]
    else:
        raise TypeError(f"Unexpected file type input {type(files)}, expected mapping or sequence")

    return files


def _transform_file(file: FileTypes) -> HttpxFileTypes:
    if is_file_content(file):
        if isinstance(file, os.PathLike):
            path = pathlib.Path(file)
            return (path.name, path.read_bytes())

        return file

    from ._utils import is_tuple_t

    if is_tuple_t(file):
        return (file[0], _read_file_content(file[1]), *file[2:])

    raise TypeError("Expected file types input to be a FileContent type or to be a tuple")


def _read_file_content(file: FileContent) -> HttpxFileContent:
    if isinstance(file, os.PathLike):
        return pathlib.Path(file).read_bytes()
    return file


@overload
async def async_to_httpx_files(files: None) -> None: ...


@overload
async def async_to_httpx_files(files: RequestFiles) -> HttpxRequestFiles: ...


async def async_to_httpx_files(files: RequestFiles | None) -> HttpxRequestFiles | None:
    from ._utils import is_mapping_t, is_sequence_t

    if files is None:
        return None

    if is_mapping_t(files):
        files = {key: await _async_transform_file(file) for key, file in files.items()}
    elif is_sequence_t(files):
        files = [(key, await _async_transform_file(file)) for key, file in files]
    else:
        raise TypeError("Unexpected file type input {type(files)}, expected mapping or sequence")

    return files


async def _async_transform_file(file: FileTypes) -> HttpxFileTypes:
    if is_file_content(file):
        if isinstance(file, os.PathLike):
            path = anyio.Path(file)
            return (path.name, await path.read_bytes())

        return file

    from ._utils import is_tuple_t

    if is_tuple_t(file):
        return (file[0], await _async_read_file_content(file[1]), *file[2:])

    raise TypeError("Expected file types input to be a FileContent type or to be a tuple")


async def _async_read_file_content(file: FileContent) -> HttpxFileContent:
    if isinstance(file, os.PathLike):
        return await anyio.Path(file).read_bytes()

    return file


async def upload_file(session, url, file_path, semaphore):
    """Upload a single file with rate limiting via semaphore"""
    if not os.path.exists(str(file_path)):
        raise ValueError(f"File path {file_path} does not exist")

    async with semaphore:  # Use semaphore for rate limiting
        try:
            # Read the actual file contents
            if isinstance(file_path, (str, os.PathLike)):
                async with aiofiles.open(str(file_path), "rb") as f:
                    data = await f.read()
            else:
                data = await _async_read_file_content(file_path)

            timeout = ClientTimeout(total=300)  # 5 minute timeout per file

            # Upload the actual file contents
            async with session.put(url, data=data, timeout=timeout) as response:
                status = response.status
                if status != 200:
                    logging.error(f"Failed to upload {file_path}: Status {status}")
                return status

        except Exception as e:
            logging.error(f"Error uploading {file_path}: {str(e)}")
            return 500


async def upload_files(response_urls, files):
    """Upload multiple files with concurrent uploads and rate limiting"""
    # Configure concurrent upload limits
    MAX_CONCURRENT_UPLOADS = 10
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_UPLOADS)

    # Configure session with longer timeout
    timeout = ClientTimeout(total=3600)  # 1 hour total timeout
    conn = aiohttp.TCPConnector(
        limit=MAX_CONCURRENT_UPLOADS,
        ssl=False,
    )

    async with aiohttp.ClientSession(timeout=timeout, connector=conn) as session:
        file_url_mapping = {}
        unmatched_urls = []

        # Map files to URLs and prepare file contents
        for presigned_url in response_urls:
            # Remove leading slash and normalize the presigned URL path
            relative_path = presigned_url.relative_path.lstrip('/')
            relative_path = pathlib.PurePath(relative_path).as_posix()
            matched = False
            
            for file_path in files:
                if isinstance(file_path, (str, os.PathLike)):
                    # Normalize the file path
                    normalized_file_path = pathlib.PurePath(file_path).as_posix()
                    
                    # Compare the paths directly without any leading slashes
                    if normalized_file_path == relative_path:
                        file_url_mapping[file_path] = presigned_url.presigned_url
                        matched = True
                        break
            if not matched:
                unmatched_urls.append(presigned_url)

        if unmatched_urls:
            # Provide more detailed error message
            available_files = "\n".join([str(f) for f in files])
            unmatched_paths = "\n".join([u.relative_path for u in unmatched_urls])
            raise ValueError(f"Could not match presigned URLs with provided files.\nUnmatched URLs paths:\n{unmatched_paths}\nAvailable files:\n{available_files}")

        # Create upload tasks with semaphore
        tasks = [upload_file(session, url, file_path, semaphore) for file_path, url in file_url_mapping.items()]

        # Execute uploads with progress tracking
        results = []
        for task in asyncio.as_completed(tasks):
            try:
                status = await task
                results.append(status)
            except Exception as e:
                logging.error(f"Task failed: {str(e)}")
                results.append(500)

        return results
