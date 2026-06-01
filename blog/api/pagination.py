DEFAULT_LIMIT = 50
MAX_LIMIT = 100


def page_bounds(limit: int, offset: int) -> tuple[int, int]:
    limit = min(max(limit, 1), MAX_LIMIT)
    offset = max(offset, 0)
    return offset, offset + limit
