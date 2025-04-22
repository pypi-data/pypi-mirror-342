from __future__ import annotations

from typing import Any

import pandas as pd
import ray.data
from feast import Entity, FeatureService, FeatureStore, Field, RepoConfig

from almanak.mlops.feature_store.create_feature_view import (
    create_feature_view as _create_feature_view,
)
from almanak.mlops.feature_store.entity_records_to_rows import (
    entity_records_to_entity_rows as _entity_records_to_entity_rows,
)
from almanak.mlops.feature_store.launch_ui import launch_ui as _launch_ui
from almanak.mlops.feature_store.materialize_training_features import (
    materialize_to_polars as _materialize_to_polars,
)
from almanak.mlops.feature_store.materialize_training_features import (
    materialize_to_ray_dataset as _materialize_to_ray_dataset,
)


class AlmanakFeatureStore(FeatureStore):
    def __init__(
        self,
        feature_store_name: str = "europe_west4",
        repo_config: RepoConfig = None,
        fs_yaml_file: str = None,
    ):
        """Use this class to interact with the Almanak Feature Store.
        Provide a feature_store_name to use the default sdk config.
        Provide exactly one of either a config or a fs_yaml_file to override the default sdk config.
        """
        return self._configure_feature_store(feature_store_name, repo_config, fs_yaml_file)

    def _configure_feature_store(self, feature_store_name, repo_config):
        super().__init__(config=repo_config)
        self.name = feature_store_name

    @property
    def name(self):
        return self._feature_store_name

    @name.setter
    def name(self, feature_store_name: str):
        self._feature_store_name = feature_store_name

    @property
    def repo_descriptor(self):
        return self._repo_descriptor

    @repo_descriptor.setter
    def repo_descriptor(self, repo_descriptor: dict[str, Any]):
        self._repo_descriptor = repo_descriptor

    def create_feature_view(
        self,
        feature_view_name: str,
        select_sql: str,
        entities: list[Entity],
        timestamp_field: str,
        schema: list[Field] | None,
        owner: str,
        description: str = None,
        tags: dict[str, str] = None,
    ):
        _create_feature_view(
            feature_store=self,
            feature_view_name=feature_view_name,
            select_sql=select_sql,
            entities=entities,
            timestamp_field=timestamp_field,
            schema=schema,
            owner=owner,
            description=description,
            tags=tags,
        )

    def materialize_to_ray_dataset(
        self,
        entity_df: pd.DataFrame,
        features: list[str] | FeatureService,
    ) -> ray.data.Dataset:
        return _materialize_to_ray_dataset(
            self,
            entity_df,
            features,
        )

    def materialize_to_polars(
        self,
        entity_df: pd.DataFrame,
        features: list[str] | FeatureService,
    ):
        return _materialize_to_polars(self, entity_df, features)

    def launch_ui(self, port: int = 5000):
        return _launch_ui(self, port)

    @staticmethod
    def entity_records_to_entity_rows(
        entity_records: dict[str, Any],
    ) -> list[dict[str, Any]]:
        return _entity_records_to_entity_rows(entity_records)


if __name__ == "__main__":
    AlmanakFeatureStore().launch_ui()
