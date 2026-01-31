from typing import Callable

def catch_errors(func: Callable, handler: Callable,*args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return handler(e)