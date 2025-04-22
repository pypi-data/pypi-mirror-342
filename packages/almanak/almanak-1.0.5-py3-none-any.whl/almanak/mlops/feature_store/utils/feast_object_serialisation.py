from __future__ import annotations

from typing import Union

from feast import BigQuerySource, Entity, FeatureService, FeatureView
from feast.protos.feast.core.DataSource_pb2 import DataSource as DataSourceProto
from feast.protos.feast.core.Entity_pb2 import Entity as EntityProto
from feast.protos.feast.core.FeatureService_pb2 import (
    FeatureService as FeatureServiceProto,
)
from feast.protos.feast.core.FeatureView_pb2 import FeatureView as FeatureViewProto

FEAST_OBJECT_PROTO_MAP = {
    BigQuerySource: DataSourceProto,
    Entity: EntityProto,
    FeatureView: FeatureViewProto,
    FeatureService: FeatureServiceProto,
}

FeastObject = Union[FeatureService, FeatureView, BigQuerySource, Entity]

FEAST_PROTO_BYTES_ENCODING = "latin-1"


def serialize_feast_object(feast_object: FeastObject) -> str:
    serialised_object_string = feast_object.to_proto().SerializeToString().decode(FEAST_PROTO_BYTES_ENCODING)
    return serialised_object_string


def deserialize_feast_object(
    feast_object_bytes_string: str,
    feast_object_type: type[FeastObject],
    bytes_string_encoding: str = FEAST_PROTO_BYTES_ENCODING,
) -> FeastObject:
    proto = FEAST_OBJECT_PROTO_MAP[feast_object_type]
    feast_object = feast_object_type.from_proto(proto.FromString(feast_object_bytes_string.encode(bytes_string_encoding)))
    return feast_object


def _test():
    from almanak.almanak_mlops.feature_store import AlmanakFeatureStore

    feature_service = AlmanakFeatureStore().get_feature_service("eth_contracts_service_v1")
    serialized = serialize_feast_object(feature_service)
    print(serialized)
    deserialized = deserialize_feast_object(serialized, FeatureService)
    print(deserialized)


if __name__ == "__main__":
    _test()
