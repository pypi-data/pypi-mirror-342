from __future__ import annotations

from collections.abc import Iterable

from feast import FeatureService, FeatureStore, FeatureView


def get_feature_views_from_feature_service(store: FeatureStore, feature_service: FeatureService) -> list[FeatureView]:
    feature_views: Iterable[FeatureView] = [store.get_feature_view(projection.name) for projection in feature_service.feature_view_projections]
    return feature_views
