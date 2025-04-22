# -*- coding: utf-8 -*-

import typing as T
from datetime import datetime
from functools import partial
from itertools import islice

from .arg import _NOTHING


def datetime_to_iso_string(
    dt: T.Union[_NOTHING, datetime],
) -> T.Union[_NOTHING, str]:
    if isinstance(dt, datetime):
        return dt.isoformat()
    else:
        return dt


def take(n, iterable):  # pragma: no cover
    """Return first *n* items of the iterable as a list.

        >>> take(3, range(10))
        [0, 1, 2]

    If there are fewer than *n* items in the iterable, all of them are
    returned.

        >>> take(10, range(3))
        [0, 1, 2]

    """
    return list(islice(iterable, n))


def chunked(iterable, n, strict=False):  # pragma: no cover
    """Break *iterable* into lists of length *n*:

        >>> list(chunked([1, 2, 3, 4, 5, 6], 3))
        [[1, 2, 3], [4, 5, 6]]

    By the default, the last yielded list will have fewer than *n* elements
    if the length of *iterable* is not divisible by *n*:

        >>> list(chunked([1, 2, 3, 4, 5, 6, 7, 8], 3))
        [[1, 2, 3], [4, 5, 6], [7, 8]]

    To use a fill-in value instead, see the :func:`grouper` recipe.

    If the length of *iterable* is not divisible by *n* and *strict* is
    ``True``, then ``ValueError`` will be raised before the last
    list is yielded.

    """
    iterator = iter(partial(take, n, iter(iterable)), [])
    if strict:
        if n is None:
            raise ValueError("n must not be None when using strict mode.")

        def ret():
            for chunk in iterator:
                if len(chunk) != n:
                    raise ValueError("iterable is not divisible by n.")
                yield chunk

        return iter(ret())
    else:
        return iterator


KT = T.TypeVar("KT")
VT = T.TypeVar("VT")

def group_by(
    iterable: T.Iterable[VT],
    get_key: T.Callable[[VT], KT],
) -> T.Dict[KT, T.List[VT]]: # pragma: no cover
    """
    Group items by it's key, with type hint.

    Example::

        >>> class Record:
        ...     def __init__(self, product: str, date: str, sale: int):
        ...         self.product = product
        ...         self.date = date
        ...         self.sale = sale

        >>> records = [
        ...     Record("apple", "2020-01-01", 10),
        ...     Record("apple", "2020-01-02", 20),
        ...     Record("apple", "2020-01-03", 30),
        ...     Record("banana", "2020-01-01", 10),
        ...     Record("banana", "2020-01-02", 20),
        ...     Record("banana", "2020-01-03", 30),
        ... ]

        >>> group_by(records, lambda x: x.product)
        {
            "apple": [
                Record("apple", "2020-01-01", 10),
                Record("apple", "2020-01-02", 20),
                Record("apple", "2020-01-03", 30),
            ],
            "banana": [
                Record("banana", "2020-01-01", 10),
                Record("banana", "2020-01-02", 20),
                Record("banana", "2020-01-03", 30),
            ],
        }
    """
    grouped = dict()
    for item in iterable:
        key = get_key(item)
        try:
            grouped[key].append(item)
        except KeyError:
            grouped[key] = [item]
    return grouped