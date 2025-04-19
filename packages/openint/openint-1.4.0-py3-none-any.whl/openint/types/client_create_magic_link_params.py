# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ClientCreateMagicLinkParams", "ClientOptions"]


class ClientCreateMagicLinkParams(TypedDict, total=False):
    client_options: ClientOptions
    """Search params to configure the connect page.

    Not signed as part of JWT and therefore can be modified by client
    """

    validity_in_seconds: float
    """How long the magic link will be valid for (in seconds) before it expires"""


class ClientOptions(TypedDict, total=False):
    minus_background: Annotated[str, PropertyInfo(alias="--background")]

    minus_card: Annotated[str, PropertyInfo(alias="--card")]

    minus_card_foreground: Annotated[str, PropertyInfo(alias="--card-foreground")]

    minus_foreground: Annotated[str, PropertyInfo(alias="--foreground")]

    minus_primary: Annotated[str, PropertyInfo(alias="--primary")]

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
    """The name of the connector to limit connection to. Default to all otherwise"""

    debug: bool
    """Whether to enable debug mode"""

    view: Literal["add", "manage"]
    """The default view to show when the magic link is opened. Defaults to "add" """
