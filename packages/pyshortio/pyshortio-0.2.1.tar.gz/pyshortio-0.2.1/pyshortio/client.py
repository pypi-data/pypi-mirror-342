# -*- coding: utf-8 -*-

"""
Short.io API Client implementation.

This module provides the main Client class that serves as the primary interface
for interacting with the Short.io API in a Pythonic way. The Client class
combines multiple specialized mixins to provide comprehensive access to all
Short.io API endpoints while maintaining clean separation of concerns.
"""

import typing as T
import json
import dataclasses

import requests

from .type_hint import T_KWARGS
from .constants import DEFAULT_DEBUG

# mixin modules
from .domain import DomainMixin
from .link_queries import LinkQueriesMixin
from .link_management import LinkManagementMixin
from .sync_tsv import SyncTSVMixin


def normalize_endpoint(endpoint: str) -> str:
    """
    Normalize the endpoint URL by ensuring it ends with a slash.

    This utility function ensures consistent handling of API endpoint URLs
    by standardizing the format. It removes trailing slashes to ensure
    that when paths are appended to the endpoint, double slashes are avoided.

    Examples:

    >>> normalize_endpoint("https://api.short.io/")
    "https://api.short.io"
    >>> normalize_endpoint("https://api.short.io")
    "https://api.short.io"
    """
    if endpoint.endswith("/"):
        endpoint = endpoint[:-1]
    return endpoint


@dataclasses.dataclass
class Client(
    DomainMixin,
    LinkQueriesMixin,
    LinkManagementMixin,
    SyncTSVMixin,
):
    """
    Main client class for interacting with the Short.io API.

    This class combines multiple specialized mixins to provide a unified
    interface to all Short.io API endpoints. It handles authentication,
    request formatting, and response processing while delegating specific
    API endpoint implementations to the various mixins.

    The Client implements core HTTP request methods (http_get, http_post)
    which are then used by the mixin classes to implement specific API endpoints.
    This ensures consistent request handling and error management across all
    API calls.

    :param token: The Short.io API token for authentication
    :param endpoint: The base URL for the Short.io API (defaults to "https://api.short.io")
    """

    token: str = dataclasses.field()
    endpoint: str = dataclasses.field(default="https://api.short.io")

    def __post_init__(self):
        self.endpoint = normalize_endpoint(self.endpoint)

    @property
    def headers(self) -> dict[str, str]:
        """
        Get the default HTTP headers for API requests.
        """
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.token,
        }

    @property
    def delete_headers(self) -> dict[str, str]:
        """
        Get the default HTTP headers for delete API requests.
        """
        return {
            "accept": "application/json",
            "authorization": self.token,
        }

    def http_get(
        self,
        url: str,
        headers: T.Optional[T_KWARGS] = None,
        params: T.Optional[T_KWARGS] = None,
        debug: bool = DEFAULT_DEBUG,
    ):
        """
        Perform an HTTP GET request to the Short.io API.

        This method handles the details of making GET requests to the API,
        including adding appropriate headers, formatting parameters, and
        logging request/response details for debugging.
        """
        if debug:  # pragma: no cover
            print(f"===== Start of GET request.url = {url} =====")

        final_headers = self.headers
        if headers is not None:  # pragma: no cover
            final_headers.update(headers)
        if debug:  # pragma: no cover
            print(f"request.headers = {final_headers}")
            print(f"request.params = {params}")

        res = requests.get(
            url,
            headers=final_headers,
            params=params,
        )
        if debug:  # pragma: no cover
            print(f"response.status = {res.status_code}")
            print("response.data =")
            print(json.dumps(res.json(), indent=4, ensure_ascii=False))
            print(f"===== End of GET request.url = {url} =====")
        return res

    def http_post(
        self,
        url: str,
        headers: T.Optional[dict[str, T.Any]] = None,
        params: T.Optional[dict[str, T.Any]] = None,
        data: T.Optional[dict[str, T.Any]] = None,
        debug: bool = DEFAULT_DEBUG,
    ):
        """
        Perform an HTTP POST request to the Short.io API.
        """
        if debug:  # pragma: no cover
            print(f"===== Start of POST request.url = {url} =====")

        final_headers = self.headers
        if headers is not None:  # pragma: no cover
            final_headers.update(headers)
        if debug:  # pragma: no cover
            print(f"request.headers = {final_headers}")
            print(f"request.params = {params}")
            print(f"request.data = {data}")

        res = requests.post(
            url,
            headers=final_headers,
            params=params,
            json=data,
        )
        if debug:  # pragma: no cover
            print(f"response.status = {res.status_code}")
            print(f"response.headers = {res.headers}")
            print("response.data =")
            print(json.dumps(res.json(), indent=4, ensure_ascii=False))
            print(f"===== End of POST request.url = {url} =====")
        return res

    def http_delete(
        self,
        url: str,
        headers: T.Optional[dict[str, T.Any]] = None,
        params: T.Optional[dict[str, T.Any]] = None,
        data: T.Optional[dict[str, T.Any]] = None,
        debug: bool = DEFAULT_DEBUG,
    ):
        """
        Perform an HTTP DELETE request to the Short.io API.
        """
        if debug:  # pragma: no cover
            print(f"===== Start of DELETE request.url = {url} =====")

        final_headers = self.delete_headers
        if headers is not None:  # pragma: no cover
            final_headers.update(headers)
        if debug:  # pragma: no cover
            print(f"request.headers = {final_headers}")
            print(f"request.params = {params}")
            print(f"request.data = {data}")

        res = requests.delete(
            url,
            headers=final_headers,
            params=params,
            json=data,
        )
        if debug:  # pragma: no cover
            print(f"response.status = {res.status_code}")
            print(f"response.headers = {res.headers}")
            print("response.data =")
            print(json.dumps(res.json(), indent=4, ensure_ascii=False))
            print(f"===== End of DELETE request.url = {url} =====")
        return res
