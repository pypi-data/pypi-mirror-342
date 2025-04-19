from typing import Any, Dict, Iterable, TypeVar

T = TypeVar("T")


def merge_dicts_no_overlap(a: Dict[Any, Any], b: Dict[Any, Any]) -> Dict[Any, Any]:
    """Merge two dicts, error on key collisions."""
    overlap = set(a) & set(b)
    if overlap:
        raise KeyError(f"Collision on keys: {overlap}")
    return {**a, **b}


def sole(items: Iterable[T]) -> T:
    lst = list(items)
    if len(lst) != 1:
        raise ValueError(f"Expected single element, got {len(lst)}")
    return lst[0]
