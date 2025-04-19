# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["CheckConnectionResponse"]


class CheckConnectionResponse(BaseModel):
    id: str
    """The id of the connection, starts with `conn_`"""

    status: Literal["healthy", "disconnected", "error", "manual"]
    """
    Connection status: healthy (all well), disconnected (needs reconnection), error
    (system issue), manual (import connection)
    """

    error: Optional[Literal["refresh_failed", "unknown_external_error"]] = None
    """Error types: refresh_failed and unknown_external_error"""

    error_message: Optional[str] = FieldInfo(alias="errorMessage", default=None)
    """Optional expanded error message"""
