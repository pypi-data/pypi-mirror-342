from typing import Optional

from pydantic import BaseModel

from almanak.mlops.feature_store.create_feature_view import (
    FeastTypes,
    create_feature_view,
)
from almanak.mlops.feature_store.entity_records_to_rows import (
    entity_records_to_entity_rows,
)
from almanak.mlops.feature_store.feature_store import (
    AlmanakFeatureStore as _AlmanakFeatureStore,
)
from almanak.mlops.feature_store.feature_store import (
    RepoConfig,
)
from almanak.mlops.feature_store.launch_ui import launch_ui
from almanak.mlops.feature_store.materialize_training_features import (
    materialize_to_polars,
    materialize_to_ray_dataset,
)


class OfflineStoreConfigModel(BaseModel):
    type: str
    dataset: str
    location: str


class RepoConfigModel(BaseModel):
    """Feature Store configuration model."""

    project: str
    registry: str
    provider: str
    offline_store: OfflineStoreConfigModel
    entity_key_serialization_version: int


class AlmanakFeatureStore(_AlmanakFeatureStore):
    def __init__(self, feature_store_name: str, repo_config: dict | None = None):
        if repo_config is None:
            repo_config = {
                "project": feature_store_name,
                "registry": "gs://almanak-data-lake-prod/feast/registry/public.registry",
                "provider": "gcp",
                "offline_store": {
                    "type": "bigquery",
                    "dataset": "feast_europe_west4",
                    "location": "europe-west4",
                },
                "entity_key_serialization_version": 2,
            }

        repo_config: RepoConfigModel = RepoConfigModel(**repo_config)

        super().__init__(
            feature_store_name,
            repo_config=RepoConfig(**repo_config.dict()),
        )


__all__ = [
    "AlmanakFeatureStore",
    "FeastTypes",
    "create_feature_view",
    "entity_records_to_entity_rows",
    "launch_ui",
    "materialize_to_polars",
    "materialize_to_ray_dataset",
]
