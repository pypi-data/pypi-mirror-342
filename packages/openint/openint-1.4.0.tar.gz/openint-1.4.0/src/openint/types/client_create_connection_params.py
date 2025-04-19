# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "ClientCreateConnectionParams",
    "Data",
    "DataConnectorDummyOauth2DiscriminatedConnectionSettings",
    "DataConnectorDummyOauth2DiscriminatedConnectionSettingsSettings",
    "DataConnectorDummyOauth2DiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorDummyOauth2DiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorSharepointonlineDiscriminatedConnectionSettings",
    "DataConnectorSharepointonlineDiscriminatedConnectionSettingsSettings",
    "DataConnectorSharepointonlineDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorSharepointonlineDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorSlackDiscriminatedConnectionSettings",
    "DataConnectorSlackDiscriminatedConnectionSettingsSettings",
    "DataConnectorSlackDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorSlackDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorGitHubDiscriminatedConnectionSettings",
    "DataConnectorGitHubDiscriminatedConnectionSettingsSettings",
    "DataConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorQuickbooksDiscriminatedConnectionSettings",
    "DataConnectorQuickbooksDiscriminatedConnectionSettingsSettings",
    "DataConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorGooglemailDiscriminatedConnectionSettings",
    "DataConnectorGooglemailDiscriminatedConnectionSettingsSettings",
    "DataConnectorGooglemailDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorGooglemailDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorNotionDiscriminatedConnectionSettings",
    "DataConnectorNotionDiscriminatedConnectionSettingsSettings",
    "DataConnectorNotionDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorNotionDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorLinkedinDiscriminatedConnectionSettings",
    "DataConnectorLinkedinDiscriminatedConnectionSettingsSettings",
    "DataConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorGoogledocsDiscriminatedConnectionSettings",
    "DataConnectorGoogledocsDiscriminatedConnectionSettingsSettings",
    "DataConnectorGoogledocsDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorGoogledocsDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorAircallDiscriminatedConnectionSettings",
    "DataConnectorAircallDiscriminatedConnectionSettingsSettings",
    "DataConnectorAircallDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorAircallDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorGooglecalendarDiscriminatedConnectionSettings",
    "DataConnectorGooglecalendarDiscriminatedConnectionSettingsSettings",
    "DataConnectorGooglecalendarDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorGooglecalendarDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorGooglesheetDiscriminatedConnectionSettings",
    "DataConnectorGooglesheetDiscriminatedConnectionSettingsSettings",
    "DataConnectorGooglesheetDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorGooglesheetDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorDiscordDiscriminatedConnectionSettings",
    "DataConnectorDiscordDiscriminatedConnectionSettingsSettings",
    "DataConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorHubspotDiscriminatedConnectionSettings",
    "DataConnectorHubspotDiscriminatedConnectionSettingsSettings",
    "DataConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorSalesforceDiscriminatedConnectionSettings",
    "DataConnectorSalesforceDiscriminatedConnectionSettingsSettings",
    "DataConnectorSalesforceDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorSalesforceDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorLinearDiscriminatedConnectionSettings",
    "DataConnectorLinearDiscriminatedConnectionSettingsSettings",
    "DataConnectorLinearDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorLinearDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorConfluenceDiscriminatedConnectionSettings",
    "DataConnectorConfluenceDiscriminatedConnectionSettingsSettings",
    "DataConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorGoogledriveDiscriminatedConnectionSettings",
    "DataConnectorGoogledriveDiscriminatedConnectionSettingsSettings",
    "DataConnectorGoogledriveDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorGoogledriveDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorAirtableDiscriminatedConnectionSettings",
    "DataConnectorAirtableDiscriminatedConnectionSettingsSettings",
    "DataConnectorApolloDiscriminatedConnectionSettings",
    "DataConnectorApolloDiscriminatedConnectionSettingsSettings",
    "DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorApolloDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorBrexDiscriminatedConnectionSettings",
    "DataConnectorBrexDiscriminatedConnectionSettingsSettings",
    "DataConnectorCodaDiscriminatedConnectionSettings",
    "DataConnectorCodaDiscriminatedConnectionSettingsSettings",
    "DataConnectorFacebookDiscriminatedConnectionSettings",
    "DataConnectorFacebookDiscriminatedConnectionSettingsSettings",
    "DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorFacebookDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorFinchDiscriminatedConnectionSettings",
    "DataConnectorFinchDiscriminatedConnectionSettingsSettings",
    "DataConnectorFirebaseDiscriminatedConnectionSettings",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettings",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccount",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthData",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJson",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember1",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember2",
    "DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1FirebaseConfig",
    "DataConnectorForeceiptDiscriminatedConnectionSettings",
    "DataConnectorForeceiptDiscriminatedConnectionSettingsSettings",
    "DataConnectorGongDiscriminatedConnectionSettings",
    "DataConnectorGongDiscriminatedConnectionSettingsSettings",
    "DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorGongDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorGreenhouseDiscriminatedConnectionSettings",
    "DataConnectorGreenhouseDiscriminatedConnectionSettingsSettings",
    "DataConnectorHeronDiscriminatedConnectionSettings",
    "DataConnectorInstagramDiscriminatedConnectionSettings",
    "DataConnectorInstagramDiscriminatedConnectionSettingsSettings",
    "DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorInstagramDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorIntercomDiscriminatedConnectionSettings",
    "DataConnectorIntercomDiscriminatedConnectionSettingsSettings",
    "DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorIntercomDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorJiraDiscriminatedConnectionSettings",
    "DataConnectorJiraDiscriminatedConnectionSettingsSettings",
    "DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorJiraDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorKustomerDiscriminatedConnectionSettings",
    "DataConnectorKustomerDiscriminatedConnectionSettingsSettings",
    "DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorKustomerDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorLeverDiscriminatedConnectionSettings",
    "DataConnectorLeverDiscriminatedConnectionSettingsSettings",
    "DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorLeverDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorLunchmoneyDiscriminatedConnectionSettings",
    "DataConnectorMercuryDiscriminatedConnectionSettings",
    "DataConnectorMergeDiscriminatedConnectionSettings",
    "DataConnectorMergeDiscriminatedConnectionSettingsSettings",
    "DataConnectorMicrosoftDiscriminatedConnectionSettings",
    "DataConnectorMicrosoftDiscriminatedConnectionSettingsSettings",
    "DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorMootaDiscriminatedConnectionSettings",
    "DataConnectorOnebrickDiscriminatedConnectionSettings",
    "DataConnectorOnebrickDiscriminatedConnectionSettingsSettings",
    "DataConnectorOutreachDiscriminatedConnectionSettings",
    "DataConnectorOutreachDiscriminatedConnectionSettingsSettings",
    "DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorOutreachDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorPipedriveDiscriminatedConnectionSettings",
    "DataConnectorPipedriveDiscriminatedConnectionSettingsSettings",
    "DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorPlaidDiscriminatedConnectionSettings",
    "DataConnectorPlaidDiscriminatedConnectionSettingsSettings",
    "DataConnectorPostgresDiscriminatedConnectionSettings",
    "DataConnectorPostgresDiscriminatedConnectionSettingsSettings",
    "DataConnectorPostgresDiscriminatedConnectionSettingsSettingsSourceQueries",
    "DataConnectorRampDiscriminatedConnectionSettings",
    "DataConnectorRampDiscriminatedConnectionSettingsSettings",
    "DataConnectorRedditDiscriminatedConnectionSettings",
    "DataConnectorRedditDiscriminatedConnectionSettingsSettings",
    "DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorRedditDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorSalesloftDiscriminatedConnectionSettings",
    "DataConnectorSalesloftDiscriminatedConnectionSettingsSettings",
    "DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorSaltedgeDiscriminatedConnectionSettings",
    "DataConnectorSplitwiseDiscriminatedConnectionSettings",
    "DataConnectorSplitwiseDiscriminatedConnectionSettingsSettings",
    "DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUser",
    "DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserNotifications",
    "DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserPicture",
    "DataConnectorStripeDiscriminatedConnectionSettings",
    "DataConnectorStripeDiscriminatedConnectionSettingsSettings",
    "DataConnectorTellerDiscriminatedConnectionSettings",
    "DataConnectorTellerDiscriminatedConnectionSettingsSettings",
    "DataConnectorTogglDiscriminatedConnectionSettings",
    "DataConnectorTogglDiscriminatedConnectionSettingsSettings",
    "DataConnectorTwentyDiscriminatedConnectionSettings",
    "DataConnectorTwentyDiscriminatedConnectionSettingsSettings",
    "DataConnectorTwitterDiscriminatedConnectionSettings",
    "DataConnectorTwitterDiscriminatedConnectionSettingsSettings",
    "DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorTwitterDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorVenmoDiscriminatedConnectionSettings",
    "DataConnectorVenmoDiscriminatedConnectionSettingsSettings",
    "DataConnectorWiseDiscriminatedConnectionSettings",
    "DataConnectorWiseDiscriminatedConnectionSettingsSettings",
    "DataConnectorXeroDiscriminatedConnectionSettings",
    "DataConnectorXeroDiscriminatedConnectionSettingsSettings",
    "DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorXeroDiscriminatedConnectionSettingsSettingsError",
    "DataConnectorYodleeDiscriminatedConnectionSettings",
    "DataConnectorYodleeDiscriminatedConnectionSettingsSettings",
    "DataConnectorYodleeDiscriminatedConnectionSettingsSettingsAccessToken",
    "DataConnectorYodleeDiscriminatedConnectionSettingsSettingsProviderAccount",
    "DataConnectorZohodeskDiscriminatedConnectionSettings",
    "DataConnectorZohodeskDiscriminatedConnectionSettingsSettings",
    "DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuth",
    "DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsError",
]


