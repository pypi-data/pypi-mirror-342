# -*- coding: utf-8 -*-

import os
from pathlib import Path

from ..client import Client

IS_CI = "CI" in os.environ

if IS_CI:
    client = None
else:
    path_token = Path.home() / ".short.io" / "sanhehu_esc" / "sanhe-dev.txt"
    token = path_token.read_text().strip()
    client = Client(token=token)
