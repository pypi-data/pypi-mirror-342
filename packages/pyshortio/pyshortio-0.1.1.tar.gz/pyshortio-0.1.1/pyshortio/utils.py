# -*- coding: utf-8 -*-

import typing as T
from datetime import datetime

from .arg import _NOTHING


def datetime_to_iso_string(
    dt: T.Union[_NOTHING, datetime],
) -> T.Union[_NOTHING, str]:
    if isinstance(dt, datetime):
        return dt.isoformat()
    else:
        return dt
