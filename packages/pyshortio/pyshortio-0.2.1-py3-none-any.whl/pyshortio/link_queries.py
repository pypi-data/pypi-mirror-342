# -*- coding: utf-8 -*-

"""
Short.io Link query API implementation.

This module provides classes and methods for interacting with the Short.io Link-related
API endpoints. It focuses on query operations that retrieve link information from the
Short.io service, implementing a comprehensive suite of methods for different query
patterns.

he implementation follows three key design patterns:

1. **Return Pattern**:

All methods representing Short.io API calls return a tuple of two objects:

- First: The raw `requests.Response` object, allowing users complete access to
 HTTP response details (headers, status codes, etc.)
- Second: A method-specific result in a Pythonic format (e.g., a list of Link objects)

Each method includes a `raise_for_status` parameter that controls whether
exceptions are raised immediately on HTTP errors, giving users fine-grained control
over error handling.

2. **Parameter Handling**:

Methods use the NA (Not Applicable) sentinel value for optional parameters,
which are filtered out before being sent to the API using the `rm_na` utility.

3. **Pagination Abstraction Pattern**:

Short.io API list methods use next page tokens for pagination. This module implements
a universal pagination mechanism that converts any regular API method to an
auto-paginating method. These methods are prefixed with `pagi_` followed by the
original method name and return an iterable of the original method's return values
(typically tuples of response and specialized objects).
"""

import typing as T
from datetime import datetime

from requests import Response

from .arg import NA, rm_na
from .constants import DEFAULT_RAISE_FOR_STATUS
from .model import Link, Folder
from .paginator import _paginate


if T.TYPE_CHECKING:  # pragma: no cover
    from .client import Client


