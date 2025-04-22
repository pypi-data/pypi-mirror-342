# -*- coding: utf-8 -*-

from .vendor.vislog import VisLog

logger = VisLog(
    name="pyshortio",
    log_format="%(message)s",
)
