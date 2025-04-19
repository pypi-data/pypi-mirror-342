# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "CreateConnectionResponse",
    "ConnectorDummyOauth2DiscriminatedConnectionSettings",
    "ConnectorDummyOauth2DiscriminatedConnectionSettingsSettings",
    "ConnectorDummyOauth2DiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorDummyOauth2DiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorSharepointonlineDiscriminatedConnectionSettings",
    "ConnectorSharepointonlineDiscriminatedConnectionSettingsSettings",
    "ConnectorSharepointonlineDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorSharepointonlineDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorSlackDiscriminatedConnectionSettings",
    "ConnectorSlackDiscriminatedConnectionSettingsSettings",
    "ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGitHubDiscriminatedConnectionSettings",
    "ConnectorGitHubDiscriminatedConnectionSettingsSettings",
    "ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorQuickbooksDiscriminatedConnectionSettings",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsSettings",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGooglemailDiscriminatedConnectionSettings",
    "ConnectorGooglemailDiscriminatedConnectionSettingsSettings",
    "ConnectorGooglemailDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGooglemailDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorNotionDiscriminatedConnectionSettings",
    "ConnectorNotionDiscriminatedConnectionSettingsSettings",
    "ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorLinkedinDiscriminatedConnectionSettings",
    "ConnectorLinkedinDiscriminatedConnectionSettingsSettings",
    "ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGoogledocsDiscriminatedConnectionSettings",
    "ConnectorGoogledocsDiscriminatedConnectionSettingsSettings",
    "ConnectorGoogledocsDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGoogledocsDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorAircallDiscriminatedConnectionSettings",
    "ConnectorAircallDiscriminatedConnectionSettingsSettings",
    "ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGooglecalendarDiscriminatedConnectionSettings",
    "ConnectorGooglecalendarDiscriminatedConnectionSettingsSettings",
    "ConnectorGooglecalendarDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGooglecalendarDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGooglesheetDiscriminatedConnectionSettings",
    "ConnectorGooglesheetDiscriminatedConnectionSettingsSettings",
    "ConnectorGooglesheetDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGooglesheetDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorDiscordDiscriminatedConnectionSettings",
    "ConnectorDiscordDiscriminatedConnectionSettingsSettings",
    "ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorHubspotDiscriminatedConnectionSettings",
    "ConnectorHubspotDiscriminatedConnectionSettingsSettings",
    "ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorSalesforceDiscriminatedConnectionSettings",
    "ConnectorSalesforceDiscriminatedConnectionSettingsSettings",
    "ConnectorSalesforceDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorSalesforceDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorLinearDiscriminatedConnectionSettings",
    "ConnectorLinearDiscriminatedConnectionSettingsSettings",
    "ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorConfluenceDiscriminatedConnectionSettings",
    "ConnectorConfluenceDiscriminatedConnectionSettingsSettings",
    "ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGoogledriveDiscriminatedConnectionSettings",
    "ConnectorGoogledriveDiscriminatedConnectionSettingsSettings",
    "ConnectorGoogledriveDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGoogledriveDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorAirtableDiscriminatedConnectionSettings",
    "ConnectorAirtableDiscriminatedConnectionSettingsSettings",
    "ConnectorApolloDiscriminatedConnectionSettings",
    "ConnectorApolloDiscriminatedConnectionSettingsSettings",
    "ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorApolloDiscriminatedConnectionSettingsSettingsError",
    "ConnectorBrexDiscriminatedConnectionSettings",
    "ConnectorBrexDiscriminatedConnectionSettingsSettings",
    "ConnectorCodaDiscriminatedConnectionSettings",
    "ConnectorCodaDiscriminatedConnectionSettingsSettings",
    "ConnectorFacebookDiscriminatedConnectionSettings",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettings",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettingsError",
    "ConnectorFinchDiscriminatedConnectionSettings",
    "ConnectorFinchDiscriminatedConnectionSettingsSettings",
    "ConnectorFirebaseDiscriminatedConnectionSettings",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettings",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccount",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthData",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJson",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember1",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember2",
    "ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1FirebaseConfig",
    "ConnectorForeceiptDiscriminatedConnectionSettings",
    "ConnectorForeceiptDiscriminatedConnectionSettingsSettings",
    "ConnectorGongDiscriminatedConnectionSettings",
    "ConnectorGongDiscriminatedConnectionSettingsSettings",
    "ConnectorGongDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorGongDiscriminatedConnectionSettingsSettingsError",
    "ConnectorGreenhouseDiscriminatedConnectionSettings",
    "ConnectorGreenhouseDiscriminatedConnectionSettingsSettings",
    "ConnectorHeronDiscriminatedConnectionSettings",
    "ConnectorInstagramDiscriminatedConnectionSettings",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettings",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettingsError",
    "ConnectorIntercomDiscriminatedConnectionSettings",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettings",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettingsError",
    "ConnectorJiraDiscriminatedConnectionSettings",
    "ConnectorJiraDiscriminatedConnectionSettingsSettings",
    "ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorJiraDiscriminatedConnectionSettingsSettingsError",
    "ConnectorKustomerDiscriminatedConnectionSettings",
    "ConnectorKustomerDiscriminatedConnectionSettingsSettings",
    "ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorKustomerDiscriminatedConnectionSettingsSettingsError",
    "ConnectorLeverDiscriminatedConnectionSettings",
    "ConnectorLeverDiscriminatedConnectionSettingsSettings",
    "ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorLeverDiscriminatedConnectionSettingsSettingsError",
    "ConnectorLunchmoneyDiscriminatedConnectionSettings",
    "ConnectorMercuryDiscriminatedConnectionSettings",
    "ConnectorMergeDiscriminatedConnectionSettings",
    "ConnectorMergeDiscriminatedConnectionSettingsSettings",
    "ConnectorMicrosoftDiscriminatedConnectionSettings",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsSettings",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsError",
    "ConnectorMootaDiscriminatedConnectionSettings",
    "ConnectorOnebrickDiscriminatedConnectionSettings",
    "ConnectorOnebrickDiscriminatedConnectionSettingsSettings",
    "ConnectorOutreachDiscriminatedConnectionSettings",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettings",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettingsError",
    "ConnectorPipedriveDiscriminatedConnectionSettings",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettings",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettingsError",
    "ConnectorPlaidDiscriminatedConnectionSettings",
    "ConnectorPlaidDiscriminatedConnectionSettingsSettings",
    "ConnectorPostgresDiscriminatedConnectionSettings",
    "ConnectorPostgresDiscriminatedConnectionSettingsSettings",
    "ConnectorPostgresDiscriminatedConnectionSettingsSettingsSourceQueries",
    "ConnectorRampDiscriminatedConnectionSettings",
    "ConnectorRampDiscriminatedConnectionSettingsSettings",
    "ConnectorRedditDiscriminatedConnectionSettings",
    "ConnectorRedditDiscriminatedConnectionSettingsSettings",
    "ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorRedditDiscriminatedConnectionSettingsSettingsError",
    "ConnectorSalesloftDiscriminatedConnectionSettings",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettings",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettingsError",
    "ConnectorSaltedgeDiscriminatedConnectionSettings",
    "ConnectorSplitwiseDiscriminatedConnectionSettings",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettings",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUser",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserNotifications",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserPicture",
    "ConnectorStripeDiscriminatedConnectionSettings",
    "ConnectorStripeDiscriminatedConnectionSettingsSettings",
    "ConnectorTellerDiscriminatedConnectionSettings",
    "ConnectorTellerDiscriminatedConnectionSettingsSettings",
    "ConnectorTogglDiscriminatedConnectionSettings",
    "ConnectorTogglDiscriminatedConnectionSettingsSettings",
    "ConnectorTwentyDiscriminatedConnectionSettings",
    "ConnectorTwentyDiscriminatedConnectionSettingsSettings",
    "ConnectorTwitterDiscriminatedConnectionSettings",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettings",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettingsError",
    "ConnectorVenmoDiscriminatedConnectionSettings",
    "ConnectorVenmoDiscriminatedConnectionSettingsSettings",
    "ConnectorWiseDiscriminatedConnectionSettings",
    "ConnectorWiseDiscriminatedConnectionSettingsSettings",
    "ConnectorXeroDiscriminatedConnectionSettings",
    "ConnectorXeroDiscriminatedConnectionSettingsSettings",
    "ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorXeroDiscriminatedConnectionSettingsSettingsError",
    "ConnectorYodleeDiscriminatedConnectionSettings",
    "ConnectorYodleeDiscriminatedConnectionSettingsSettings",
    "ConnectorYodleeDiscriminatedConnectionSettingsSettingsAccessToken",
    "ConnectorYodleeDiscriminatedConnectionSettingsSettingsProviderAccount",
    "ConnectorZohodeskDiscriminatedConnectionSettings",
    "ConnectorZohodeskDiscriminatedConnectionSettingsSettings",
    "ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorZohodeskDiscriminatedConnectionSettingsSettingsError",
]


