# -*- coding: utf-8 -*-

"""
Argument manipulation utilities.

This module provides utilities for handling required and optional parameters
in the context of HTTP API requests and dataclass constructors. It defines
sentinel values and helper functions to:

1. Mark parameters as explicitly required (:attr:`REQ`)
2. Mark parameters as explicitly "Not Applicable" (:attr:`NA`) rather than using None
3. Remove ``NA`` values from kwargs before sending to HTTP APIs

The sentinel values REQ and NA help maintain proper dataclass field ordering
since dataclasses don't allow required fields (those without defaults) to be
defined after fields with default values. By using these sentinels, we can
define required and optional fields in any order without worrying about
dataclass constraints.

When mapping Python function arguments to HTTP request parameters, the rm_na
function can be called to remove all NA values from the keyword arguments
dictionary before sending the request.
"""

import dataclasses

from .type_hint import T_KWARGS


@dataclasses.dataclass(frozen=True)
class _REQUIRED:
    def __eq__(self, other):
        return isinstance(other, _REQUIRED)


REQ = _REQUIRED()


@dataclasses.dataclass(frozen=True)
class _NOTHING:
    def __eq__(self, other):
        print(self, other)
        return isinstance(other, _NOTHING)


NA = _NOTHING()


def rm_na(**kwargs) -> T_KWARGS:
    """

    Remove NA values from kwargs.

    This function filters out any keyword arguments that have the NA sentinel value.
    It's particularly useful when preparing parameters for HTTP API requests
    where you want to exclude optional parameters that weren't provided.

    Example:
    >>> params = {"domain_id": 123, "limit": 10, "offset": NA}
    >>> filtered_params = rm_na(**params)
    >>> # filtered_params will be {"domain_id": 123, "limit": 10}
    """
    return {
        key: value
        for key, value in kwargs.items()
        if isinstance(value, _NOTHING) is False
    }
