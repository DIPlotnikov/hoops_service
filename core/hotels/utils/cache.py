from datetime import datetime
from functools import wraps

_cache = {}


def cache(func):
    """
    Декоратор кеширования данных
    @param func: Функция
    @return: Результат вычислений func
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = (func.__name__, args, tuple(kwargs.items()))
        cache_value = _cache.get(cache_key)
        if cache_value:
            if cache_value["expires"] < datetime.now().timestamp():
                del _cache[cache_key]
            return cache_value["data"]
        res = func(*args, **kwargs)
        _cache[cache_key] = {"data": res, "expires": datetime.now().timestamp() + 60}
        return res

    return wrapper
