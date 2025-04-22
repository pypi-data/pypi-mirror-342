from typing import Any


def entity_records_to_entity_rows(
    entity_records: dict[str, Any],
) -> list[dict[str, Any]]:
    return [{attribute: value} for attribute, collection in entity_records.items() for value in collection]
