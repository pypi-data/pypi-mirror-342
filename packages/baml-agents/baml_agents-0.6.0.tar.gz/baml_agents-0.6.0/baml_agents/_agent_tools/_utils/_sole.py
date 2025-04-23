def sole(collection):
    """
    Return the sole (one and only) element from the collection.

    Args:
        collection: An iterable with exactly one element

    Returns:
        The single element

    Raises:
        ValueError: If collection doesn't contain exactly one element

    """
    items = list(collection)
    if len(items) != 1:
        raise ValueError(f"Expected exactly one element, found {len(items)}")
    return items[0]
