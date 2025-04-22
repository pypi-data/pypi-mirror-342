from dataclasses import dataclass

import feast.types
from feast import BigQuerySource, Entity, FeatureStore, FeatureView, Field


@dataclass
class FeastTypes:
    """These are the primitive feast types that can be used in the schema of a feature view."""

    BYTES = feast.types.Bytes
    STRING = feast.types.String
    BOOL = feast.types.Bool
    INT32 = feast.types.Int32
    INT64 = feast.types.Int64
    FLOAT32 = feast.types.Float32
    FLOAT64 = feast.types.Float64
    UNIX_TIMESTAMP = feast.types.UnixTimestamp


def create_feature_view(
    feature_store: FeatureStore,
    feature_view_name: str,
    select_sql: str,
    entities: list[Entity],
    timestamp_field: str,
    schema: list[Field] | None,
    owner: str,
    description: str = None,
    tags: dict[str, str] = None,
):
    """Create a feature view in Feast.
    feature_store: Feast feature store
    feature_view_name: Name of the feature view
    select_sql: Bigquery SQL query to select the features. The query itself should not create the view and should not include a limit clause.
    entities: List of Feast entities
    timestamp_field: Name of the timestamp field in the Bigquery table
    schema: List of tuples of the form (name of column, column type) where type is a Feast type.
    owner: Owner of the feature view
    description (optional): Description of the feature view
    tags (optional): Tags to add to the feature view
    """
    dynamic_bigquery_source = BigQuerySource(
        name=f"{feature_view_name}_source",
        query=select_sql,
        timestamp_field=timestamp_field,
        description=description,
    )
    dynamic_feature_view = FeatureView(
        name=feature_view_name,
        entities=entities,
        schema=schema,
        source=dynamic_bigquery_source,
        description=description,
        tags={"view_type": "dynamic", **tags},
        owner=owner,
    )
    feature_store.apply([dynamic_bigquery_source, *entities, dynamic_feature_view])
    print("Feature view created successfully")
