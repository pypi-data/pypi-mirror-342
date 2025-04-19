# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["ClientGetConnectionParams"]


class ClientGetConnectionParams(TypedDict, total=False):
    expand: List[Literal["connector"]]

    include_secrets: Literal["none", "basic", "all"]
    """Controls secret inclusion: none (default), basic (auth only), or all secrets"""

    refresh_policy: Literal["none", "force", "auto"]
    """
    Controls credential refresh: none (never), force (always), or auto (when
    expired, default)
    """
