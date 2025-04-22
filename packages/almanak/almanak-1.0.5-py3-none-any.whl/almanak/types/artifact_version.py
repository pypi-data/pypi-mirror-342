from datetime import datetime
from typing import Any, Literal

from .._models import BaseModel


class ArtifactVersion(BaseModel):
    name: str
    id: str
    description: str | None
    date_created: datetime
    metadata: dict[str, Any] | None  # Changed to Optional
    author: str
    is_public: bool
    artifact: dict[str, str]


class ArtifactVersionRetrieved(BaseModel):
    data: list[ArtifactVersion]
    object: Literal["list"]


class ArtifactVersionList(BaseModel):
    versions: list[ArtifactVersion]


class ArtifactVersionWithType(BaseModel):
    name: str
    author: str
    date_created: datetime
    description: str | None
    is_public: bool
    metadata: dict[str, Any] | None  # Changed to Optional
    artifact: dict[str, str]


class ArtifactVersionQueryResult(BaseModel):
    versions: list[ArtifactVersionWithType]


class ArtifactVersionInfo(BaseModel):
    author: str
    date_created: datetime
    description: str | None
    name: str
    id: str
    uri: str | None
    metadata: dict[str, Any] | None  # Changed to Optional


class ArtifactVersionArtifactReturn(BaseModel):
    name: str


class ArtifactVersionUpdateReturn(BaseModel):
    id: str
    artifact: ArtifactVersionArtifactReturn
    name: str


class ArtifactVersionUpdated(BaseModel):
    data: list[ArtifactVersionUpdateReturn]
    object: Literal["list"]


class ArtifactUpdatedReturn(BaseModel):
    returning: list[ArtifactVersionUpdateReturn]


class ArtifactVersionUpdateParams(BaseModel):
    updates: dict[str, Any]

    def __init__(self, **data):
        super().__init__(**data)
        self.updates = self.transform_updates()

    def transform_updates(self) -> str:
        return ",".join(f"{k}:{v}" for k, v in self.updates.items())


class PresignedUrl(BaseModel):
    id: str | None = None
    presigned_url: str | None = None
    relative_path: str | None = None


class ArtifactVersionUploaded(BaseModel):
    success: bool | None = None
    message: str | None = None
    version: str | None = None
    versionId: str | None = None
    rootUri: str | None = None
    urls: list[PresignedUrl] | None = None


class ArtifactDownloadUrl(BaseModel):
    success: bool
    message: str
    files: list[PresignedUrl]


class ArtifactUploadUrl(BaseModel):
    success: bool
    urls: list[PresignedUrl]


class ArtifactFile(BaseModel):
    id: str
    uri: str
    date_created: datetime
    description: str | None


class ArtifactFileReturn(BaseModel):
    data: list[ArtifactFile]
    object: Literal["list"]
