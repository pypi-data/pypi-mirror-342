# -*- coding: utf-8 -*-

"""
Base model implementation for Short.io API objects.

This module provides the foundational data models for the Short.io API client library,
implementing common patterns for representing and interacting with Short.io resources.
The models follow three key design patterns:

1. **Raw Data Storage Pattern**:

All models store the original API response data in a `_data` attribute, treating the
API response schema as potentially unstable. Properties provide a stable interface
for accessing the underlying data, making the code more resilient to API changes.

2. **Property-Based Access Pattern**:

All attributes are exposed through properties rather than direct instance attributes.
This approach allows for lazy loading, data validation, and type conversion while
maintaining a clean public interface.

3. **Core Data Extraction Pattern**:

Each model implements a `core_data` property that returns a standardized, minimal
representation of the object. This provides a consistent way to access essential
information across different model types.

These models are designed to be instantiated by the API client methods, not directly
by users of the library. They provide a Pythonic interface to the JSON data returned
by the Short.io API.
"""

import typing as T
import json
import dataclasses
from datetime import datetime
from functools import cached_property

from .exc import ParamError
from .arg import REQ, _REQUIRED, rm_na, T_KWARGS

T_RESPONSE = T.Dict[str, T.Any]


@dataclasses.dataclass
class BaseModel:
    """
    Base class for all Short.io API object models.

    This abstract base class provides common functionality for data validation,
    parameter handling, and consistent interfaces across all Short.io resource models.
    It implements parameter validation for required fields and provides methods to
    distinguish between required and optional parameters.

    All Short.io API resource models (Domain, Link, Folder, etc.) inherit from this
    class, ensuring consistent behavior and interfaces throughout the library.

    The class works with the sentinel values (REQ, NA) defined in the arg module
    to manage required vs. optional fields in a dataclass-friendly way.
    """

    def _validate(self):
        """
        Validate that all required fields have values.
        """
        for field in dataclasses.fields(self.__class__):
            if field.init:
                k = field.name
                if getattr(self, k) is REQ:  # pragma: no cover
                    raise ParamError(f"Field {k!r} is required for {self.__class__}.")

    def __post_init__(self):
        self._validate()

    @classmethod
    def _split_req_opt(
        cls, kwargs: T_KWARGS
    ) -> T.Tuple[T_KWARGS, T_KWARGS]:  # pragma: no cover
        """
        Splits parameters into required and optional dictionaries.

        This is useful when constructing objects or API requests to ensure
        all required parameters are present before sending a request.
        """
        req_kwargs, opt_kwargs = dict(), dict()
        for field in dataclasses.fields(cls):
            if isinstance(field.default, _REQUIRED):
                try:
                    req_kwargs[field.name] = kwargs[field.name]
                except KeyError:
                    raise ParamError(
                        f"{field.name!r} is a required parameter for {cls}!"
                    )
            else:
                try:
                    opt_kwargs[field.name] = kwargs[field.name]
                except KeyError:
                    pass
        opt_kwargs = rm_na(**opt_kwargs)
        return req_kwargs, opt_kwargs

    @property
    def core_data(self) -> T_KWARGS:
        """
        Returns a dictionary containing the essential data of the model.

        This property must be implemented by all subclasses to provide
        a consistent minimal representation of the model's core data.
        """
        raise NotImplementedError