class ConnectorDummyOauth2DiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorDummyOauth2DiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorDummyOauth2DiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorDummyOauth2DiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorDummyOauth2DiscriminatedConnectionSettingsSettingsOAuth


class ConnectorDummyOauth2DiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["dummy-oauth2"]

    settings: ConnectorDummyOauth2DiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorSharepointonlineDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorSharepointonlineDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorSharepointonlineDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorSharepointonlineDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorSharepointonlineDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorSharepointonlineDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["sharepointonline"]

    settings: ConnectorSharepointonlineDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorSlackDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorSlackDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["slack"]

    settings: ConnectorSlackDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorGitHubDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorGitHubDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["github"]

    settings: ConnectorGitHubDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorQuickbooksDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuth

    realm_id: str = FieldInfo(alias="realmId")
    """The realmId of your quickbooks company (e.g., 9341453474484455)"""


class ConnectorQuickbooksDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["quickbooks"]

    settings: ConnectorQuickbooksDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorGooglemailDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorGooglemailDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorGooglemailDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorGooglemailDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorGooglemailDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorGooglemailDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["googlemail"]

    settings: ConnectorGooglemailDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorNotionDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorNotionDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["notion"]

    settings: ConnectorNotionDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorLinkedinDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorLinkedinDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["linkedin"]

    settings: ConnectorLinkedinDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorGoogledocsDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorGoogledocsDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorGoogledocsDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorGoogledocsDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorGoogledocsDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorGoogledocsDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["googledocs"]

    settings: ConnectorGoogledocsDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorAircallDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorAircallDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["aircall"]

    settings: ConnectorAircallDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorGooglecalendarDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorGooglecalendarDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorGooglecalendarDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorGooglecalendarDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorGooglecalendarDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorGooglecalendarDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["googlecalendar"]

    settings: ConnectorGooglecalendarDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorGooglesheetDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorGooglesheetDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorGooglesheetDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorGooglesheetDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorGooglesheetDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorGooglesheetDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["googlesheet"]

    settings: ConnectorGooglesheetDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorDiscordDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorDiscordDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["discord"]

    settings: ConnectorDiscordDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorHubspotDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorHubspotDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["hubspot"]

    settings: ConnectorHubspotDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorSalesforceDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorSalesforceDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorSalesforceDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorSalesforceDiscriminatedConnectionSettingsSettings(BaseModel):
    instance_url: str
    """The instance URL of your Salesforce account (e.g., example)"""

    oauth: ConnectorSalesforceDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorSalesforceDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["salesforce"]

    settings: ConnectorSalesforceDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorLinearDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorLinearDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["linear"]

    settings: ConnectorLinearDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorConfluenceDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorConfluenceDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["confluence"]

    settings: ConnectorConfluenceDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorGoogledriveDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    access_token: str

    client_id: str
    """Client ID used for the connection"""

    raw: Dict[str, object]

    scope: str

    expires_at: Optional[str] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    token_type: Optional[str] = None


class ConnectorGoogledriveDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    created_at: Optional[str] = None

    credentials: Optional[ConnectorGoogledriveDiscriminatedConnectionSettingsSettingsOAuthCredentials] = None
    """Output of the postConnect hook for oauth2 connectors"""

    last_fetched_at: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None

    updated_at: Optional[str] = None


class ConnectorGoogledriveDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorGoogledriveDiscriminatedConnectionSettingsSettingsOAuth


class ConnectorGoogledriveDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["googledrive"]

    settings: ConnectorGoogledriveDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorAirtableDiscriminatedConnectionSettingsSettings(BaseModel):
    airtable_base: str = FieldInfo(alias="airtableBase")

    api_key: str = FieldInfo(alias="apiKey")


class ConnectorAirtableDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["airtable"]

    settings: ConnectorAirtableDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorApolloDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorApolloDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorApolloDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorApolloDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["apollo"]

    settings: ConnectorApolloDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorBrexDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")


class ConnectorBrexDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["brex"]

    settings: ConnectorBrexDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorCodaDiscriminatedConnectionSettingsSettings(BaseModel):
    api_key: str = FieldInfo(alias="apiKey")


class ConnectorCodaDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["coda"]

    settings: ConnectorCodaDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorFacebookDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorFacebookDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorFacebookDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorFacebookDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["facebook"]

    settings: ConnectorFacebookDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorFinchDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str


class ConnectorFinchDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["finch"]

    settings: ConnectorFinchDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccount(BaseModel):
    project_id: str

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0(BaseModel):
    role: Literal["admin"]

    service_account: ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0ServiceAccount = FieldInfo(
        alias="serviceAccount"
    )


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJson(BaseModel):
    app_name: str = FieldInfo(alias="appName")

    sts_token_manager: Dict[str, object] = FieldInfo(alias="stsTokenManager")

    uid: str

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0(BaseModel):
    method: Literal["userJson"]

    user_json: ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0UserJson = (
        FieldInfo(alias="userJson")
    )


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember1(BaseModel):
    custom_token: str = FieldInfo(alias="customToken")

    method: Literal["customToken"]


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember2(BaseModel):
    email: str

    method: Literal["emailPassword"]

    password: str


ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthData: TypeAlias = Union[
    ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember0,
    ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember1,
    ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthDataUnionMember2,
]


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1FirebaseConfig(BaseModel):
    api_key: str = FieldInfo(alias="apiKey")

    app_id: str = FieldInfo(alias="appId")

    auth_domain: str = FieldInfo(alias="authDomain")

    database_url: str = FieldInfo(alias="databaseURL")

    project_id: str = FieldInfo(alias="projectId")

    measurement_id: Optional[str] = FieldInfo(alias="measurementId", default=None)

    messaging_sender_id: Optional[str] = FieldInfo(alias="messagingSenderId", default=None)

    storage_bucket: Optional[str] = FieldInfo(alias="storageBucket", default=None)


class ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1(BaseModel):
    auth_data: ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1AuthData = FieldInfo(
        alias="authData"
    )

    firebase_config: ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1FirebaseConfig = FieldInfo(
        alias="firebaseConfig"
    )

    role: Literal["user"]


ConnectorFirebaseDiscriminatedConnectionSettingsSettings: TypeAlias = Union[
    ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember0,
    ConnectorFirebaseDiscriminatedConnectionSettingsSettingsUnionMember1,
]


class ConnectorFirebaseDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["firebase"]

    settings: ConnectorFirebaseDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorForeceiptDiscriminatedConnectionSettingsSettings(BaseModel):
    env_name: Literal["staging", "production"] = FieldInfo(alias="envName")

    api_id: Optional[object] = FieldInfo(alias="_id", default=None)

    credentials: Optional[object] = None


class ConnectorForeceiptDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["foreceipt"]

    settings: ConnectorForeceiptDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorGongDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorGongDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorGongDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorGongDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorGongDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorGongDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["gong"]

    settings: ConnectorGongDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorGreenhouseDiscriminatedConnectionSettingsSettings(BaseModel):
    api_key: str = FieldInfo(alias="apiKey")


class ConnectorGreenhouseDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["greenhouse"]

    settings: ConnectorGreenhouseDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorHeronDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["heron"]

    settings: object

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorInstagramDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorInstagramDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorInstagramDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorInstagramDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["instagram"]

    settings: ConnectorInstagramDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorIntercomDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorIntercomDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorIntercomDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorIntercomDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["intercom"]

    settings: ConnectorIntercomDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorJiraDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorJiraDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorJiraDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorJiraDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["jira"]

    settings: ConnectorJiraDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorKustomerDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorKustomerDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorKustomerDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorKustomerDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["kustomer"]

    settings: ConnectorKustomerDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorLeverDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorLeverDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorLeverDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorLeverDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["lever"]

    settings: ConnectorLeverDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorLunchmoneyDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["lunchmoney"]

    settings: object

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorMercuryDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["mercury"]

    settings: object

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorMergeDiscriminatedConnectionSettingsSettings(BaseModel):
    account_token: str = FieldInfo(alias="accountToken")

    account_details: Optional[object] = FieldInfo(alias="accountDetails", default=None)


class ConnectorMergeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["merge"]

    settings: ConnectorMergeDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorMicrosoftDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuth

    client_id: Optional[str] = None

    error: Optional[ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorMicrosoftDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["microsoft"]

    settings: ConnectorMicrosoftDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorMootaDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["moota"]

    settings: object

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorOnebrickDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")


class ConnectorOnebrickDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["onebrick"]

    settings: ConnectorOnebrickDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorOutreachDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorOutreachDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorOutreachDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorOutreachDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["outreach"]

    settings: ConnectorOutreachDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorPipedriveDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorPipedriveDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorPipedriveDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorPipedriveDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["pipedrive"]

    settings: ConnectorPipedriveDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorPlaidDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")

    institution: Optional[object] = None

    item: Optional[object] = None

    item_id: Optional[str] = FieldInfo(alias="itemId", default=None)

    status: Optional[object] = None

    webhook_item_error: None = FieldInfo(alias="webhookItemError", default=None)


class ConnectorPlaidDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["plaid"]

    settings: ConnectorPlaidDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorPostgresDiscriminatedConnectionSettingsSettingsSourceQueries(BaseModel):
    invoice: Optional[str] = None
    """Should order by lastModifiedAt and id descending"""


class ConnectorPostgresDiscriminatedConnectionSettingsSettings(BaseModel):
    database_url: str = FieldInfo(alias="databaseUrl")

    source_queries: Optional[ConnectorPostgresDiscriminatedConnectionSettingsSettingsSourceQueries] = FieldInfo(
        alias="sourceQueries", default=None
    )


class ConnectorPostgresDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["postgres"]

    settings: ConnectorPostgresDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorRampDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: Optional[str] = FieldInfo(alias="accessToken", default=None)

    start_after_transaction_id: Optional[str] = FieldInfo(alias="startAfterTransactionId", default=None)


class ConnectorRampDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["ramp"]

    settings: ConnectorRampDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorRedditDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorRedditDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorRedditDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorRedditDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["reddit"]

    settings: ConnectorRedditDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorSalesloftDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorSalesloftDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorSalesloftDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorSalesloftDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["salesloft"]

    settings: ConnectorSalesloftDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorSaltedgeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["saltedge"]

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    settings: Optional[object] = None

    updated_at: Optional[str] = None


class ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserNotifications(BaseModel):
    added_as_friend: bool

    added_to_group: bool

    announcements: bool

    bills: bool

    expense_added: bool

    expense_updated: bool

    monthly_summary: bool

    payments: bool


class ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserPicture(BaseModel):
    large: Optional[str] = None

    medium: Optional[str] = None

    original: Optional[str] = None

    small: Optional[str] = None

    xlarge: Optional[str] = None

    xxlarge: Optional[str] = None


class ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUser(BaseModel):
    id: float

    country_code: str

    custom_picture: bool

    date_format: str

    default_currency: str

    default_group_id: float

    email: str

    first_name: str

    force_refresh_at: str

    last_name: str

    locale: str

    notifications: ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserNotifications

    notifications_count: float

    notifications_read: str

    picture: ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserPicture

    registration_status: str


class ConnectorSplitwiseDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")

    current_user: Optional[ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUser] = FieldInfo(
        alias="currentUser", default=None
    )


class ConnectorSplitwiseDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["splitwise"]

    settings: ConnectorSplitwiseDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorStripeDiscriminatedConnectionSettingsSettings(BaseModel):
    secret_key: str = FieldInfo(alias="secretKey")


class ConnectorStripeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["stripe"]

    settings: ConnectorStripeDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorTellerDiscriminatedConnectionSettingsSettings(BaseModel):
    token: str


class ConnectorTellerDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["teller"]

    settings: ConnectorTellerDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorTogglDiscriminatedConnectionSettingsSettings(BaseModel):
    api_token: str = FieldInfo(alias="apiToken")

    email: Optional[str] = None

    password: Optional[str] = None


class ConnectorTogglDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["toggl"]

    settings: ConnectorTogglDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorTwentyDiscriminatedConnectionSettingsSettings(BaseModel):
    access_token: str


class ConnectorTwentyDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["twenty"]

    settings: ConnectorTwentyDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorTwitterDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorTwitterDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorTwitterDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorTwitterDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["twitter"]

    settings: ConnectorTwitterDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorVenmoDiscriminatedConnectionSettingsSettings(BaseModel):
    credentials: Optional[object] = None

    me: Optional[object] = None


class ConnectorVenmoDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["venmo"]

    settings: ConnectorVenmoDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorWiseDiscriminatedConnectionSettingsSettings(BaseModel):
    env_name: Literal["sandbox", "live"] = FieldInfo(alias="envName")

    api_token: Optional[str] = FieldInfo(alias="apiToken", default=None)


class ConnectorWiseDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["wise"]

    settings: ConnectorWiseDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorXeroDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorXeroDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorXeroDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorXeroDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["xero"]

    settings: ConnectorXeroDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorYodleeDiscriminatedConnectionSettingsSettingsAccessToken(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")

    expires_in: float = FieldInfo(alias="expiresIn")

    issued_at: str = FieldInfo(alias="issuedAt")


class ConnectorYodleeDiscriminatedConnectionSettingsSettingsProviderAccount(BaseModel):
    id: float

    aggregation_source: str = FieldInfo(alias="aggregationSource")

    created_date: str = FieldInfo(alias="createdDate")

    dataset: List[object]

    is_manual: bool = FieldInfo(alias="isManual")

    provider_id: float = FieldInfo(alias="providerId")

    status: Literal["LOGIN_IN_PROGRESS", "USER_INPUT_REQUIRED", "IN_PROGRESS", "PARTIAL_SUCCESS", "SUCCESS", "FAILED"]

    is_deleted: Optional[bool] = FieldInfo(alias="isDeleted", default=None)


class ConnectorYodleeDiscriminatedConnectionSettingsSettings(BaseModel):
    login_name: str = FieldInfo(alias="loginName")

    provider_account_id: Union[float, str] = FieldInfo(alias="providerAccountId")

    access_token: Optional[ConnectorYodleeDiscriminatedConnectionSettingsSettingsAccessToken] = FieldInfo(
        alias="accessToken", default=None
    )

    provider: None = None

    provider_account: Optional[ConnectorYodleeDiscriminatedConnectionSettingsSettingsProviderAccount] = FieldInfo(
        alias="providerAccount", default=None
    )

    user: None = None


class ConnectorYodleeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["yodlee"]

    settings: ConnectorYodleeDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


class ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw(BaseModel):
    access_token: str

    expires_at: Optional[datetime] = None

    expires_in: Optional[float] = None

    refresh_token: Optional[str] = None

    refresh_token_expires_in: Optional[float] = None

    scope: Optional[str] = None

    token_type: Optional[str] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentials(BaseModel):
    raw: ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw

    type: Literal["OAUTH2", "OAUTH1", "BASIC", "API_KEY"]

    access_token: Optional[str] = None

    api_key: Optional[str] = None

    expires_at: Optional[datetime] = None

    refresh_token: Optional[str] = None


class ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig(BaseModel):
    instance_url: Optional[str] = None

    portal_id: Optional[float] = FieldInfo(alias="portalId", default=None)

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...


class ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuth(BaseModel):
    credentials: ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentials

    metadata: Optional[Dict[str, object]] = None

    connection_config: Optional[ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig] = None


class ConnectorZohodeskDiscriminatedConnectionSettingsSettingsError(BaseModel):
    code: Union[Literal["refresh_token_external_error"], str]

    message: Optional[str] = None


class ConnectorZohodeskDiscriminatedConnectionSettingsSettings(BaseModel):
    oauth: ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuth

    error: Optional[ConnectorZohodeskDiscriminatedConnectionSettingsSettingsError] = None


class ConnectorZohodeskDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["zohodesk"]

    settings: ConnectorZohodeskDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector_config_id: Optional[str] = None

    created_at: Optional[str] = None

    customer_id: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integration_id: Optional[str] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    updated_at: Optional[str] = None


CreateConnectionResponse: TypeAlias = Union[
    ConnectorDummyOauth2DiscriminatedConnectionSettings,
    ConnectorSharepointonlineDiscriminatedConnectionSettings,
    ConnectorSlackDiscriminatedConnectionSettings,
    ConnectorGitHubDiscriminatedConnectionSettings,
    ConnectorQuickbooksDiscriminatedConnectionSettings,
    ConnectorGooglemailDiscriminatedConnectionSettings,
    ConnectorNotionDiscriminatedConnectionSettings,
    ConnectorLinkedinDiscriminatedConnectionSettings,
    ConnectorGoogledocsDiscriminatedConnectionSettings,
    ConnectorAircallDiscriminatedConnectionSettings,
    ConnectorGooglecalendarDiscriminatedConnectionSettings,
    ConnectorGooglesheetDiscriminatedConnectionSettings,
    ConnectorDiscordDiscriminatedConnectionSettings,
    ConnectorHubspotDiscriminatedConnectionSettings,
    ConnectorSalesforceDiscriminatedConnectionSettings,
    ConnectorLinearDiscriminatedConnectionSettings,
    ConnectorConfluenceDiscriminatedConnectionSettings,
    ConnectorGoogledriveDiscriminatedConnectionSettings,
    ConnectorAirtableDiscriminatedConnectionSettings,
    ConnectorApolloDiscriminatedConnectionSettings,
    ConnectorBrexDiscriminatedConnectionSettings,
    ConnectorCodaDiscriminatedConnectionSettings,
    ConnectorFacebookDiscriminatedConnectionSettings,
    ConnectorFinchDiscriminatedConnectionSettings,
    ConnectorFirebaseDiscriminatedConnectionSettings,
    ConnectorForeceiptDiscriminatedConnectionSettings,
    ConnectorGongDiscriminatedConnectionSettings,
    ConnectorGreenhouseDiscriminatedConnectionSettings,
    ConnectorHeronDiscriminatedConnectionSettings,
    ConnectorInstagramDiscriminatedConnectionSettings,
    ConnectorIntercomDiscriminatedConnectionSettings,
    ConnectorJiraDiscriminatedConnectionSettings,
    ConnectorKustomerDiscriminatedConnectionSettings,
    ConnectorLeverDiscriminatedConnectionSettings,
    ConnectorLunchmoneyDiscriminatedConnectionSettings,
    ConnectorMercuryDiscriminatedConnectionSettings,
    ConnectorMergeDiscriminatedConnectionSettings,
    ConnectorMicrosoftDiscriminatedConnectionSettings,
    ConnectorMootaDiscriminatedConnectionSettings,
    ConnectorOnebrickDiscriminatedConnectionSettings,
    ConnectorOutreachDiscriminatedConnectionSettings,
    ConnectorPipedriveDiscriminatedConnectionSettings,
    ConnectorPlaidDiscriminatedConnectionSettings,
    ConnectorPostgresDiscriminatedConnectionSettings,
    ConnectorRampDiscriminatedConnectionSettings,
    ConnectorRedditDiscriminatedConnectionSettings,
    ConnectorSalesloftDiscriminatedConnectionSettings,
    ConnectorSaltedgeDiscriminatedConnectionSettings,
    ConnectorSplitwiseDiscriminatedConnectionSettings,
    ConnectorStripeDiscriminatedConnectionSettings,
    ConnectorTellerDiscriminatedConnectionSettings,
    ConnectorTogglDiscriminatedConnectionSettings,
    ConnectorTwentyDiscriminatedConnectionSettings,
    ConnectorTwitterDiscriminatedConnectionSettings,
    ConnectorVenmoDiscriminatedConnectionSettings,
    ConnectorWiseDiscriminatedConnectionSettings,
    ConnectorXeroDiscriminatedConnectionSettings,
    ConnectorYodleeDiscriminatedConnectionSettings,
    ConnectorZohodeskDiscriminatedConnectionSettings,
]
