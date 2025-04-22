# -*- coding: utf-8 -*-

"""
Short.io Export functionality for exporting links to TSV format.

This module provides capabilities to export URL shortening data from Short.io
to a TSV (Tab-Separated Values) format, enabling users to analyze their links,
perform bulk operations, or keep local backups of their Short.io configuration.
"""

import io

try:
    import typing_extensions as T
except ImportError:  # pragma: no cover
    import typing as T

try:
    import polars as pl
except ImportError:  # pragma: no cover
    pass

from .constants import DEFAULT_RAISE_FOR_STATUS

if T.TYPE_CHECKING:  # pragma: no cover
    from .client import Client


class ExportMixin:
    """
    Mixin class providing export capabilities for the Client.
    """

    def export_to_tsv(
        self: "Client",
        hostname: str,
        raise_for_status: bool = DEFAULT_RAISE_FOR_STATUS,
    ) -> str:
        _, domain = self.get_domain_by_hostname(hostname=hostname)
        _, folder_list = self.list_folders(domain_id=domain.id)
        folder_id_to_name_mapping = {folder.id: folder.name for folder in folder_list}

        rows = []
        paginator = self.pagi_list_links(
            domain_id=domain.id,
            limit=150,
            total_max_results=9999,
            raise_for_status=raise_for_status,
        )
        for _, link_list in paginator:
            for link in link_list:
                row = {
                    "id": link.id,
                    "short_url": link.short_url,
                    "original_url": link.original_url,
                    "title": link.title,
                    "path": link.path,
                    "tags": ", ".join(link.tags) if link.tags else None,
                    "folder_name": (
                        folder_id_to_name_mapping[link.folder_id]
                        if link.folder_id
                        else None
                    ),
                    "allow_duplicates": False,
                    "clicks_limit": link.clicks_limit,
                    "cloaking": link.cloaking,
                    "password": link.password,
                    "password_contact": link.password_contact,
                    "redirect_type": link.redirect_type,
                    "ttl": link.ttl,
                    "expire_at": link.expires_at,
                    "expire_url": link.expired_url,
                    "utm_source": link.utm_source,
                    "utm_medium": link.utm_medium,
                    "utm_campaign": link.utm_campaign,
                    "utm_term": link.utm_term,
                    "utm_content": link.utm_content,
                    "android_url": link.android_url,
                    "iphone_url": link.iphone_url,
                    "skip_qs": link.skip_qs,
                    "archived": link.archived,
                    "split_url": link.split_url,
                    "split_percent": link.split_percent,
                    "integration_adroll": link.integration_adroll,
                    "integration_fb": link.integration_fb,
                    "integration_ga": link.integration_ga,
                    "integration_gtm": link.integration_gtm,
                }
                rows.append(row)
        df = pl.DataFrame(rows)
        buffer = io.StringIO()
        df.write_csv(buffer, separator="\t")
        return buffer.getvalue()