class ClientCreateConnectionParams(TypedDict, total=False):
    connector_config_id: Required[str]
    """The id of the connector config, starts with `ccfg_`"""

    customer_id: Required[str]
    """The id of the customer in your application.

    Ensure it is unique for that customer.
    """

    data: Required[Data]
    """Connector specific data"""

    metadata: Dict[str, object]


class DataConnectorDummyOauth2DiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorDummyOauth2DiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorDummyOauth2DiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorDummyOauth2DiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorDummyOauth2DiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorDummyOauth2DiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["dummy-oauth2"]]

    settings: Required[DataConnectorDummyOauth2DiscriminatedConnectionSettingsSettings]


class DataConnectorSharepointonlineDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorSharepointonlineDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorSharepointonlineDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorSharepointonlineDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorSharepointonlineDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorSharepointonlineDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["sharepointonline"]]

    settings: Required[DataConnectorSharepointonlineDiscriminatedConnectionSettingsSettings]


class DataConnectorSlackDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorSlackDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorSlackDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorSlackDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorSlackDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorSlackDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["slack"]]

    settings: Required[DataConnectorSlackDiscriminatedConnectionSettingsSettings]


class DataConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorGitHubDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorGitHubDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["github"]]

    settings: Required[DataConnectorGitHubDiscriminatedConnectionSettingsSettings]


class DataConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorQuickbooksDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuth]

    realm_id: Required[Annotated[str, PropertyInfo(alias="realmId")]]
    """The realmId of your quickbooks company (e.g., 9341453474484455)"""


class DataConnectorQuickbooksDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["quickbooks"]]

    settings: Required[DataConnectorQuickbooksDiscriminatedConnectionSettingsSettings]


class DataConnectorGooglemailDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorGooglemailDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorGooglemailDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorGooglemailDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorGooglemailDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorGooglemailDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["googlemail"]]

    settings: Required[DataConnectorGooglemailDiscriminatedConnectionSettingsSettings]


class DataConnectorNotionDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorNotionDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorNotionDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorNotionDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorNotionDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorNotionDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["notion"]]

    settings: Required[DataConnectorNotionDiscriminatedConnectionSettingsSettings]


class DataConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorLinkedinDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorLinkedinDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["linkedin"]]

    settings: Required[DataConnectorLinkedinDiscriminatedConnectionSettingsSettings]


class DataConnectorGoogledocsDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorGoogledocsDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorGoogledocsDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorGoogledocsDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorGoogledocsDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorGoogledocsDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["googledocs"]]

    settings: Required[DataConnectorGoogledocsDiscriminatedConnectionSettingsSettings]


class DataConnectorAircallDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorAircallDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorAircallDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorAircallDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorAircallDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorAircallDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["aircall"]]

    settings: Required[DataConnectorAircallDiscriminatedConnectionSettingsSettings]


class DataConnectorGooglecalendarDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorGooglecalendarDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorGooglecalendarDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorGooglecalendarDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorGooglecalendarDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorGooglecalendarDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["googlecalendar"]]

    settings: Required[DataConnectorGooglecalendarDiscriminatedConnectionSettingsSettings]


class DataConnectorGooglesheetDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorGooglesheetDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorGooglesheetDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorGooglesheetDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorGooglesheetDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorGooglesheetDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["googlesheet"]]

    settings: Required[DataConnectorGooglesheetDiscriminatedConnectionSettingsSettings]


class DataConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorDiscordDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorDiscordDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["discord"]]

    settings: Required[DataConnectorDiscordDiscriminatedConnectionSettingsSettings]


class DataConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorHubspotDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorHubspotDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["hubspot"]]

    settings: Required[DataConnectorHubspotDiscriminatedConnectionSettingsSettings]


class DataConnectorSalesforceDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorSalesforceDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorSalesforceDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorSalesforceDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    instance_url: Required[str]
    """The instance URL of your Salesforce account (e.g., example)"""

    oauth: Required[DataConnectorSalesforceDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorSalesforceDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["salesforce"]]

    settings: Required[DataConnectorSalesforceDiscriminatedConnectionSettingsSettings]


class DataConnectorLinearDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorLinearDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorLinearDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorLinearDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorLinearDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorLinearDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["linear"]]

    settings: Required[DataConnectorLinearDiscriminatedConnectionSettingsSettings]


class DataConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorConfluenceDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorConfluenceDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["confluence"]]

    settings: Required[DataConnectorConfluenceDiscriminatedConnectionSettingsSettings]


class DataConnectorGoogledriveDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    access_token: Required[str]

    client_id: Required[str]
    """Client ID used for the connection"""

    raw: Required[Dict[str, object]]

    scope: Required[str]

    expires_at: str

    expires_in: float

    refresh_token: str

    token_type: str


class DataConnectorGoogledriveDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    created_at: str

    credentials: DataConnectorGoogledriveDiscriminatedConnectionSettingsSettingsOAuthCredentials
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: str

    metadata: Optional[Dict[str, object]]

    updated_at: str


class DataConnectorGoogledriveDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorGoogledriveDiscriminatedConnectionSettingsSettingsOAuth]


class DataConnectorGoogledriveDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["googledrive"]]

    settings: Required[DataConnectorGoogledriveDiscriminatedConnectionSettingsSettings]


class DataConnectorAirtableDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    airtable_base: Required[Annotated[str, PropertyInfo(alias="airtableBase")]]

    api_key: Required[Annotated[str, PropertyInfo(alias="apiKey")]]


class DataConnectorAirtableDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["airtable"]]

    settings: Required[DataConnectorAirtableDiscriminatedConnectionSettingsSettings]


class DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorApolloDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorApolloDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorApolloDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorApolloDiscriminatedConnectionSettingsSettingsError]


class DataConnectorApolloDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["apollo"]]

    settings: Required[DataConnectorApolloDiscriminatedConnectionSettingsSettings]


class DataConnectorBrexDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    access_token: Required[Annotated[str, PropertyInfo(alias="accessToken")]]


class DataConnectorBrexDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["brex"]]

    settings: Required[DataConnectorBrexDiscriminatedConnectionSettingsSettings]


class DataConnectorCodaDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    api_key: Required[Annotated[str, PropertyInfo(alias="apiKey")]]


class DataConnectorCodaDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["coda"]]

    settings: Required[DataConnectorCodaDiscriminatedConnectionSettingsSettings]


class DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorFacebookDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorFacebookDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorFacebookDiscriminatedConnectionSettingsSettingsError]


class DataConnectorFacebookDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["facebook"]]

    settings: Required[DataConnectorFacebookDiscriminatedConnectionSettingsSettings]


class DataConnectorFinchDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    access_token: Required[str]


class DataConnectorFinchDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["finch"]]

    settings: Required[DataConnectorFinchDiscriminatedConnectionSettingsSettings]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccountTyped(
    TypedDict, total=False
):
    project_id: Required[str]


DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccount: TypeAlias = Union[
    DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccountTyped, Dict[str, object]
]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0(TypedDict, total=False):
    role: Required[Literal["admin"]]

    service_account: Required[
        Annotated[
            DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccount,
            PropertyInfo(alias="serviceAccount"),
        ]
    ]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJsonTyped(
    TypedDict, total=False
):
    app_name: Required[Annotated[str, PropertyInfo(alias="appName")]]

    sts_token_manager: Required[Annotated[Dict[str, object], PropertyInfo(alias="stsTokenManager")]]

    uid: Required[str]


DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJson: TypeAlias = Union[
    DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJsonTyped,
    Dict[str, object],
]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0(
    TypedDict, total=False
):
    method: Required[Literal["userJson"]]

    user_json: Required[
        Annotated[
            DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJson,
            PropertyInfo(alias="userJson"),
        ]
    ]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember1(
    TypedDict, total=False
):
    custom_token: Required[Annotated[str, PropertyInfo(alias="customToken")]]

    method: Required[Literal["customToken"]]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember2(
    TypedDict, total=False
):
    email: Required[str]

    method: Required[Literal["emailPassword"]]

    password: Required[str]


DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthData: TypeAlias = Union[
    DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0,
    DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember1,
    DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember2,
]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1FirebaseConfig(TypedDict, total=False):
    api_key: Required[Annotated[str, PropertyInfo(alias="apiKey")]]

    app_id: Required[Annotated[str, PropertyInfo(alias="appId")]]

    auth_domain: Required[Annotated[str, PropertyInfo(alias="authDomain")]]

    database_url: Required[Annotated[str, PropertyInfo(alias="databaseURL")]]

    project_id: Required[Annotated[str, PropertyInfo(alias="projectId")]]

    measurement_id: Annotated[str, PropertyInfo(alias="measurementId")]

    messaging_sender_id: Annotated[str, PropertyInfo(alias="messagingSenderId")]

    storage_bucket: Annotated[str, PropertyInfo(alias="storageBucket")]


class DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1(TypedDict, total=False):
    auth_data: Required[
        Annotated[
            DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthData,
            PropertyInfo(alias="authData"),
        ]
    ]

    firebase_config: Required[
        Annotated[
            DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1FirebaseConfig,
            PropertyInfo(alias="firebaseConfig"),
        ]
    ]

    role: Required[Literal["user"]]


DataConnectorFirebaseDiscriminatedConnectionSettingsSettings: TypeAlias = Union[
    DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0,
    DataConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1,
]


class DataConnectorFirebaseDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["firebase"]]

    settings: Required[DataConnectorFirebaseDiscriminatedConnectionSettingsSettings]


class DataConnectorForeceiptDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    env_name: Required[Annotated[Literal["staging", "production"], PropertyInfo(alias="envName")]]

    _id: object

    credentials: object


class DataConnectorForeceiptDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["foreceipt"]]

    settings: Required[DataConnectorForeceiptDiscriminatedConnectionSettingsSettings]


class DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorGongDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorGongDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorGongDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorGongDiscriminatedConnectionSettingsSettingsError]


class DataConnectorGongDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["gong"]]

    settings: Required[DataConnectorGongDiscriminatedConnectionSettingsSettings]


class DataConnectorGreenhouseDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    api_key: Required[Annotated[str, PropertyInfo(alias="apiKey")]]


class DataConnectorGreenhouseDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["greenhouse"]]

    settings: Required[DataConnectorGreenhouseDiscriminatedConnectionSettingsSettings]


class DataConnectorHeronDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["heron"]]

    settings: Required[object]


class DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorInstagramDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorInstagramDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorInstagramDiscriminatedConnectionSettingsSettingsError]


class DataConnectorInstagramDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["instagram"]]

    settings: Required[DataConnectorInstagramDiscriminatedConnectionSettingsSettings]


class DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorIntercomDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorIntercomDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorIntercomDiscriminatedConnectionSettingsSettingsError]


class DataConnectorIntercomDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["intercom"]]

    settings: Required[DataConnectorIntercomDiscriminatedConnectionSettingsSettings]


class DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorJiraDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorJiraDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorJiraDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorJiraDiscriminatedConnectionSettingsSettingsError]


class DataConnectorJiraDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["jira"]]

    settings: Required[DataConnectorJiraDiscriminatedConnectionSettingsSettings]


class DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorKustomerDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorKustomerDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorKustomerDiscriminatedConnectionSettingsSettingsError]


class DataConnectorKustomerDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["kustomer"]]

    settings: Required[DataConnectorKustomerDiscriminatedConnectionSettingsSettings]


class DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorLeverDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorLeverDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorLeverDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorLeverDiscriminatedConnectionSettingsSettingsError]


class DataConnectorLeverDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["lever"]]

    settings: Required[DataConnectorLeverDiscriminatedConnectionSettingsSettings]


class DataConnectorLunchmoneyDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["lunchmoney"]]

    settings: Required[object]


class DataConnectorMercuryDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["mercury"]]

    settings: Required[object]


class DataConnectorMergeDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    account_token: Required[Annotated[str, PropertyInfo(alias="accountToken")]]

    account_details: Annotated[object, PropertyInfo(alias="accountDetails")]


class DataConnectorMergeDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["merge"]]

    settings: Required[DataConnectorMergeDiscriminatedConnectionSettingsSettings]


class DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorMicrosoftDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuth]

    client_id: str

    error: Optional[DataConnectorMicrosoftDiscriminatedConnectionSettingsSettingsError]


class DataConnectorMicrosoftDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["microsoft"]]

    settings: Required[DataConnectorMicrosoftDiscriminatedConnectionSettingsSettings]


class DataConnectorMootaDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["moota"]]

    settings: Required[object]


class DataConnectorOnebrickDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    access_token: Required[Annotated[str, PropertyInfo(alias="accessToken")]]


class DataConnectorOnebrickDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["onebrick"]]

    settings: Required[DataConnectorOnebrickDiscriminatedConnectionSettingsSettings]


class DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorOutreachDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorOutreachDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorOutreachDiscriminatedConnectionSettingsSettingsError]


class DataConnectorOutreachDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["outreach"]]

    settings: Required[DataConnectorOutreachDiscriminatedConnectionSettingsSettings]


class DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorPipedriveDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorPipedriveDiscriminatedConnectionSettingsSettingsError]


class DataConnectorPipedriveDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["pipedrive"]]

    settings: Required[DataConnectorPipedriveDiscriminatedConnectionSettingsSettings]


class DataConnectorPlaidDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    access_token: Required[Annotated[str, PropertyInfo(alias="accessToken")]]

    institution: object

    item: object

    item_id: Annotated[Optional[str], PropertyInfo(alias="itemId")]

    status: object

    webhook_item_error: Annotated[None, PropertyInfo(alias="webhookItemError")]


class DataConnectorPlaidDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["plaid"]]

    settings: Required[DataConnectorPlaidDiscriminatedConnectionSettingsSettings]


class DataConnectorPostgresDiscriminatedConnectionSettingsSettingsSourceQueries(TypedDict, total=False):
    invoice: Optional[str]
    """Should order by lastModifiedAt and id descending"""


class DataConnectorPostgresDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    database_url: Required[Annotated[str, PropertyInfo(alias="databaseUrl")]]

    source_queries: Annotated[
        DataConnectorPostgresDiscriminatedConnectionSettingsSettingsSourceQueries, PropertyInfo(alias="sourceQueries")
    ]


class DataConnectorPostgresDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["postgres"]]

    settings: Required[DataConnectorPostgresDiscriminatedConnectionSettingsSettings]


class DataConnectorRampDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    access_token: Annotated[Optional[str], PropertyInfo(alias="accessToken")]

    start_after_transaction_id: Annotated[Optional[str], PropertyInfo(alias="startAfterTransactionId")]


class DataConnectorRampDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["ramp"]]

    settings: Required[DataConnectorRampDiscriminatedConnectionSettingsSettings]


class DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorRedditDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorRedditDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorRedditDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorRedditDiscriminatedConnectionSettingsSettingsError]


class DataConnectorRedditDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["reddit"]]

    settings: Required[DataConnectorRedditDiscriminatedConnectionSettingsSettings]


class DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorSalesloftDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorSalesloftDiscriminatedConnectionSettingsSettingsError]


class DataConnectorSalesloftDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["salesloft"]]

    settings: Required[DataConnectorSalesloftDiscriminatedConnectionSettingsSettings]


class DataConnectorSaltedgeDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["saltedge"]]

    settings: object


class DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserNotifications(TypedDict, total=False):
    added_as_friend: Required[bool]

    added_to_group: Required[bool]

    announcements: Required[bool]

    bills: Required[bool]

    expense_added: Required[bool]

    expense_updated: Required[bool]

    monthly_summary: Required[bool]

    payments: Required[bool]


class DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserPicture(TypedDict, total=False):
    large: Optional[str]

    medium: Optional[str]

    original: Optional[str]

    small: Optional[str]

    xlarge: Optional[str]

    xxlarge: Optional[str]


class DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUser(TypedDict, total=False):
    id: Required[float]

    country_code: Required[str]

    custom_picture: Required[bool]

    date_format: Required[str]

    default_currency: Required[str]

    default_group_id: Required[float]

    email: Required[str]

    first_name: Required[str]

    force_refresh_at: Required[str]

    last_name: Required[str]

    locale: Required[str]

    notifications: Required[DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserNotifications]

    notifications_count: Required[float]

    notifications_read: Required[str]

    picture: Required[DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserPicture]

    registration_status: Required[str]


class DataConnectorSplitwiseDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    access_token: Required[Annotated[str, PropertyInfo(alias="accessToken")]]

    current_user: Annotated[
        Optional[DataConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUser],
        PropertyInfo(alias="currentUser"),
    ]


class DataConnectorSplitwiseDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["splitwise"]]

    settings: Required[DataConnectorSplitwiseDiscriminatedConnectionSettingsSettings]


class DataConnectorStripeDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    secret_key: Required[Annotated[str, PropertyInfo(alias="secretKey")]]


class DataConnectorStripeDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["stripe"]]

    settings: Required[DataConnectorStripeDiscriminatedConnectionSettingsSettings]


class DataConnectorTellerDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    token: Required[str]


class DataConnectorTellerDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["teller"]]

    settings: Required[DataConnectorTellerDiscriminatedConnectionSettingsSettings]


class DataConnectorTogglDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    api_token: Required[Annotated[str, PropertyInfo(alias="apiToken")]]

    email: Optional[str]

    password: Optional[str]


class DataConnectorTogglDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["toggl"]]

    settings: Required[DataConnectorTogglDiscriminatedConnectionSettingsSettings]


class DataConnectorTwentyDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    access_token: Required[str]


class DataConnectorTwentyDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["twenty"]]

    settings: Required[DataConnectorTwentyDiscriminatedConnectionSettingsSettings]


class DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorTwitterDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorTwitterDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorTwitterDiscriminatedConnectionSettingsSettingsError]


class DataConnectorTwitterDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["twitter"]]

    settings: Required[DataConnectorTwitterDiscriminatedConnectionSettingsSettings]


class DataConnectorVenmoDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    credentials: object

    me: object


class DataConnectorVenmoDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["venmo"]]

    settings: Required[DataConnectorVenmoDiscriminatedConnectionSettingsSettings]


class DataConnectorWiseDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    env_name: Required[Annotated[Literal["sandbox", "live"], PropertyInfo(alias="envName")]]

    api_token: Annotated[Optional[str], PropertyInfo(alias="apiToken")]


class DataConnectorWiseDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["wise"]]

    settings: Required[DataConnectorWiseDiscriminatedConnectionSettingsSettings]


class DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorXeroDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorXeroDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorXeroDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorXeroDiscriminatedConnectionSettingsSettingsError]


class DataConnectorXeroDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["xero"]]

    settings: Required[DataConnectorXeroDiscriminatedConnectionSettingsSettings]


class DataConnectorYodleeDiscriminatedConnectionSettingsSettingsAccessToken(TypedDict, total=False):
    access_token: Required[Annotated[str, PropertyInfo(alias="accessToken")]]

    expires_in: Required[Annotated[float, PropertyInfo(alias="expiresIn")]]

    issued_at: Required[Annotated[str, PropertyInfo(alias="issuedAt")]]


class DataConnectorYodleeDiscriminatedConnectionSettingsSettingsProviderAccount(TypedDict, total=False):
    id: Required[float]

    aggregation_source: Required[Annotated[str, PropertyInfo(alias="aggregationSource")]]

    created_date: Required[Annotated[str, PropertyInfo(alias="createdDate")]]

    dataset: Required[Iterable[object]]

    is_manual: Required[Annotated[bool, PropertyInfo(alias="isManual")]]

    provider_id: Required[Annotated[float, PropertyInfo(alias="providerId")]]

    status: Required[
        Literal["LOGIN_IN_PROGRESS", "USER_INPUT_REQUIRED", "IN_PROGRESS", "PARTIAL_SUCCESS", "SUCCESS", "FAILED"]
    ]

    is_deleted: Annotated[Optional[bool], PropertyInfo(alias="isDeleted")]


class DataConnectorYodleeDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    login_name: Required[Annotated[str, PropertyInfo(alias="loginName")]]

    provider_account_id: Required[Annotated[Union[float, str], PropertyInfo(alias="providerAccountId")]]

    access_token: Annotated[
        Optional[DataConnectorYodleeDiscriminatedConnectionSettingsSettingsAccessToken],
        PropertyInfo(alias="accessToken"),
    ]

    provider: None

    provider_account: Annotated[
        Optional[DataConnectorYodleeDiscriminatedConnectionSettingsSettingsProviderAccount],
        PropertyInfo(alias="providerAccount"),
    ]

    user: None


class DataConnectorYodleeDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["yodlee"]]

    settings: Required[DataConnectorYodleeDiscriminatedConnectionSettingsSettings]


class DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped(TypedDict, total=False):
    access_token: Required[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    expires_in: float

    refresh_token: Optional[str]

    refresh_token_expires_in: Optional[float]

    scope: str

    token_type: Optional[str]


DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw: TypeAlias = Union[
    DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentialsRawTyped, Dict[str, object]
]


class DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentials(TypedDict, total=False):
    raw: Required[DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw]

    type: Required[Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]]

    access_token: str

    api_key: Optional[str]

    expires_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    refresh_token: str


class DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped(TypedDict, total=False):
    instance_url: Optional[str]

    portal_id: Annotated[Optional[float], PropertyInfo(alias="portalId")]


DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig: TypeAlias = Union[
    DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthConnectionConfigTyped, Dict[str, object]
]


class DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuth(TypedDict, total=False):
    credentials: Required[DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentials]

    metadata: Required[Optional[Dict[str, object]]]

    connection_config: Optional[DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig]


class DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsError(TypedDict, total=False):
    code: Required[Union[Literal["refresh_token_external_error"], str]]

    message: Optional[str]


