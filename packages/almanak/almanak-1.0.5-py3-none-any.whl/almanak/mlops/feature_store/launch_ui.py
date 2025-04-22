from feast import FeatureStore


def launch_ui(feature_store: FeatureStore, port: int = 5000):
    feature_store.serve_ui(
        host="127.0.0.1",
        port=port,
        get_registry_dump=lambda: None,
        registry_ttl_sec=300,
    )
