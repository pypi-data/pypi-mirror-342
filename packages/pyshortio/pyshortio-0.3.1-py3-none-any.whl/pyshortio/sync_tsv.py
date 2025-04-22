# -*- coding: utf-8 -*-

"""
Short.io TSV Synchronization Tool

This module provides functionality to synchronize URL shortening data between
a TSV (Tab-Separated Values) file and the Short.io service. It enables bulk management
of shortened URLs through a single configuration file, automating the creation,
updating, and deletion of links to maintain consistency between local definitions
and the Short.io service.
"""

try:
    import typing_extensions as T
except ImportError:  # pragma: no cover
    import typing as T

import io
from datetime import datetime

try:
    import polars as pl
except ImportError:  # pragma: no cover
    pass

from .arg import NA, T_KWARGS
from .constants import DEFAULT_RAISE_FOR_STATUS
from .utils import chunked, group_by
from .model import Link, Folder
from .logger import logger

if T.TYPE_CHECKING:  # pragma: no cover
    from .client import Client


class T_LINK_DATA(T.TypedDict):
    """
    his TypedDict defines the expected structure for link data extracted from
    TSV files, mapping column names to their appropriate types. It includes both
    required fields (original_url) and various optional fields that correspond to
    Short.io link properties.
    """

    original_url: T.Required[str]
    cloaking: T.NotRequired[T.Optional[bool]]
    password: T.NotRequired[T.Optional[str]]
    redirect_type: T.NotRequired[T.Optional[str]]
    expire_at: T.NotRequired[T.Optional[datetime]]
    expire_url: T.NotRequired[T.Optional[str]]
    title: T.NotRequired[T.Optional[str]]
    tags: T.NotRequired[T.Optional[list[str]]]
    utm_source: T.NotRequired[T.Optional[str]]
    utm_medium: T.NotRequired[T.Optional[str]]
    utm_campaign: T.NotRequired[T.Optional[str]]
    utm_term: T.NotRequired[T.Optional[str]]
    utm_content: T.NotRequired[T.Optional[str]]
    ttl: T.NotRequired[T.Optional[datetime]]
    path: T.NotRequired[T.Optional[str]]
    android_url: T.NotRequired[T.Optional[str]]
    iphone_url: T.NotRequired[T.Optional[str]]
    clicks_limit: T.NotRequired[T.Optional[int]]
    password_contact: T.NotRequired[T.Optional[bool]]
    skip_qs: T.NotRequired[T.Optional[bool]]
    archived: T.NotRequired[T.Optional[bool]]
    split_url: T.NotRequired[T.Optional[str]]
    split_percent: T.NotRequired[T.Optional[int]]
    integration_adroll: T.NotRequired[T.Optional[str]]
    integration_fb: T.NotRequired[T.Optional[str]]
    integration_ga: T.NotRequired[T.Optional[str]]
    integration_gtm: T.NotRequired[T.Optional[str]]
    folder_id: T.NotRequired[T.Optional[str]]


def get_fingerprint_data_from_link(link: Link) -> T_KWARGS:
    """
    Extract relevant data from a Link object for fingerprinting purposes.

    This function extracts a standardized subset of link properties from a Link
    object to create a consistent representation for comparison. It removes None
    values and sorts tags to ensure consistent comparison regardless of order.
    """
    data = {
        "original_url": link.original_url,
        "cloaking": link.cloaking,
        "password": link.password,
        "redirect_type": link.redirect_type,
        "expires_at": link.expires_at,
        "expired_url": link.expired_url,
        "title": link.title,
        "tags": link.tags,
        "utm_source": link.utm_source,
        "utm_medium": link.utm_medium,
        "utm_campaign": link.utm_campaign,
        "utm_term": link.utm_term,
        "utm_content": link.utm_content,
        "ttl": link.ttl,
        "path": link.path,
        "android_url": link.android_url,
        "iphone_url": link.iphone_url,
        "clicks_limit": link.clicks_limit,
        "password_contact": link.password_contact,
        "skip_qs": link.skip_qs,
        "archived": link.archived,
        "split_url": link.split_url,
        "split_percent": link.split_percent,
        "integration_adroll": link.integration_adroll,
        "integration_fb": link.integration_fb,
        "integration_ga": link.integration_ga,
        "integration_gtm": link.integration_gtm,
        "folder_id": link.folder_id,
    }
    data = {k: v for k, v in data.items() if v is not None}
    if "tags" in data:
        data["tags"].sort()
    return data


