# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ListConnectorsResponse", "Item", "ItemIntegration", "ItemSchemas", "ItemScope"]


class ItemIntegration(BaseModel):
    id: str

    connector_name: Literal[
        "aircall",
        "airtable",
        "apollo",
        "brex",
        "coda",
        "confluence",
        "discord",
        "dummy-oauth2",
        "facebook",
        "finch",
        "firebase",
        "foreceipt",
        "github",
        "gong",
        "googlecalendar",
        "googledocs",
        "googledrive",
        "googlemail",
        "googlesheet",
        "greenhouse",
        "heron",
        "hubspot",
        "instagram",
        "intercom",
        "jira",
        "kustomer",
        "lever",
        "linear",
        "linkedin",
        "lunchmoney",
        "mercury",
        "merge",
        "microsoft",
        "moota",
        "notion",
        "onebrick",
        "outreach",
        "pipedrive",
        "plaid",
        "postgres",
        "quickbooks",
        "ramp",
        "reddit",
        "salesforce",
        "salesloft",
        "saltedge",
        "sharepointonline",
        "slack",
        "splitwise",
        "stripe",
        "teller",
        "toggl",
        "twenty",
        "twitter",
        "venmo",
        "wise",
        "xero",
        "yodlee",
        "zohodesk",
    ]

    created_at: str

    external: Union[str, float, bool, Dict[str, object], List[object], None] = None

    name: str

    standard: Union[str, float, bool, Dict[str, object], List[object], None] = None

    updated_at: str

    auth_type: Optional[str] = None

    category: Optional[str] = None

    logo_url: Optional[str] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop"]]] = None

    stage: Optional[Literal["alpha", "beta", "ga"]] = None

    version: Optional[str] = None


class ItemSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ItemScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class Item(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    integrations: Optional[List[ItemIntegration]] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ItemSchemas] = None

    scopes: Optional[List[ItemScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ListConnectorsResponse(BaseModel):
    items: List[Item]

    limit: int
    """Limit the number of items returned"""

    offset: int
    """Offset the items returned"""

    total: int
    """Total number of items in the database for the organization"""
