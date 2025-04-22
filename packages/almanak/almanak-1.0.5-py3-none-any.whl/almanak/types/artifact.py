from datetime import datetime
from typing import Any, Literal

from .._models import BaseModel


class ArtifactType(BaseModel):
    value: str


class ArtifactVersionInfo(BaseModel):
    author: str
    date_created: datetime
    description: str | None
    name: str
    id: str
    uri: str | None
    metadata: dict[str, Any] | None  # Changed to Optional


class Artifact(BaseModel):
    name: str
    author: str
    metadata: dict[str, Any] | None  # Changed to Optional
    artifact_type: ArtifactType
    date_created: datetime
    description: str | None
    id: str
    is_public: bool
    pending_public_approval: bool
    latest_public_version_artifact: ArtifactVersionInfo | None
    latest_registered_production_version_artifact: ArtifactVersionInfo | None
    latest_registered_staging_version_artifact: ArtifactVersionInfo | None
    latest_version_artifact: ArtifactVersionInfo | None


class ArtifactSpecific(BaseModel):
    name: str
    author: str
    metadata: dict[str, Any] | None  # Changed to Optional
    date_created: datetime
    description: str | None
    id: str
    is_public: bool
    pending_public_approval: bool
    latest_public_version_artifact: ArtifactVersionInfo | None
    latest_registered_production_version_artifact: ArtifactVersionInfo | None
    latest_registered_staging_version_artifact: ArtifactVersionInfo | None
    latest_version_artifact: ArtifactVersionInfo | None


class ArtifactVersionLatest(BaseModel):
    latest_public_version_artifact: ArtifactVersionInfo | None
    latest_registered_production_version_artifact: ArtifactVersionInfo | None
    latest_registered_staging_version_artifact: ArtifactVersionInfo | None
    latest_version_artifact: ArtifactVersionInfo | None


class ArtifactVersionLatestReturn(BaseModel):
    data: list[ArtifactVersionLatest]


class ArtifactCreated(BaseModel):
    id: str
    name: str
    author: str
    date_created: datetime
    description: str | None
    is_public: bool
    pending_public_approval: bool
    metadata: dict[str, Any] | None  # Changed to Optional


class ArtifactCreateParams(BaseModel):
    name: str
    description: str | None
    type: str
    metadata: dict[str, Any] | None  # Changed to Optional
    is_public: bool = False


class ArtifactSpecificCreateParams(BaseModel):
    name: str
    description: str | None
    metadata: dict[str, Any] | None  # Changed to Optional
    is_public: bool = False


class ArtifactUpdateReturn(BaseModel):
    id: str
    name: str


class ArtifactUpdated(BaseModel):
    data: list[ArtifactUpdateReturn]
    object: Literal["list"]


class ArtifactUpdateParams(BaseModel):
    data: dict[str, Any]
    object: Literal["artifact"]

    def __init__(self, **data):
        super().__init__(**data)
        self.data = self.transform_updates()

    def transform_updates(self) -> str:
        return ",".join(f"{k}:{v}" for k, v in self.data.items())


class ArtifactDeleteReturnFields(BaseModel):
    id: str
    name: str


class ArtifactDeleted(BaseModel):
    data: list[ArtifactDeleteReturnFields]  # List can be empty
    object: Literal["list"]


class ArtifactDownloadUrl(BaseModel):
    success: bool
    message: str
    files: list[dict[str, str]]


class ArtifactQueryResult(BaseModel):
    data: list[Artifact]
    object: Literal["list"]


class ArtifactSpecificQueryResult(BaseModel):
    data: list[ArtifactSpecific]
    object: Literal["list"]
