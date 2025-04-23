"""Provide common utilities."""

from typing import Any, Type, TypeVar, Union

T = TypeVar('T')


def lookup_subclasses(obj: Type[T]) -> set[Type[T]]:
    """Get all unique subsclasses of a class object."""
    return set(obj.__subclasses__()).union(
        [s for c in obj.__subclasses__() for s in lookup_subclasses(c)]
    )


def to_bool(value: Union[bool, int, str]) -> bool:
    """Convert truthy statement to boolean."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value = value.lower()
    if value in ('y', 'yes', 't', 'true', 'on', '1', 1):
        return True
    if value in ('n', 'no', 'f', 'false', 'off', '0', 0):
        return False
    raise ValueError(f"invalid truthy statement: {value!r}")


def tuplize(value: Any) -> tuple[Any, ...]:
    """Convert various collection types to tuple."""
    return tuple(value) if type(value) in (list, tuple) else (value,)
