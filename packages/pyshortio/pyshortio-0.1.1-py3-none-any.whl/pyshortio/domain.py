# -*- coding: utf-8 -*-

"""
Short.io Domain API implementation.

This module provides classes and methods for interacting with the Short.io Domain-related
API endpoints. It includes the Domain model class and API methods for retrieving domain
information.
"""

import typing as T

from requests import Response

from .arg import NA, rm_na
from .constants import DEFAULT_RAISE_FOR_STATUS
from .model import Domain

if T.TYPE_CHECKING:  # pragma: no cover
    from .client import Client


class DomainMixin:
    """
    Mixin class providing Domain-related API methods for the Client.
    """

    def list_domains(
        self: "Client",
        limit: T.Optional[int] = NA,
        offset: T.Optional[int] = NA,
        no_team_id: T.Optional[bool] = NA,
        pattern: T.Optional[str] = NA,
        team_id: T.Optional[str] = NA,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, list[Domain]]:
        """
        Retrieve a list of all domains with optional filtering.

        Ref:

        - https://developers.short.io/reference/get_api-domains
        """
        url = f"{self.endpoint}/api/domains"
        params = {
            "limit": limit,
            "offset": offset,
            "noTeamId": no_team_id,
            "pattern": pattern,
            "teamId": team_id,
        }
        params = rm_na(**params)
        response = self.http_get(
            url=url,
            params=params,
        )
        if raise_for_status:
            response.raise_for_status()
        domain_list = [Domain(_data=dct) for dct in response.json()]
        return response, domain_list

    def get_domain(
        self: "Client",
        domain_id: int,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> tuple[Response, T.Optional[Domain]]:
        """
        Retrieve a specific domain by its ID.

        Ref:

        - https://developers.short.io/reference/get_domains-domainid
        """
        url = f"{self.endpoint}/domains/{domain_id}"
        response = self.http_get(
            url=url,
        )
        if raise_for_status:
            response.raise_for_status()
        if response.status_code == 404:
            domain = None
        else:
            domain = Domain(_data=response.json())
        return response, domain

    def get_domain_by_hostname(
        self: "Client",
        hostname: str,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> T.Tuple[Response, T.Optional[Domain]]:
        """
        Find a domain by its hostname.

        This method lists all domains and finds the one matching the specified hostname.
        This is a convenience method that combines :meth:`list_domains` and filtering.
        """
        response, domain_list = self.list_domains(raise_for_status=raise_for_status)
        for domain in domain_list:
            if domain.hostname == hostname:
                return response, domain
        return response, None
