# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["ClientListConnectionConfigsParams"]


class ClientListConnectionConfigsParams(TypedDict, total=False):
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

    expand: List[Literal["connector", "connector.schemas", "connection_count"]]

    limit: int

    offset: int