class DataConnectorZohodeskDiscriminatedConnectionSettingsSettings(TypedDict, total=False):
    oauth: Required[DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuth]

    error: Optional[DataConnectorZohodeskDiscriminatedConnectionSettingsSettingsError]


class DataConnectorZohodeskDiscriminatedConnectionSettings(TypedDict, total=False):
    connector_name: Required[Literal["zohodesk"]]

    settings: Required[DataConnectorZohodeskDiscriminatedConnectionSettingsSettings]


Data: TypeAlias = Union[
    DataConnectorDummyOauth2DiscriminatedConnectionSettings,
    DataConnectorSharepointonlineDiscriminatedConnectionSettings,
    DataConnectorSlackDiscriminatedConnectionSettings,
    DataConnectorGitHubDiscriminatedConnectionSettings,
    DataConnectorQuickbooksDiscriminatedConnectionSettings,
    DataConnectorGooglemailDiscriminatedConnectionSettings,
    DataConnectorNotionDiscriminatedConnectionSettings,
    DataConnectorLinkedinDiscriminatedConnectionSettings,
    DataConnectorGoogledocsDiscriminatedConnectionSettings,
    DataConnectorAircallDiscriminatedConnectionSettings,
    DataConnectorGooglecalendarDiscriminatedConnectionSettings,
    DataConnectorGooglesheetDiscriminatedConnectionSettings,
    DataConnectorDiscordDiscriminatedConnectionSettings,
    DataConnectorHubspotDiscriminatedConnectionSettings,
    DataConnectorSalesforceDiscriminatedConnectionSettings,
    DataConnectorLinearDiscriminatedConnectionSettings,
    DataConnectorConfluenceDiscriminatedConnectionSettings,
    DataConnectorGoogledriveDiscriminatedConnectionSettings,
    DataConnectorAirtableDiscriminatedConnectionSettings,
    DataConnectorApolloDiscriminatedConnectionSettings,
    DataConnectorBrexDiscriminatedConnectionSettings,
    DataConnectorCodaDiscriminatedConnectionSettings,
    DataConnectorFacebookDiscriminatedConnectionSettings,
    DataConnectorFinchDiscriminatedConnectionSettings,
    DataConnectorFirebaseDiscriminatedConnectionSettings,
    DataConnectorForeceiptDiscriminatedConnectionSettings,
    DataConnectorGongDiscriminatedConnectionSettings,
    DataConnectorGreenhouseDiscriminatedConnectionSettings,
    DataConnectorHeronDiscriminatedConnectionSettings,
    DataConnectorInstagramDiscriminatedConnectionSettings,
    DataConnectorIntercomDiscriminatedConnectionSettings,
    DataConnectorJiraDiscriminatedConnectionSettings,
    DataConnectorKustomerDiscriminatedConnectionSettings,
    DataConnectorLeverDiscriminatedConnectionSettings,
    DataConnectorLunchmoneyDiscriminatedConnectionSettings,
    DataConnectorMercuryDiscriminatedConnectionSettings,
    DataConnectorMergeDiscriminatedConnectionSettings,
    DataConnectorMicrosoftDiscriminatedConnectionSettings,
    DataConnectorMootaDiscriminatedConnectionSettings,
    DataConnectorOnebrickDiscriminatedConnectionSettings,
    DataConnectorOutreachDiscriminatedConnectionSettings,
    DataConnectorPipedriveDiscriminatedConnectionSettings,
    DataConnectorPlaidDiscriminatedConnectionSettings,
    DataConnectorPostgresDiscriminatedConnectionSettings,
    DataConnectorRampDiscriminatedConnectionSettings,
    DataConnectorRedditDiscriminatedConnectionSettings,
    DataConnectorSalesloftDiscriminatedConnectionSettings,
    DataConnectorSaltedgeDiscriminatedConnectionSettings,
    DataConnectorSplitwiseDiscriminatedConnectionSettings,
    DataConnectorStripeDiscriminatedConnectionSettings,
    DataConnectorTellerDiscriminatedConnectionSettings,
    DataConnectorTogglDiscriminatedConnectionSettings,
    DataConnectorTwentyDiscriminatedConnectionSettings,
    DataConnectorTwitterDiscriminatedConnectionSettings,
    DataConnectorVenmoDiscriminatedConnectionSettings,
    DataConnectorWiseDiscriminatedConnectionSettings,
    DataConnectorXeroDiscriminatedConnectionSettings,
    DataConnectorYodleeDiscriminatedConnectionSettings,
    DataConnectorZohodeskDiscriminatedConnectionSettings,
]
