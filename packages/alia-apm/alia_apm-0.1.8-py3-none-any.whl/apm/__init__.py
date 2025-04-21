from typing import Callable, TypeVar, ParamSpec


P = ParamSpec("P")
R = TypeVar("R")


def function_registry(registry: dict[str, Callable[..., object]]) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        registry[func.__name__] = func
        return func
    return decorator


__all__ = ["function_registry"]
