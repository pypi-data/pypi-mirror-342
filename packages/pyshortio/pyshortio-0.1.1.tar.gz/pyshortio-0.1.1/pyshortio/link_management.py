# -*- coding: utf-8 -*-

"""
Short.io Link Management API implementation.

This module provides classes and methods for creating, updating, and deleting links
in the Short.io service. It complements the :mod:`pyshortio.link_queries` module
by focusing on modification operations rather than retrieval operations.
"""

try:
    import typing_extensions as T
except ImportError:  # pragma: no cover
    import typing as T

from datetime import datetime

from requests import Response

from .arg import NA, rm_na
from .constants import DEFAULT_RAISE_FOR_STATUS
from .utils import datetime_to_iso_string
from .model import Link


if T.TYPE_CHECKING:  # pragma: no cover
    from .client import Client


class T_CREATE_BATCH_LINK(T.TypedDict):
    """
    Type definition for batch link creation parameters.

    This TypedDict defines the expected structure for the links parameter in
    the batch_create_links method. It includes both required and optional fields
    that can be specified for each link in the batch.
    """

    original_url: T.Required[str]
    cloaking: T.NotRequired[bool]
    password: T.NotRequired[str]
    redirect_type: T.NotRequired[str]
    expire_at: T.NotRequired[datetime]
    expire_url: T.NotRequired[str]
    title: T.NotRequired[str]
    tags: T.NotRequired[list[str]]
    utm_source: T.NotRequired[str]
    utm_medium: T.NotRequired[str]
    utm_campaign: T.NotRequired[str]
    utm_term: T.NotRequired[str]
    utm_content: T.NotRequired[str]
    ttl: T.NotRequired[datetime]
    path: T.NotRequired[str]
    android_url: T.NotRequired[str]
    iphone_url: T.NotRequired[str]
    created_at: T.NotRequired[datetime]
    clicks_limit: T.NotRequired[int]
    password_contact: T.NotRequired[bool]
    skip_qs: T.NotRequired[bool]
    archived: T.NotRequired[bool]
    split_url: T.NotRequired[str]
    split_percent: T.NotRequired[int]
    integration_adroll: T.NotRequired[str]
    integration_fb: T.NotRequired[str]
    integration_ga: T.NotRequired[str]
    integration_gtm: T.NotRequired[str]
    allow_duplicates: T.NotRequired[bool]
    folder_id: T.NotRequired[str]


class T_CREATE_LINK(T_CREATE_BATCH_LINK):
    """
    Type definition for link creation parameters.

    Extends ``T_CREATE_BATCH_LINK`` by adding the required hostname parameter.
    This TypedDict is used to define the expected structure for create_link method
    parameters.
    """

    hostname: T.Required[str]


