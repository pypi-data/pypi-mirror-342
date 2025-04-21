# -*- coding: utf-8 -*-

"""
Pagination utility for Short.io API calls.

This module provides a flexible, universal pagination mechanism that can convert
any single-page API method into an auto-paginating iterator. It's designed around
the concept of "pagination abstraction" - decoupling the pagination logic from
specific API endpoints while accommodating different pagination implementations.
"""

import typing as T


def _paginate(
    method: T.Callable,
    list_key: str,
    get_next_token: T.Callable,
    set_next_token: T.Callable,
    kwargs: T.Optional[dict[str, T.Any]] = None,
    max_results: T.Optional[int] = None,
) -> dict[str, T.Any]:
    """
    Convert a single API call into a generator that handles pagination.

    This universal pagination mechanism takes any API method and transforms it into
    an auto-paginating iterator. It abstracts away the details of token-based
    pagination by using callback functions to extract and apply pagination tokens.

    The design allows this single function to work with any API method that follows
    a basic request-response pattern with token-based pagination, regardless of the
    specific endpoint or resource type. This flexibility comes from:

    Example, to implement paginated listing of links:

    .. code-block:: python

        def pagi_list_links(self, domain_id, ...):
            def get_next_token(res):
                return res.get("nextPageToken")

            def set_next_token(kwargs, next_token):
                kwargs["page_token"] = next_token

            yield from _paginate(
                method=self.list_link,
                list_key="links",
                get_next_token=get_next_token,
                set_next_token=set_next_token,
                kwargs={"domain_id": domain_id, ...},
                max_results=total_max_results,
            )

    .. note::

        This function will continue to yield results until either:

        1. There are no more pages (next_token is None)
        2. The max_results limit is reached

        Each yield produces the exact same return value structure as the original method

    :param method: The original API method to call (e.g., list_link)
    :param list_key: The key in the response JSON that contains the list of items
    :param get_next_token: Function that extracts the next page token from a response
    :param set_next_token: Function that sets the next page token in the kwargs
    :param kwargs: Original kwargs to pass to the method
    :param max_results: Total maximum results to return across all pages
    """
    n = 0
    if kwargs is None: # pragma: no cover
        kwargs = {}

    while 1:
        response, result = method(**kwargs)
        response_data = response.json()
        n += len(response_data.get(list_key, []))
        yield response, result

        if n >= max_results: # pragma: no cover
            break

        next_token = get_next_token(response_data)
        if next_token is None:
            break
        else:
            set_next_token(kwargs, next_token)