def is_same(
    link_data: T_LINK_DATA,
    link: Link,
) -> bool:
    """
    Compare a link data dictionary with a Link object to determine if they are equivalent.

    This function checks if the properties in the link_data dictionary match the
    corresponding properties in the Link object. It handles comparing only the
    properties that are present in both, ignoring properties that are only in the
    Link object but not in link_data.

    :param link_data: Dictionary containing link properties from TSV
    :param link: Link object retrieved from Short.io

    :returns: True if all matching properties are the same, False otherwise

    .. note::

        The comparison is one-directional: it checks if properties in link_data
        match those in the Link object, but doesn't require all properties in the
        Link object to be in link_data.
    """
    # print("--- start is_same(...) ---") # pragma: no cover
    link_fingerprint_data = get_fingerprint_data_from_link(link)
    # print(f"{link_data = }") # pragma: no cover
    # print(f"{link_fingerprint_data = }")  # pragma: no cover
    for k, v in link_fingerprint_data.items():
        if k in link_data:
            if link_data[k] != v:
                return False
    return True


class SyncTSVMixin:
    """
    Mixin class providing TSV synchronization capabilities for the Client.
    """

    @logger.emoji_block(
        msg="Read link data from TSV file",
        emoji="📄",
    )
    def _sync_read_link_data_from_tsv(
        self: "Client",
        file: io.StringIO,
    ) -> tuple[
        dict[str, T_LINK_DATA],
        list[str],
    ]:
        """
        Read and parse link data from a TSV file.

        This method reads a TSV file using the polars library, validates the required
        ``original_url`` column, processes tag values, and extracts folder names.
        """
        logger.info("Read data ...")
        df = pl.read_csv(file, separator="\t")

        logger.info("Check original_url column ...")
        if "original_url" not in df.columns:
            raise ValueError("original_url column not found")
        df = df.drop_nulls("original_url")
        if df["original_url"].unique().count() != df.shape[0]:
            raise ValueError("original_url column must be unique")

        logger.info("Process tags column ...")
        df = df.with_columns(
            tags=pl.col("tags")
            .str.split(",")
            .list.eval(pl.element().str.strip_chars())
            .list.sort()
        )
        logger.info(f"Got {df.shape[0]} rows")
        mapping: dict[str, T_LINK_DATA] = dict()
        for row in df.to_dicts():
            row = {k: v for k, v in row.items() if v is not None}
            original_url = row["original_url"]
            mapping[original_url] = row

        folder_name_list = df["folder_name"].drop_nulls().unique().to_list()
        logger.info(f"Got {len(folder_name_list)} unique folder names")
        return mapping, folder_name_list

    def _read_folders_from_short_io(
        self: "Client",
        domain_id: int,
    ) -> dict[str, Folder]:
        """
        Retrieve all folders from Short.io for a specific domain.
        """
        _, folder_list = self.list_folders(domain_id=domain_id)
        return {folder.name: folder for folder in folder_list}

    def _read_links_from_short_io(
        self: "Client",
        domain_id: int,
    ) -> dict[str, Link]:
        """
        Retrieve all links from Short.io for a specific domain.

        This method uses pagination to efficiently retrieve all links from the domain,
        regardless of how many there are, and organizes them by original URL for
        easy lookup during the synchronization process.
        """
        paginator = self.pagi_list_links(
            domain_id=domain_id,
            limit=150,
            total_max_results=9999,
        )
        mapping: dict[str, Link] = dict()
        for _, link_list in paginator:
            for link in link_list:
                mapping[link.original_url] = link
        return mapping

    @logger.emoji_block(
        msg="Create folder if they do not exists",
        emoji="📂",
    )
    def _create_folder_if_they_do_not_exists(
        self: "Client",
        domain_id: int,
        folder_name_list: list[str],
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> dict[str, str]:
        """
        Create folders in Short.io if they don't already exist.

        This method compares the list of folder names from the TSV file with the
        existing folders in Short.io. It creates any folders that don't exist yet
        and builds a mapping of folder names to their IDs for use in link creation.
        """
        logger.info("Read existing folder info from short.io ...")
        existing_folders = self._read_folders_from_short_io(domain_id=domain_id)
        logger.info(f"Got {len(existing_folders)} existing folders")
        folder_name_to_id_mapping = dict()
        for folder_name in folder_name_list:
            if folder_name not in existing_folders:
                logger.info(f"{folder_name!r} folder not exists, create it ...")
                _, folder = self.create_folder(
                    domain_id=domain_id,
                    name=folder_name,
                    raise_for_status=raise_for_status,
                )
                logger.info(f"succeeded! folder_id = {folder.id}")
                folder_name_to_id_mapping[folder_name] = folder.id
            else:
                logger.info(f"{folder_name!r} folder already exists")
                folder_id = existing_folders[folder_name].id
                folder_name_to_id_mapping[folder_name] = folder_id
        return folder_name_to_id_mapping

    @logger.emoji_block(
        msg="Identify link to create, update and delete",
        emoji="🔍",
    )
    def _sync_identify_link_to_create_update_and_delete(
        self: "Client",
        domain_id: int,
        wanted_links: dict[str, T_LINK_DATA],
        folder_name_to_id_mapping: dict[str, str],
    ) -> tuple[
        list[T_LINK_DATA],
        list[tuple[str, T_LINK_DATA]],
        list[str],
    ]:
        """
        Identify which links need to be created, updated, or deleted.

        This method compares the links defined in the TSV file with those that already
        exist in Short.io to determine which operations are needed to synchronize them.
        It converts folder names to folder IDs, checks if existing links need updates,
        and identifies links that should be deleted if they're not in the TSV file.

        .. note::

            This method logs detailed information about each link's synchronization
            status (create/update/delete) for debugging and auditing purposes.
        """
        logger.info("Read existing link info from short.io ...")
        existing_links = self._read_links_from_short_io(domain_id=domain_id)
        logger.info(f"Got {len(existing_links)} existing links")

        to_create: list[T_LINK_DATA] = list()
        to_update: list[tuple[str, T_LINK_DATA]] = list()
        for original_url, link_data in wanted_links.items():
            if "folder_name" in link_data:
                folder_name = link_data.pop("folder_name")
                link_data["folder_id"] = folder_name_to_id_mapping[folder_name]
            if original_url in existing_links:
                link = existing_links.pop(original_url)
                is_same_flag = is_same(link_data=link_data, link=link)
                # logger.info(f"{link_data = }") # for debug only
                # logger.info(f"{get_fingerprint_data_from_link(link) = }") # for debug only
                # logger.info(f"{is_same_flag = }") # for debug only
                if is_same_flag is False:
                    to_update.append((link.id, link_data))
            else:
                to_create.append(link_data)
        to_delete: list[str] = [link.id for link in existing_links.values()]
        logger.info(f"🟢 got {len(to_create)} links to create")
        logger.info(f"🟡 got {len(to_update)} links to update")
        logger.info(f"🔴 got {len(to_delete)} links to delete")

        for link_data in to_create:
            logger.info(f"To create: {link_data = }")
        for link_id, link_data in to_update:
            logger.info(f"To update: {link_id = }, {link_data = }")
        for link_id in to_delete:
            logger.info(f"To delete: {link_id = }")
        return to_create, to_update, to_delete

    @logger.emoji_block(
        msg="Create links",
        emoji="🟢",
    )
    def _sync_create_links(
        self: "Client",
        hostname: str,
        to_create: list[T_LINK_DATA],
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
        real_run: bool = True,
    ):
        """
        Create new links in Short.io.

        This method creates new links based on the list identified by
        :meth:`_sync_identify_link_to_create_update_and_delete`. It groups links by folder
        to optimize the creation process and uses batch operations for efficiency.
        """
        for folder_id, link_data_list in group_by(
            to_create,
            get_key=lambda link_data: link_data.get("folder_id", "__no_folder_"),
        ).items():
            if folder_id == "__no_folder_":
                folder_id = NA
            for link_data_sub_list in chunked(link_data_list, 150):
                for link in link_data_sub_list:
                    logger.info(
                        f"create link for original_url = {link['original_url']}"
                    )
                if real_run:
                    _, link_list = self.batch_create_links(
                        hostname=hostname,
                        links=link_data_sub_list,
                        folder_id=folder_id,
                        raise_for_status=raise_for_status,
                    )

    @logger.emoji_block(
        msg="Update links",
        emoji="🟡",
    )
    def _sync_update_links(
        self: "Client",
        domain_id: int,
        to_update: list[tuple[str, T_LINK_DATA]],
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
        real_run: bool = True,
    ):
        """
        Update existing links in Short.io.

        This method updates links based on the list identified by
        :meth:`_sync_identify_link_to_create_update_and_delete`. It removes the folder_id
        from the update data since folders can't be changed via the update API.
        """
        for link_id, link_data in to_update:
            if "folder_id" in link_data:
                link_data.pop("folder_id")
            logger.info(
                f"update link {link_id}, original_url = {link_data['original_url']}"
            )
            if real_run:
                self.update_link(
                    link_id=link_id,
                    domain_id=domain_id,
                    **link_data,
                    raise_for_status=raise_for_status,
                )

    @logger.emoji_block(
        msg="Delete links",
        emoji="🔴",
    )
    def _sync_delete_links(
        self: "Client",
        to_delete: list[str],
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
        real_run: bool = True,
    ):
        """
        Delete links from Short.io.

        This method deletes links based on the list identified by
        :meth:`_sync_identify_link_to_create_update_and_delete`. It uses batch operations
        for efficiency, processing links in chunks.
        """
        for link_id_list in chunked(to_delete, 150):
            for link_id in link_id_list:
                logger.info(f"delete link {link_id}")
            if real_run:
                self.batch_delete_links(
                    link_ids=link_id_list,
                    raise_for_status=raise_for_status,
                )

    @logger.emoji_block(
        msg="Sync links from TSV file to short.io",
        emoji="🔄",
    )
    def sync_tsv(
        self: "Client",
        hostname: str,
        file: T.TextIO,
        update_if_not_the_same: bool = True,
        delete_if_not_in_file: bool = False,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
        real_run: bool = True,
    ):
        """
        Synchronize links from a TSV file to Short.io.

        This is the main public method of the :class:`SyncTSVMixin` class, orchestrating the
        entire synchronization process. It reads the TSV file, creates folders if needed,
        identifies necessary operations, and executes them according to the specified
        options.

        :param hostname: The hostname of the Short.io domain (e.g., "example.short.gy")
        :param file: An open file-like object containing TSV data
        :param update_if_not_the_same: Whether to update links that have
            changed. Defaults to True.
        :param delete_if_not_in_file: Whether to delete links that aren't
            in the TSV file. Defaults to False.
        :param raise_for_status: Whether to raise exceptions for HTTP errors.
            Defaults to DEFAULT_RAISE_FOR_STATUS.
        :param real_run: Whether to actually perform the API calls or
            just simulate them for a dry run. Defaults to True.

        .. note::

            - Setting ``delete_if_not_in_file=True`` can be destructive, as it will delete
              any links not defined in the TSV file. Use with caution.
            - Setting ``real_run=False`` performs a dry run, logging what would happen
              without making actual API calls. This is useful for testing.
            - The method logs detailed information about all operations for auditing
              and debugging purposes
        """
        logger.info(f"{hostname = }")
        logger.info(f"{update_if_not_the_same = }")
        logger.info(f"{delete_if_not_in_file = }")
        with logger.nested():
            wanted_links, folder_name_list = self._sync_read_link_data_from_tsv(
                file=file
            )

            _, domain = self.get_domain_by_hostname(hostname=hostname)

            folder_name_to_id_mapping = self._create_folder_if_they_do_not_exists(
                domain_id=domain.id,
                folder_name_list=folder_name_list,
                raise_for_status=raise_for_status,
            )

            to_create, to_update, to_delete = (
                self._sync_identify_link_to_create_update_and_delete(
                    domain_id=domain.id,
                    wanted_links=wanted_links,
                    folder_name_to_id_mapping=folder_name_to_id_mapping,
                )
            )

            if len(to_create):
                self._sync_create_links(
                    hostname=hostname,
                    to_create=to_create,
                    raise_for_status=raise_for_status,
                    real_run=real_run,
                )

            if update_if_not_the_same:
                if len(to_update):
                    self._sync_update_links(
                        domain_id=domain.id,
                        to_update=to_update,
                        raise_for_status=raise_for_status,
                        real_run=real_run,
                    )

            if delete_if_not_in_file:
                if len(to_delete):
                    self._sync_delete_links(
                        to_delete=to_delete,
                        raise_for_status=raise_for_status,
                        real_run=real_run,
                    )
