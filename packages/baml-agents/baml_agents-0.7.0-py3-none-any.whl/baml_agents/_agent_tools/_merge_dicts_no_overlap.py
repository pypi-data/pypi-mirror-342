from typing import Any


def merge_dicts_no_overlap(a: dict[Any, Any], b: dict[Any, Any]) -> dict[Any, Any]:
    """Merge two dicts, error on key collisions."""
    overlap = set(a) & set(b)
    if overlap:
        raise KeyError(f"Collision on keys: {overlap}")
    return {**a, **b}
