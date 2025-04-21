def get(obj: dict, key: str, fallback=None):
    items = key.split(".", 1)
    if len(items) > 1:
        for i in items:
            return get(obj, i, fallback)
    elif items:
        return obj.get(key, fallback)

    return fallback