class LinkQueriesMixin:
    """
    Mixin class providing Link-related query methods for the Client.

    This class implements various methods for retrieving link information from the
    Short.io API. It focuses exclusively on query operations (retrieving existing
    links) rather than modification operations, which are handled by the
    LinkManagementMixin class.

    All methods follow the Dual Return Pattern, returning both the raw HTTP
    response and a Pythonic representation of the API result.

    Methods prefixed with ``pagi_`` implement the Pagination Abstraction Pattern,
    automatically handling pagination for list operations.

    These methods interact with Link objects which are defined in the model module,
    providing a clean separation between data models and API operations.
    """

    def list_links(
        self: "Client",
        domain_id: int,
        limit: T.Optional[int] = NA,
        id_string: T.Optional[int] = NA,
        create_at: T.Optional[datetime] = NA,
        before_date: T.Optional[datetime] = NA,
        after_date: T.Optional[datetime] = NA,
        date_sort_order: T.Optional[str] = NA,
        page_token: T.Optional[str] = NA,
        folder_id: T.Optional[str] = NA,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, list[Link]]:
        """
        List links for a specific domain with optional filtering.

        This method retrieves links from the Short.io API with various filtering options.
        It follows the Dual Return Pattern, providing both raw HTTP access and
        Pythonic data models.

        Example:

        >>> # List all links for a domain with a limit of 2
        >>> response, link_list = client.list_links(
        ...     domain_id=45678,
        ...     limit=2,
        ... )
        >>> print(len(link_list))  # Output: 2
        >>>
        >>> # List all links for a domain
        >>> response, link_list = client.list_links(
        ...     domain_id=45678,
        ... )
        >>> print(len(link_list))  # Output: 3

        Ref:

        - https://developers.short.io/reference/get_api-domains
        """
        url = f"{self.endpoint}/api/links"
        params = {
            "domain_id": domain_id,
            "limit": limit,
            "idString": id_string,
            "createdAt": create_at,
            "beforeDate": before_date,
            "afterDate": after_date,
            "dateSortOrder": date_sort_order,
            "pageToken": page_token,
            "folderId": folder_id,
        }
        params = rm_na(**params)
        response = self.http_get(
            url=url,
            params=params,
        )
        if raise_for_status:
            response.raise_for_status()
        if response.status_code == 200:
            link_list = [Link(_data=dct) for dct in response.json().get("links", [])]
        else:
            raise NotImplementedError("Unexpected response code")
        return response, link_list

    def pagi_list_links(
        self: "Client",
        domain_id: int,
        limit: T.Optional[int] = NA,
        id_string: T.Optional[int] = NA,
        create_at: T.Optional[datetime] = NA,
        before_date: T.Optional[datetime] = NA,
        after_date: T.Optional[datetime] = NA,
        date_sort_order: T.Optional[str] = NA,
        folder_id: T.Optional[str] = NA,
        total_max_results: int = 9999,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> T.Iterable[tuple[Response, list[Link]]]:
        """
        Auto-paginated version of list_link method.

        This method implements the Pagination Abstraction Pattern, automatically
        handling pagination for listing links. It returns an iterable that yields
        each page of results, allowing for efficient processing of large result sets.

        >>> # Process all links across multiple pages
        >>> for response, links in client.pagi_list_links(domain_id=45678):
        >>>     for link in links:
        >>>         process_link(link)

        .. note::

            This method automatically handles fetching subsequent pages until
        """

        def get_next_token(res):
            return res.get("nextPageToken")

        def set_next_token(kwargs, next_token):
            kwargs["page_token"] = next_token

        yield from _paginate(
            method=self.list_links,
            list_key="links",
            get_next_token=get_next_token,
            set_next_token=set_next_token,
            kwargs=dict(
                domain_id=domain_id,
                limit=limit,
                id_string=id_string,
                create_at=create_at,
                before_date=before_date,
                after_date=after_date,
                date_sort_order=date_sort_order,
                folder_id=folder_id,
                raise_for_status=raise_for_status,
            ),
            max_results=total_max_results,
        )

    def get_link_opengraph_properties(
        self: "Client",
        domain_id: int,
        link_id: str,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, T.Optional[list]]:
        """
        Get OpenGraph properties for a specific link.

        Example:

        >>> # Get OpenGraph properties for a specific link
        >>> response, properties = client.get_link_opengraph_properties(
        ...     domain_id=45678,
        ...     link_id="lnk_abc123def456"
        ... )
        >>> # Properties typically include metadata like title, description, etc.
        >>> print(properties)  # Output: {'title': 'Example Page', ...}

        Ref:

        - https://developers.short.io/reference/get_links-opengraph-domainid-linkid
        """
        url = f"https://api.short.io/links/opengraph/{domain_id}/{link_id}"
        response = self.http_get(url=url)
        if raise_for_status:
            response.raise_for_status()
        if response.status_code == 200:
            result = response.json()
        else:  # pragma: no cover
            raise NotImplementedError("Unexpected response code")
        return response, result

    def get_link_info_by_link_id(
        self: "Client",
        link_id: str,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, Link]:
        """
        This method retrieves detailed information about a specific link using its ID.

        Example:

        >>> # Get information for an existing link
        >>> response, link = client.get_link_info_by_link_id(
        ...     link_id="lnk_abc123def456"
        ... )
        >>> print(link.id)  # Output: lnk_abc123def456
        >>>
        >>> # Try to get a non-existent link
        >>> response, link = client.get_link_info_by_link_id(
        ...     link_id="non_existent",
        ...     raise_for_status=False
        ... )
        >>> print(link)  # Output: None

        Ref:

        - https://developers.short.io/reference/get_links-linkid
        """
        url = f"{self.endpoint}/links/{link_id}"
        response = self.http_get(url=url)
        if raise_for_status:
            response.raise_for_status()
        if response.status_code == 200:
            link = Link(_data=response.json())
        elif response.status_code == 404:
            link = None
        else:  # pragma: no cover
            raise NotImplementedError("Unexpected response code")
        return response, link

    def get_link_info_by_path(
        self: "Client",
        hostname: str,
        path: str,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, Link]:
        """
        This method retrieves link information using the hostname and path
        components of the shortened URL.

        Example:

        >>> # Get link information by path
        >>> response, link = client.get_link_info_by_path(
        ...     hostname="example.short.gy",
        ...     path="abc123"
        ... )
        >>> print(link.id)  # Output: lnk_abc123def456
        >>> print(link.path)  # Output: abc123
        >>>
        >>> # Try to get a non-existent path
        >>> response, link = client.get_link_info_by_path(
        ...     hostname="example.short.gy",
        ...     path="non_existent",
        ...     raise_for_status=False
        ... )
        >>> print(link)  # Output: None

        Ref:

        - https://developers.short.io/reference/get_links-expand
        """
        url = f"{self.endpoint}/links/expand"
        params = {
            "domain": hostname,
            "path": path,
        }
        response = self.http_get(url=url, params=params)
        if raise_for_status:
            response.raise_for_status()
        if response.status_code == 200:
            link = Link(_data=response.json())
        elif response.status_code == 404:
            link = None
        else:  # pragma: no cover
            raise NotImplementedError("Unexpected response code")
        return response, link

    def list_links_by_original_url(
        self: "Client",
        hostname: str,
        original_url: str,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, list[Link]]:
        """
        This method finds all shortened links that point to the specified original URL.

        Example:

        >>> # Find all links pointing to a specific URL
        >>> response, link_list = client.list_links_by_original_url(
        ...     hostname="example.short.gy",
        ...     original_url="https://example.com/page"
        ... )
        >>> print(len(link_list))  # Output: 1
        >>> print(link_list[0].original_url)  # Output: https://example.com/page
        >>>
        >>> # Search for a URL with no links
        >>> response, link_list = client.list_links_by_original_url(
        ...     hostname="example.short.gy",
        ...     original_url="https://example.com/not-exists",
        ...     raise_for_status=False
        ... )
        >>> print(len(link_list))  # Output: 0

        Ref:

        - https://developers.short.io/reference/get_links-multiple-by-url
        """
        url = f"{self.endpoint}/links/multiple-by-url"
        params = {
            "domain": hostname,
            "originalURL": original_url,
        }
        response = self.http_get(url=url, params=params)
        if raise_for_status:
            response.raise_for_status()
        if response.status_code == 200:
            link_list = [Link(_data=dct) for dct in response.json().get("links", [])]
        elif response.status_code == 404:
            link_list = []
        else:  # pragma: no cover
            raise NotImplementedError("Unexpected response code")
        return response, link_list

    def list_folders(
        self: "Client",
        domain_id: int,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, list[Folder]]:
        """
        This method retrieves all folders used to organize links for a domain.

        Example:

        >>> # List all folders for a domain
        >>> response, folder_list = client.list_folders(
        ...     domain_id=45678
        ... )
        >>> # Print folder information
        >>> for folder in folder_list:
        ...     print(f"ID: {folder.id}, Name: {folder.name}")

        Ref:

        - https://developers.short.io/reference/get_links-folders-domainid
        """
        url = f"{self.endpoint}/links/folders/{domain_id}"
        response = self.http_get(url=url)
        if raise_for_status:
            response.raise_for_status()
        if response.status_code == 200:
            folder_list = [
                Folder(_data=dct) for dct in response.json().get("linkFolders", [])
            ]
        else:
            raise NotImplementedError("Unexpected response code")
        return response, folder_list

    def get_folder(
        self: "Client",
        domain_id: int,
        folder_id: str,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, T.Optional[Folder]]:
        """
        This method retrieves detailed information about a specific folder.

        Example:

        >>> # Get folder information
        >>> response, folder = client.get_folder(
        ...     domain_id=45678,
        ...     folder_id="fld_abc123def456"
        ... )
        >>> if folder:
        ...     print(f"Folder name: {folder.name}")
        >>>
        >>> # Try to get a non-existent folder
        >>> response, folder = client.get_folder(
        ...     domain_id=45678,
        ...     folder_id="non_existent",
        ...     raise_for_status=False
        ... )
        >>> print(folder)  # Output: None

        Ref:

        - https://developers.short.io/reference/get_links-folders-domainid-folderid
        """
        url = f"{self.endpoint}/links/folders/{domain_id}/{folder_id}"
        response = self.http_get(url=url)
        if raise_for_status:  # pragma: no cover
            response.raise_for_status()
        if response.status_code == 200:
            response_json = response.json()
            if response_json is None:
                folder = None
            else:
                folder = Folder(_data=response.json())
        elif response.status_code == 404:  # pragma: no cover
            folder = None
        else:  # pragma: no cover
            raise NotImplementedError("Unexpected response code")
        return response, folder

    def list_folders(
        self: "Client",
        domain_id: int,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, list[Folder]]:
        """
        This method retrieves all folders used to organize links for a domain.

        Example:

        >>> # List all folders for a domain
        >>> response, folder_list = client.list_folders(
        ...     domain_id=45678
        ... )
        >>> # Print folder information
        >>> for folder in folder_list:
        ...     print(f"ID: {folder.id}, Name: {folder.name}")

        Ref:

        - https://developers.short.io/reference/get_links-folders-domainid
        """
        url = f"{self.endpoint}/links/folders/{domain_id}"
        response = self.http_get(url=url)
        if raise_for_status:
            response.raise_for_status()
        if response.status_code == 200:
            folder_list = [
                Folder(_data=dct) for dct in response.json().get("linkFolders", [])
            ]
        else:
            raise NotImplementedError("Unexpected response code")
        return response, folder_list

    def create_folder(
        self: "Client",
        domain_id: int,
        name: str,
        color: str = NA,
        background_color: str = NA,
        logo_url: str = NA,
        logo_height: str = NA,
        logo_width: str = NA,
        ec_level: str = NA,
        integration_fb: str = NA,
        integration_ga: str = NA,
        integration_gtm: str = NA,
        integration_adroll: str = NA,
        utm_campaign: str = NA,
        utm_medium: str = NA,
        utm_source: str = NA,
        redirect_type: int = NA,
        expires_at_days: int = NA,
        icon: str = NA,
        prefix: str = NA,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, T.Optional[Folder]]:
        """
        Create a new folder for organizing links.

        Ref:

        - https://developers.short.io/reference/post_links-folders
        """
        url = f"{self.endpoint}/links/folders"
        data = {
            "domainId": domain_id,
            "name": name,
            "color": color,
            "backgroundColor": background_color,
            "logoUrl": logo_url,
            "logoHeight": logo_height,
            "logoWidth": logo_width,
            "ecLevel": ec_level,
            "integrationFB": integration_fb,
            "integrationGA": integration_ga,
            "integrationGTM": integration_gtm,
            "integrationAdroll": integration_adroll,
            "utmCampaign": utm_campaign,
            "utmMedium": utm_medium,
            "utmSource": utm_source,
            "redirectType": redirect_type,
            "expiresAtDays": expires_at_days,
            "icon": icon,
            "prefix": prefix,
        }
        data = rm_na(**data)
        response = self.http_post(url=url, data=data)
        if raise_for_status:  # pragma: no cover
            response.raise_for_status()
        if response.status_code in [200, 201]:
            folder = Folder(_data=response.json())
        else:  # pragma: no cover
            raise NotImplementedError("Unexpected response code")
        return response, folder