class LinkManagementMixin:
    """
    Mixin class providing Link management API methods for the Client.

    This class implements methods for creating, updating, and deleting links in the
    Short.io service. It focuses exclusively on modification operations, complementing
    the query operations in LinkQueriesMixin.
    """

    def create_link(
        self: "Client",
        hostname: str,
        original_url: str,
        cloaking: bool = NA,
        password: str = NA,
        redirect_type: str = NA,
        expire_at: datetime = NA,
        expire_url: str = NA,
        title: str = NA,
        tags: list[str] = NA,
        utm_source: str = NA,
        utm_medium: str = NA,
        utm_campaign: str = NA,
        utm_term: str = NA,
        utm_content: str = NA,
        ttl: datetime = NA,
        path: str = NA,
        android_url: str = NA,
        iphone_url: str = NA,
        created_at: datetime = NA,
        clicks_limit: int = NA,
        password_contact: bool = NA,
        skip_qs: bool = NA,
        archived: bool = NA,
        split_url: str = NA,
        split_percent: int = NA,
        integration_adroll: str = NA,
        integration_fb: str = NA,
        integration_ga: str = NA,
        integration_gtm: str = NA,
        allow_duplicates: bool = NA,
        folder_id: str = NA,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, T.Optional[Link]]:
        """
        Create a new shortened link.

        This method creates a new shortened link on the specified domain pointing
        to the provided original URL. It supports a wide range of optional parameters
        for customizing the link's behavior and appearance.

        Example:

        >>> # Create a simple link with just original URL
        >>> response, link = client.create_link(
        ...     hostname="example.short.gy",
        ...     original_url="https://example.com/page"
        ... )
        >>> print(link.original_url)  # Output: https://example.com/page
        >>>
        >>> # Create a link with custom title and other options
        >>> response, link = client.create_link(
        ...     hostname="example.short.gy",
        ...     original_url="https://example.com/features",
        ...     title="Example Features Page",
        ...     utm_source="newsletter",
        ...     utm_medium="email"
        ... )
        >>> print(link.title)  # Output: Example Features Page

        Ref:

        - https://developers.short.io/reference/post_links
        """
        url = f"{self.endpoint}/links"
        data = {
            "domain": hostname,
            "originalURL": original_url,
            "cloaking": cloaking,
            "password": password,
            "redirectType": redirect_type,
            "expiresAt": datetime_to_iso_string(expire_at),
            "expiredURL": expire_url,
            "title": title,
            "tags": tags,
            "utmSource": utm_source,
            "utmMedium": utm_medium,
            "utmCampaign": utm_campaign,
            "utmTerm": utm_term,
            "utmContent": utm_content,
            "ttl": datetime_to_iso_string(ttl),
            "path": path,
            "androidURL": android_url,
            "iphoneURL": iphone_url,
            "createdAt": datetime_to_iso_string(created_at),
            "clicksLimit": clicks_limit,
            "passwordContact": password_contact,
            "skipQS": skip_qs,
            "archived": archived,
            "splitURL": split_url,
            "splitPercent": split_percent,
            "integrationAdroll": integration_adroll,
            "integrationFB": integration_fb,
            "integrationGA": integration_ga,
            "integrationGTM": integration_gtm,
            "allowDuplicates": allow_duplicates,
            "folderId": folder_id,
        }
        data = rm_na(**data)
        response = self.http_post(
            url=url,
            data=data,
        )
        if raise_for_status:
            response.raise_for_status()
        if response.status_code == 200:
            link = Link(_data=response.json())
        else:  # pragma: no cover
            raise NotImplementedError("Unexpected response code")
        return response, link

    def batch_create_links(
        self: "Client",
        hostname: str,
        links: list[T_CREATE_BATCH_LINK],
        allow_duplicates: bool = NA,
        folder_id: str = NA,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, T.Optional[list[Link]]]:
        """
        This method allows creating multiple links at once, which is more efficient
        than making separate requests for each link. Each link in the batch can have
        its own set of parameters.

        Example:

        >>> # Create multiple links in a batch
        >>> response, links = client.batch_create_links(
        ...     hostname="example.short.gy",
        ...     links=[
        ...         {
        ...             "title": "Example Features",
        ...             "original_url": "https://example.com/features",
        ...         },
        ...         {
        ...             "title": "Example Integrations",
        ...             "original_url": "https://example.com/integrations",
        ...         }
        ...     ]
        ... )
        >>>
        >>> # Access the created links
        >>> features_link = links[0]
        >>> integrations_link = links[1]
        >>>
        >>> print(features_link.title)  # Output: Example Features
        >>> print(features_link.original_url)  # Output: https://example.com/features
        >>>
        >>> print(integrations_link.title)  # Output: Example Integrations
        >>> print(integrations_link.original_url)  # Output: https://example.com/integrations

        Ref:

        - https://developers.short.io/reference/post_links-bulk
        """
        links = [
            rm_na(
                **{
                    "originalURL": dct["original_url"],
                    "cloaking": dct.get("cloaking", NA),
                    "password": dct.get("password", NA),
                    "redirectType": dct.get("redirect_type", NA),
                    "expiresAt": datetime_to_iso_string(dct.get("expires_at", NA)),
                    "expiredURL": dct.get("expired_url", NA),
                    "title": dct.get("title", NA),
                    "tags": dct.get("tags", NA),
                    "utmSource": dct.get("utm_source", NA),
                    "utmMedium": dct.get("utm_medium", NA),
                    "utmCampaign": dct.get("utm_campaign", NA),
                    "utmTerm": dct.get("utm_term", NA),
                    "utmContent": dct.get("utm_content", NA),
                    "ttl": datetime_to_iso_string(dct.get("ttl", NA)),
                    "path": dct.get("path", NA),
                    "androidURL": dct.get("android_url", NA),
                    "iphoneURL": dct.get("iphone_url", NA),
                    "createdAt": datetime_to_iso_string(dct.get("created_at", NA)),
                    "clicksLimit": dct.get("clicks_limit", NA),
                    "passwordContact": dct.get("password_contact", NA),
                    "skipQS": dct.get("skip_qs", NA),
                    "archived": dct.get("archived", NA),
                    "splitURL": dct.get("split_url", NA),
                    "splitPercent": dct.get("split_percent", NA),
                    "integrationAdroll": dct.get("integration_adroll", NA),
                    "integrationFB": dct.get("integration_fb", NA),
                    "integrationGA": dct.get("integration_ga", NA),
                    "integrationGTM": dct.get("integration_gtm", NA),
                    "allowDuplicates": dct.get("allow_duplicates", NA),
                }
            )
            for dct in links
        ]
        data = {
            "domain": hostname,
            "links": links,
            "allowDuplicates": allow_duplicates,
            "folderId": folder_id,
        }
        data = rm_na(**data)
        url = f"{self.endpoint}/links/bulk"
        response = self.http_post(
            url=url,
            data=data,
        )
        if raise_for_status:
            response.raise_for_status()
        if response.status_code == 200:
            link_list = [Link(_data=dct) for dct in response.json()]
        else:  # pragma: no cover
            raise NotImplementedError("Unexpected response code")
        return response, link_list

    def update_link(
        self: "Client",
        link_id: str,
        domain_id: int = NA,
        original_url: str = NA,
        cloaking: bool = NA,
        password: str = NA,
        redirect_type: str = NA,
        expire_at: datetime = NA,
        expire_url: str = NA,
        title: str = NA,
        tags: list[str] = NA,
        utm_source: str = NA,
        utm_medium: str = NA,
        utm_campaign: str = NA,
        utm_term: str = NA,
        utm_content: str = NA,
        ttl: datetime = NA,
        path: str = NA,
        android_url: str = NA,
        iphone_url: str = NA,
        created_at: datetime = NA,
        clicks_limit: int = NA,
        password_contact: bool = NA,
        skip_qs: bool = NA,
        archived: bool = NA,
        split_url: str = NA,
        split_percent: int = NA,
        integration_adroll: str = NA,
        integration_fb: str = NA,
        integration_ga: str = NA,
        integration_gtm: str = NA,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, T.Optional[Link]]:
        """
        This method updates the properties of an existing link identified by its ID.
        Any parameter not explicitly provided (set to NA) will be left unchanged.

        Example:

        >>> # Update title and original URL of an existing link
        >>> response, link = client.update_link(
        ...     link_id="lnk_abc123def456",
        ...     title="Updated Title",
        ...     original_url="https://example.com/updated"
        ... )
        >>> print(link.title)  # Output: Updated Title
        >>> print(link.original_url)  # Output: https://example.com/updated
        >>>
        >>> # Verify the update by retrieving the link
        >>> response, link = client.get_link_info_by_link_id(
        ...     link_id="lnk_abc123def456"
        ... )
        >>> print(link.title)  # Output: Updated Title
        >>> print(link.original_url)  # Output: https://example.com/updated
        >>>
        >>> # Try to update a non-existent link
        >>> response, link = client.update_link(
        ...     link_id="non_existent",
        ...     raise_for_status=False
        ... )
        >>> print(link)  # Output: None

        Ref:

        - https://developers.short.io/reference/post_links-linkid
        """
        url = f"{self.endpoint}/links/{link_id}"
        params = {
            "domain_id": domain_id,
        }
        params = rm_na(**params)
        data = {
            "originalURL": original_url,
            "cloaking": cloaking,
            "password": password,
            "redirectType": redirect_type,
            "expiresAt": datetime_to_iso_string(expire_at),
            "expiredURL": expire_url,
            "title": title,
            "tags": tags,
            "utmSource": utm_source,
            "utmMedium": utm_medium,
            "utmCampaign": utm_campaign,
            "utmTerm": utm_term,
            "utmContent": utm_content,
            "ttl": datetime_to_iso_string(ttl),
            "path": path,
            "androidURL": android_url,
            "iphoneURL": iphone_url,
            "createdAt": datetime_to_iso_string(created_at),
            "clicksLimit": clicks_limit,
            "passwordContact": password_contact,
            "skipQS": skip_qs,
            "archived": archived,
            "splitURL": split_url,
            "splitPercent": split_percent,
            "integrationAdroll": integration_adroll,
            "integrationFB": integration_fb,
            "integrationGA": integration_ga,
            "integrationGTM": integration_gtm,
        }
        data = rm_na(**data)
        response = self.http_post(
            url=url,
            params=params,
            data=data,
        )
        if raise_for_status:
            response.raise_for_status()
        if response.status_code == 200:
            link = Link(_data=response.json())
        elif response.status_code == 400:
            link = None
        elif response.status_code == 404:
            link = None
        else:
            raise NotImplementedError("Unexpected response code")
        return response, link

    def delete_link(
        self: "Client",
        link_id: str,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, T.Optional[bool]]:
        """
        This method permanently deletes a link identified by its ID.

        Example:

        >>> # Delete an existing link
        >>> response, success = client.delete_link(
        ...     link_id="lnk_abc123def456"
        ... )
        >>> print(success)  # Output: True
        >>>
        >>> # Try to delete a non-existent link
        >>> response, success = client.delete_link(
        ...     link_id="non_existent",
        ...     raise_for_status=False
        ... )
        >>> print(success)  # Output: False
        >>>
        >>> # Verify the link was deleted
        >>> response, link_list = client.list_links(
        ...     domain_id=45678
        ... )
        >>> # Count of links should be reduced

        Ref:

        - https://developers.short.io/reference/delete_links-link-id
        """
        url = f"{self.endpoint}/links/{link_id}"
        response = self.http_delete(
            url=url,
        )
        if raise_for_status:
            response.raise_for_status()
        if response.status_code == 200:
            success = response.json()["success"]
        elif response.status_code == 404:
            success = False
        else:  # pragma: no cover
            raise NotImplementedError("Unexpected response code")
        return response, success

    def batch_delete_links(
        self: "Client",
        link_ids: list[str],
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, T.Optional[bool]]:
        """
        This method allows deleting multiple links at once, which is more efficient
        than making separate requests for each link.

        Example:

        >>> # Delete multiple links in a batch
        >>> link_ids = ["lnk_abc123def456", "lnk_ghi789jkl012"]
        >>> response, success = client.batch_delete_links(
        ...     link_ids=link_ids
        ... )
        >>> print(success)  # Output: True
        >>>
        >>> # Verify links were deleted
        >>> for link_id in link_ids:
        ...     response, link = client.get_link_info_by_link_id(
        ...         link_id=link_id,
        ...         raise_for_status=False
        ...     )
        ...     print(f"Link {link_id} exists: {link is not None}")
        ... # Output:
        ... # Link lnk_abc123def456 exists: False
        ... # Link lnk_ghi789jkl012 exists: False

        Ref:

        - https://developers.short.io/reference/delete_links-delete-bulk
        """
        url = f"{self.endpoint}/links/delete_bulk"
        data = {
            "link_ids": link_ids,
        }
        data = rm_na(**data)
        response = self.http_delete(
            url=url,
            data=data,
        )
        if raise_for_status:
            response.raise_for_status()
        if response.status_code == 200:
            success = response.json()["success"]
        else:
            success = None
        return response, success