@dataclasses.dataclass
class Domain(BaseModel):
    """
    Domain model representing a Short.io domain configuration.

    This class provides a Pythonic interface to Short.io domain data while maintaining
    access to the raw API response through the `_data` attribute. All domain properties
    are accessed through getter methods that retrieve values from the underlying data.

    Following the Raw Data Storage Pattern, the Domain model doesn't define its own
    attributes beyond ``_data``, instead exposing all API data through property methods.

    Ref:

    - https://developers.short.io/reference/get_api-domains
    - https://developers.short.io/reference/get_domains-domainid
    - https://developers.short.io/reference/post_domains
    """

    _data: dict[str, T.Any] = dataclasses.field(default=REQ)

    @property
    def id(self) -> T.Optional[int]:  # pragma: no cover
        return self._data.get("id")

    @property
    def hostname(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("hostname")

    @property
    def unicode_hostname(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("unicodeHostname")

    @property
    def state(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("state")

    @property
    def created_at(self) -> T.Optional[datetime]:  # pragma: no cover
        created_at_str = self._data.get("createdAt")
        if created_at_str:
            try:
                return datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):  # pragma: no cover
                pass
        else:  # pragma: no cover
            return None

    @property
    def updated_at(self) -> T.Optional[datetime]:  # pragma: no cover
        updated_at_str = self._data.get("updatedAt")
        if updated_at_str:
            try:
                return datetime.fromisoformat(updated_at_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):  # pragma: no cover
                pass
        else:  # pragma: no cover
            return None

    @property
    def team_id(self) -> T.Optional[int]:  # pragma: no cover
        return self._data.get("TeamId")

    @property
    def has_favicon(self) -> T.Optional[bool]:  # pragma: no cover
        return self._data.get("hasFavicon")

    @property
    def segment_key(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("segmentKey")

    @property
    def hide_referer(self) -> T.Optional[bool]:  # pragma: no cover
        return self._data.get("hideReferer")

    @property
    def link_type(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("linkType")

    @property
    def cloaking(self) -> T.Optional[bool]:  # pragma: no cover
        return self._data.get("cloaking")

    @property
    def hide_visitor_ip(self) -> T.Optional[bool]:  # pragma: no cover
        return self._data.get("hideVisitorIp")

    @property
    def enable_ai(self) -> T.Optional[bool]:  # pragma: no cover
        return self._data.get("enableAI")

    @property
    def https_level(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("httpsLevel")

    @property
    def https_links(self) -> T.Optional[bool]:  # pragma: no cover
        return self._data.get("httpsLinks")

    @property
    def redirect_404(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("redirect404")

    @property
    def webhook_url(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("webhookURL")

    @property
    def integration_ga(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("integrationGA")

    @property
    def integration_fb(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("integrationFB")

    @property
    def integration_adroll(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("integrationAdroll")

    @property
    def integration_gtm(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("integrationGTM")

    @property
    def client_storage(self) -> T.Optional[dict]:  # pragma: no cover
        return self._data.get("clientStorage")

    @property
    def case_sensitive(self) -> T.Optional[bool]:  # pragma: no cover
        return self._data.get("caseSensitive")

    @property
    def increment_counter(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("incrementCounter")

    @property
    def robots(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("robots")

    @property
    def ssl_cert_expiration_date(self) -> T.Optional[datetime]:  # pragma: no cover
        expiration_date_str = self._data.get("sslCertExpirationDate")
        if expiration_date_str:
            try:
                return datetime.fromisoformat(
                    expiration_date_str.replace("Z", "+00:00")
                )
            except (ValueError, TypeError):  # pragma: no cover
                pass
        else:  # pragma: no cover
            return None

    @property
    def ssl_cert_installed_success(self) -> T.Optional[bool]:  # pragma: no cover
        return self._data.get("sslCertInstalledSuccess")

    @property
    def domain_registration_id(self) -> T.Optional[int]:  # pragma: no cover
        return self._data.get("domainRegistrationId")

    @property
    def user_id(self) -> T.Optional[int]:  # pragma: no cover
        return self._data.get("UserId")

    @property
    def export_enabled(self) -> T.Optional[bool]:  # pragma: no cover
        return self._data.get("exportEnabled")

    @property
    def ip_exclusions(self) -> T.Optional[list[str]]:  # pragma: no cover
        return self._data.get("ipExclusions")

    @property
    def user_plan(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("userPlan")

    @property
    def core_data(self) -> T_KWARGS:  # pragma: no cover
        return {
            "id": self.id,
            "hostname": self.hostname,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclasses.dataclass
class Link(BaseModel):
    """
    Link model representing a Short.io shortened URL.

    This class provides a comprehensive Pythonic interface to Short.io link data
    while preserving access to the raw API response. The Link model implements the
    Raw Data Storage Pattern, storing the original API response in the `_data` attribute
    and accessing it through property methods.

    All link properties are accessed through getter methods that retrieve values from
    the underlying data dictionary, providing resilience against API schema changes.
    This approach treats the Short.io API response as having an unstable schema,
    storing raw values as-is and using lazy-loaded properties to access the data
    instead of defining them as instance attributes.

    Property methods handle type conversion (e.g., converting string dates to datetime
    objects) and gracefully handle missing values by returning None for optional fields.

    .. note::

        All properties return None if the corresponding data is not present
        in the raw API response, providing safe access to optional fields.

    Ref:

    - https://developers.short.io/reference/get_api-links
    """

    _data: dict[str, T.Any] = dataclasses.field(default=REQ)

    @property
    def original_url(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("originalURL")

    @property
    def cloaking(self) -> T.Optional[bool]:  # pragma: no cover
        return self._data.get("cloaking")

    @property
    def password(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("password")

    @property
    def expires_at(self) -> T.Optional[int]:  # pragma: no cover
        return self._data.get("expiresAt")

    @property
    def expired_url(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("expiredURL")

    @property
    def title(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("title")

    @property
    def tags(self) -> T.Optional[list[str]]:  # pragma: no cover
        return self._data.get("tags")

    @property
    def utm_source(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("utmSource")

    @property
    def utm_medium(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("utmMedium")

    @property
    def utm_campaign(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("utmCampaign")

    @property
    def utm_term(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("utmTerm")

    @property
    def utm_content(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("utmContent")

    @property
    def ttl(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("ttl")

    @property
    def path(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("path")

    @property
    def android_url(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("androidURL")

    @property
    def iphone_url(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("iphoneURL")

    @property
    def created_at(self) -> T.Optional[datetime]:  # pragma: no cover
        created_at_val = self._data.get("createdAt")
        if created_at_val:
            try:
                # Check if it's a string format that needs conversion
                if isinstance(created_at_val, str):
                    return datetime.fromisoformat(created_at_val.replace("Z", "+00:00"))
                # If it's a timestamp
                elif isinstance(created_at_val, (int, float)):
                    return datetime.fromtimestamp(created_at_val)
            except (ValueError, TypeError):  # pragma: no cover
                pass
        return None

    @property
    def clicks_limit(self) -> T.Optional[int]:  # pragma: no cover
        return self._data.get("clicksLimit")

    @property
    def password_contact(self) -> T.Optional[bool]:  # pragma: no cover
        return self._data.get("passwordContact")

    @property
    def skip_qs(self) -> T.Optional[bool]:  # pragma: no cover
        return self._data.get("skipQS")

    @property
    def archived(self) -> T.Optional[bool]:  # pragma: no cover
        return self._data.get("archived")

    @property
    def split_url(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("splitURL")

    @property
    def split_percent(self) -> T.Optional[int]:  # pragma: no cover
        return self._data.get("splitPercent")

    @property
    def integration_adroll(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("integrationAdroll")

    @property
    def integration_fb(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("integrationFB")

    @property
    def integration_ga(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("integrationGA")

    @property
    def integration_gtm(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("integrationGTM")

    @property
    def id_string(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("idString")

    @property
    def id(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("id")

    @property
    def short_url(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("shortURL")

    @property
    def secure_short_url(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("secureShortURL")

    @property
    def redirect_type(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("redirectType")

    @property
    def folder_id(self) -> T.Optional[str]:  # pragma: no cover
        return self._data.get("FolderId")

    @property
    def domain_id(self) -> T.Optional[int]:  # pragma: no cover
        return self._data.get("DomainId")

    @property
    def owner_id(self) -> T.Optional[int]:  # pragma: no cover
        return self._data.get("OwnerId")

    @property
    def has_password(self) -> T.Optional[bool]:  # pragma: no cover
        return self._data.get("hasPassword")

    @property
    def user(self) -> T.Optional[dict]:  # pragma: no cover
        return self._data.get("User")

    @property
    def user_id(self) -> T.Optional[int]:  # pragma: no cover
        user = self.user
        if user:
            return user.get("id")
        return None

    @property
    def user_name(self) -> T.Optional[str]:  # pragma: no cover
        user = self.user
        if user:
            return user.get("name")
        return None

    @property
    def user_email(self) -> T.Optional[str]:  # pragma: no cover
        user = self.user
        if user:
            return user.get("email")
        return None

    @property
    def user_photo_url(self) -> T.Optional[str]:  # pragma: no cover
        user = self.user
        if user:
            return user.get("photoURL")
        return None

    @property
    def core_data(self) -> T_KWARGS:  # pragma: no cover
        """
        Get the essential link data in a simplified dictionary.
        """
        return {
            "id": self.id,
            "id_string": self.id_string,
            "original_url": self.original_url,
            "short_url": self.short_url,
            "created_at": self.created_at,
        }


@dataclasses.dataclass
class Folder(BaseModel):
    """
    Folder model representing a Short.io link organization folder.

    This class provides access to folder data from the Short.io API.
    Following the same pattern as other models, it stores the raw API
    response in the `_data` attribute and provides property methods
    for accessing specific attributes.
    """

    _data: dict[str, T.Any] = dataclasses.field(default=REQ)

    @property
    def domain_id(self) -> T.Optional[int]:  # pragma: no cover
        return self._data.get("DomainId")

    @property
    def id(self) -> str:  # pragma: no cover
        return self._data.get("id")

    @property
    def name(self) -> str:  # pragma: no cover
        return self._data.get("name")

    @property
    def core_data(self) -> T_KWARGS:  # pragma: no cover
        return {
            "domain_id": self.domain_id,
            "id": self.id,
            "name": self.name,
        }
