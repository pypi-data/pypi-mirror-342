# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "GetConnectionResponse",
    "ConnectorDummyOauth2DiscriminatedConnectionSettings",
    "ConnectorDummyOauth2DiscriminatedConnectionSettingsSettings",
    "ConnectorDummyOauth2DiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorDummyOauth2DiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorDummyOauth2DiscriminatedConnectionSettingsConnector",
    "ConnectorDummyOauth2DiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorDummyOauth2DiscriminatedConnectionSettingsConnectorScope",
    "ConnectorSharepointonlineDiscriminatedConnectionSettings",
    "ConnectorSharepointonlineDiscriminatedConnectionSettingsSettings",
    "ConnectorSharepointonlineDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorSharepointonlineDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorSharepointonlineDiscriminatedConnectionSettingsConnector",
    "ConnectorSharepointonlineDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorSharepointonlineDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorSlackDiscriminatedConnectionSettings",
    "ConnectorSlackDiscriminatedConnectionSettingsSettings",
    "ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorSlackDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorSlackDiscriminatedConnectionSettingsConnector",
    "ConnectorSlackDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorSlackDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGitHubDiscriminatedConnectionSettings",
    "ConnectorGitHubDiscriminatedConnectionSettingsSettings",
    "ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGitHubDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGitHubDiscriminatedConnectionSettingsConnector",
    "ConnectorGitHubDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGitHubDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorQuickbooksDiscriminatedConnectionSettings",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsSettings",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsConnector",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorQuickbooksDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGooglemailDiscriminatedConnectionSettings",
    "ConnectorGooglemailDiscriminatedConnectionSettingsSettings",
    "ConnectorGooglemailDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGooglemailDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGooglemailDiscriminatedConnectionSettingsConnector",
    "ConnectorGooglemailDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGooglemailDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorNotionDiscriminatedConnectionSettings",
    "ConnectorNotionDiscriminatedConnectionSettingsSettings",
    "ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorNotionDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorNotionDiscriminatedConnectionSettingsConnector",
    "ConnectorNotionDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorNotionDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorLinkedinDiscriminatedConnectionSettings",
    "ConnectorLinkedinDiscriminatedConnectionSettingsSettings",
    "ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorLinkedinDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorLinkedinDiscriminatedConnectionSettingsConnector",
    "ConnectorLinkedinDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorLinkedinDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGoogledocsDiscriminatedConnectionSettings",
    "ConnectorGoogledocsDiscriminatedConnectionSettingsSettings",
    "ConnectorGoogledocsDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGoogledocsDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGoogledocsDiscriminatedConnectionSettingsConnector",
    "ConnectorGoogledocsDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGoogledocsDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorAircallDiscriminatedConnectionSettings",
    "ConnectorAircallDiscriminatedConnectionSettingsSettings",
    "ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorAircallDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorAircallDiscriminatedConnectionSettingsConnector",
    "ConnectorAircallDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorAircallDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGooglecalendarDiscriminatedConnectionSettings",
    "ConnectorGooglecalendarDiscriminatedConnectionSettingsSettings",
    "ConnectorGooglecalendarDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGooglecalendarDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGooglecalendarDiscriminatedConnectionSettingsConnector",
    "ConnectorGooglecalendarDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGooglecalendarDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGooglesheetDiscriminatedConnectionSettings",
    "ConnectorGooglesheetDiscriminatedConnectionSettingsSettings",
    "ConnectorGooglesheetDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGooglesheetDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGooglesheetDiscriminatedConnectionSettingsConnector",
    "ConnectorGooglesheetDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGooglesheetDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorDiscordDiscriminatedConnectionSettings",
    "ConnectorDiscordDiscriminatedConnectionSettingsSettings",
    "ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorDiscordDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorDiscordDiscriminatedConnectionSettingsConnector",
    "ConnectorDiscordDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorDiscordDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorHubspotDiscriminatedConnectionSettings",
    "ConnectorHubspotDiscriminatedConnectionSettingsSettings",
    "ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorHubspotDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorHubspotDiscriminatedConnectionSettingsConnector",
    "ConnectorHubspotDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorHubspotDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorSalesforceDiscriminatedConnectionSettings",
    "ConnectorSalesforceDiscriminatedConnectionSettingsSettings",
    "ConnectorSalesforceDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorSalesforceDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorSalesforceDiscriminatedConnectionSettingsConnector",
    "ConnectorSalesforceDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorSalesforceDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorLinearDiscriminatedConnectionSettings",
    "ConnectorLinearDiscriminatedConnectionSettingsSettings",
    "ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorLinearDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorLinearDiscriminatedConnectionSettingsConnector",
    "ConnectorLinearDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorLinearDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorConfluenceDiscriminatedConnectionSettings",
    "ConnectorConfluenceDiscriminatedConnectionSettingsSettings",
    "ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorConfluenceDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorConfluenceDiscriminatedConnectionSettingsConnector",
    "ConnectorConfluenceDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorConfluenceDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGoogledriveDiscriminatedConnectionSettings",
    "ConnectorGoogledriveDiscriminatedConnectionSettingsSettings",
    "ConnectorGoogledriveDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGoogledriveDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGoogledriveDiscriminatedConnectionSettingsConnector",
    "ConnectorGoogledriveDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGoogledriveDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorAirtableDiscriminatedConnectionSettings",
    "ConnectorAirtableDiscriminatedConnectionSettingsSettings",
    "ConnectorAirtableDiscriminatedConnectionSettingsConnector",
    "ConnectorAirtableDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorAirtableDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorApolloDiscriminatedConnectionSettings",
    "ConnectorApolloDiscriminatedConnectionSettingsSettings",
    "ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorApolloDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorApolloDiscriminatedConnectionSettingsSettingsError",
    "ConnectorApolloDiscriminatedConnectionSettingsConnector",
    "ConnectorApolloDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorApolloDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorBrexDiscriminatedConnectionSettings",
    "ConnectorBrexDiscriminatedConnectionSettingsSettings",
    "ConnectorBrexDiscriminatedConnectionSettingsConnector",
    "ConnectorBrexDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorBrexDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorCodaDiscriminatedConnectionSettings",
    "ConnectorCodaDiscriminatedConnectionSettingsSettings",
    "ConnectorCodaDiscriminatedConnectionSettingsConnector",
    "ConnectorCodaDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorCodaDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorFacebookDiscriminatedConnectionSettings",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettings",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorFacebookDiscriminatedConnectionSettingsSettingsError",
    "ConnectorFacebookDiscriminatedConnectionSettingsConnector",
    "ConnectorFacebookDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorFacebookDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorFinchDiscriminatedConnectionSettings",
    "ConnectorFinchDiscriminatedConnectionSettingsSettings",
    "ConnectorFinchDiscriminatedConnectionSettingsConnector",
    "ConnectorFinchDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorFinchDiscriminatedConnectionSettingsConnectorScope",
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
    "ConnectorFirebaseDiscriminatedConnectionSettingsConnector",
    "ConnectorFirebaseDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorFirebaseDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorForeceiptDiscriminatedConnectionSettings",
    "ConnectorForeceiptDiscriminatedConnectionSettingsSettings",
    "ConnectorForeceiptDiscriminatedConnectionSettingsConnector",
    "ConnectorForeceiptDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorForeceiptDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGongDiscriminatedConnectionSettings",
    "ConnectorGongDiscriminatedConnectionSettingsSettings",
    "ConnectorGongDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorGongDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorGongDiscriminatedConnectionSettingsSettingsError",
    "ConnectorGongDiscriminatedConnectionSettingsConnector",
    "ConnectorGongDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGongDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorGreenhouseDiscriminatedConnectionSettings",
    "ConnectorGreenhouseDiscriminatedConnectionSettingsSettings",
    "ConnectorGreenhouseDiscriminatedConnectionSettingsConnector",
    "ConnectorGreenhouseDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorGreenhouseDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorHeronDiscriminatedConnectionSettings",
    "ConnectorHeronDiscriminatedConnectionSettingsConnector",
    "ConnectorHeronDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorHeronDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorInstagramDiscriminatedConnectionSettings",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettings",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorInstagramDiscriminatedConnectionSettingsSettingsError",
    "ConnectorInstagramDiscriminatedConnectionSettingsConnector",
    "ConnectorInstagramDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorInstagramDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorIntercomDiscriminatedConnectionSettings",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettings",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorIntercomDiscriminatedConnectionSettingsSettingsError",
    "ConnectorIntercomDiscriminatedConnectionSettingsConnector",
    "ConnectorIntercomDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorIntercomDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorJiraDiscriminatedConnectionSettings",
    "ConnectorJiraDiscriminatedConnectionSettingsSettings",
    "ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorJiraDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorJiraDiscriminatedConnectionSettingsSettingsError",
    "ConnectorJiraDiscriminatedConnectionSettingsConnector",
    "ConnectorJiraDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorJiraDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorKustomerDiscriminatedConnectionSettings",
    "ConnectorKustomerDiscriminatedConnectionSettingsSettings",
    "ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorKustomerDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorKustomerDiscriminatedConnectionSettingsSettingsError",
    "ConnectorKustomerDiscriminatedConnectionSettingsConnector",
    "ConnectorKustomerDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorKustomerDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorLeverDiscriminatedConnectionSettings",
    "ConnectorLeverDiscriminatedConnectionSettingsSettings",
    "ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorLeverDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorLeverDiscriminatedConnectionSettingsSettingsError",
    "ConnectorLeverDiscriminatedConnectionSettingsConnector",
    "ConnectorLeverDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorLeverDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorLunchmoneyDiscriminatedConnectionSettings",
    "ConnectorLunchmoneyDiscriminatedConnectionSettingsConnector",
    "ConnectorLunchmoneyDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorLunchmoneyDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorMercuryDiscriminatedConnectionSettings",
    "ConnectorMercuryDiscriminatedConnectionSettingsConnector",
    "ConnectorMercuryDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorMercuryDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorMergeDiscriminatedConnectionSettings",
    "ConnectorMergeDiscriminatedConnectionSettingsSettings",
    "ConnectorMergeDiscriminatedConnectionSettingsConnector",
    "ConnectorMergeDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorMergeDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorMicrosoftDiscriminatedConnectionSettings",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsSettings",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsSettingsError",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsConnector",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorMicrosoftDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorMootaDiscriminatedConnectionSettings",
    "ConnectorMootaDiscriminatedConnectionSettingsConnector",
    "ConnectorMootaDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorMootaDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorOnebrickDiscriminatedConnectionSettings",
    "ConnectorOnebrickDiscriminatedConnectionSettingsSettings",
    "ConnectorOnebrickDiscriminatedConnectionSettingsConnector",
    "ConnectorOnebrickDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorOnebrickDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorOutreachDiscriminatedConnectionSettings",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettings",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorOutreachDiscriminatedConnectionSettingsSettingsError",
    "ConnectorOutreachDiscriminatedConnectionSettingsConnector",
    "ConnectorOutreachDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorOutreachDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorPipedriveDiscriminatedConnectionSettings",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettings",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorPipedriveDiscriminatedConnectionSettingsSettingsError",
    "ConnectorPipedriveDiscriminatedConnectionSettingsConnector",
    "ConnectorPipedriveDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorPipedriveDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorPlaidDiscriminatedConnectionSettings",
    "ConnectorPlaidDiscriminatedConnectionSettingsSettings",
    "ConnectorPlaidDiscriminatedConnectionSettingsConnector",
    "ConnectorPlaidDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorPlaidDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorPostgresDiscriminatedConnectionSettings",
    "ConnectorPostgresDiscriminatedConnectionSettingsSettings",
    "ConnectorPostgresDiscriminatedConnectionSettingsSettingsSourceQueries",
    "ConnectorPostgresDiscriminatedConnectionSettingsConnector",
    "ConnectorPostgresDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorPostgresDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorRampDiscriminatedConnectionSettings",
    "ConnectorRampDiscriminatedConnectionSettingsSettings",
    "ConnectorRampDiscriminatedConnectionSettingsConnector",
    "ConnectorRampDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorRampDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorRedditDiscriminatedConnectionSettings",
    "ConnectorRedditDiscriminatedConnectionSettingsSettings",
    "ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorRedditDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorRedditDiscriminatedConnectionSettingsSettingsError",
    "ConnectorRedditDiscriminatedConnectionSettingsConnector",
    "ConnectorRedditDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorRedditDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorSalesloftDiscriminatedConnectionSettings",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettings",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorSalesloftDiscriminatedConnectionSettingsSettingsError",
    "ConnectorSalesloftDiscriminatedConnectionSettingsConnector",
    "ConnectorSalesloftDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorSalesloftDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorSaltedgeDiscriminatedConnectionSettings",
    "ConnectorSaltedgeDiscriminatedConnectionSettingsConnector",
    "ConnectorSaltedgeDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorSaltedgeDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorSplitwiseDiscriminatedConnectionSettings",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettings",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUser",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserNotifications",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsSettingsCurrentUserPicture",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsConnector",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorSplitwiseDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorStripeDiscriminatedConnectionSettings",
    "ConnectorStripeDiscriminatedConnectionSettingsSettings",
    "ConnectorStripeDiscriminatedConnectionSettingsConnector",
    "ConnectorStripeDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorStripeDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorTellerDiscriminatedConnectionSettings",
    "ConnectorTellerDiscriminatedConnectionSettingsSettings",
    "ConnectorTellerDiscriminatedConnectionSettingsConnector",
    "ConnectorTellerDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorTellerDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorTogglDiscriminatedConnectionSettings",
    "ConnectorTogglDiscriminatedConnectionSettingsSettings",
    "ConnectorTogglDiscriminatedConnectionSettingsConnector",
    "ConnectorTogglDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorTogglDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorTwentyDiscriminatedConnectionSettings",
    "ConnectorTwentyDiscriminatedConnectionSettingsSettings",
    "ConnectorTwentyDiscriminatedConnectionSettingsConnector",
    "ConnectorTwentyDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorTwentyDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorTwitterDiscriminatedConnectionSettings",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettings",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorTwitterDiscriminatedConnectionSettingsSettingsError",
    "ConnectorTwitterDiscriminatedConnectionSettingsConnector",
    "ConnectorTwitterDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorTwitterDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorVenmoDiscriminatedConnectionSettings",
    "ConnectorVenmoDiscriminatedConnectionSettingsSettings",
    "ConnectorVenmoDiscriminatedConnectionSettingsConnector",
    "ConnectorVenmoDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorVenmoDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorWiseDiscriminatedConnectionSettings",
    "ConnectorWiseDiscriminatedConnectionSettingsSettings",
    "ConnectorWiseDiscriminatedConnectionSettingsConnector",
    "ConnectorWiseDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorWiseDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorXeroDiscriminatedConnectionSettings",
    "ConnectorXeroDiscriminatedConnectionSettingsSettings",
    "ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorXeroDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorXeroDiscriminatedConnectionSettingsSettingsError",
    "ConnectorXeroDiscriminatedConnectionSettingsConnector",
    "ConnectorXeroDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorXeroDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorYodleeDiscriminatedConnectionSettings",
    "ConnectorYodleeDiscriminatedConnectionSettingsSettings",
    "ConnectorYodleeDiscriminatedConnectionSettingsSettingsAccessToken",
    "ConnectorYodleeDiscriminatedConnectionSettingsSettingsProviderAccount",
    "ConnectorYodleeDiscriminatedConnectionSettingsConnector",
    "ConnectorYodleeDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorYodleeDiscriminatedConnectionSettingsConnectorScope",
    "ConnectorZohodeskDiscriminatedConnectionSettings",
    "ConnectorZohodeskDiscriminatedConnectionSettingsSettings",
    "ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuth",
    "ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentials",
    "ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthCredentialsRaw",
    "ConnectorZohodeskDiscriminatedConnectionSettingsSettingsOAuthConnectionConfig",
    "ConnectorZohodeskDiscriminatedConnectionSettingsSettingsError",
    "ConnectorZohodeskDiscriminatedConnectionSettingsConnector",
    "ConnectorZohodeskDiscriminatedConnectionSettingsConnectorSchemas",
    "ConnectorZohodeskDiscriminatedConnectionSettingsConnectorScope",
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


class ConnectorDummyOauth2DiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorDummyOauth2DiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorDummyOauth2DiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorDummyOauth2DiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorDummyOauth2DiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorDummyOauth2DiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["dummy-oauth2"]

    settings: ConnectorDummyOauth2DiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorDummyOauth2DiscriminatedConnectionSettingsConnector] = None

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


class ConnectorSharepointonlineDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSharepointonlineDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSharepointonlineDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSharepointonlineDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorSharepointonlineDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSharepointonlineDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["sharepointonline"]

    settings: ConnectorSharepointonlineDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorSharepointonlineDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorSlackDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSlackDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSlackDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSlackDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorSlackDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSlackDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["slack"]

    settings: ConnectorSlackDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorSlackDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorGitHubDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGitHubDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGitHubDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGitHubDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGitHubDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGitHubDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["github"]

    settings: ConnectorGitHubDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorGitHubDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorQuickbooksDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorQuickbooksDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorQuickbooksDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorQuickbooksDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorQuickbooksDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorQuickbooksDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["quickbooks"]

    settings: ConnectorQuickbooksDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorQuickbooksDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorGooglemailDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGooglemailDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGooglemailDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGooglemailDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGooglemailDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGooglemailDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["googlemail"]

    settings: ConnectorGooglemailDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorGooglemailDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorNotionDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorNotionDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorNotionDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorNotionDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorNotionDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorNotionDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["notion"]

    settings: ConnectorNotionDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorNotionDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorLinkedinDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLinkedinDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLinkedinDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLinkedinDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorLinkedinDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLinkedinDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["linkedin"]

    settings: ConnectorLinkedinDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorLinkedinDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorGoogledocsDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGoogledocsDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGoogledocsDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGoogledocsDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGoogledocsDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGoogledocsDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["googledocs"]

    settings: ConnectorGoogledocsDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorGoogledocsDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorAircallDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorAircallDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorAircallDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorAircallDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorAircallDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorAircallDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["aircall"]

    settings: ConnectorAircallDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorAircallDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorGooglecalendarDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGooglecalendarDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGooglecalendarDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGooglecalendarDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGooglecalendarDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGooglecalendarDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["googlecalendar"]

    settings: ConnectorGooglecalendarDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorGooglecalendarDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorGooglesheetDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGooglesheetDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGooglesheetDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGooglesheetDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGooglesheetDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGooglesheetDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["googlesheet"]

    settings: ConnectorGooglesheetDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorGooglesheetDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorDiscordDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorDiscordDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorDiscordDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorDiscordDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorDiscordDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorDiscordDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["discord"]

    settings: ConnectorDiscordDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorDiscordDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorHubspotDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorHubspotDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorHubspotDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorHubspotDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorHubspotDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorHubspotDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["hubspot"]

    settings: ConnectorHubspotDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorHubspotDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorSalesforceDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSalesforceDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSalesforceDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSalesforceDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorSalesforceDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSalesforceDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["salesforce"]

    settings: ConnectorSalesforceDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorSalesforceDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorLinearDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLinearDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLinearDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLinearDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorLinearDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLinearDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["linear"]

    settings: ConnectorLinearDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorLinearDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorConfluenceDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorConfluenceDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorConfluenceDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorConfluenceDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorConfluenceDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorConfluenceDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["confluence"]

    settings: ConnectorConfluenceDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorConfluenceDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorGoogledriveDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGoogledriveDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGoogledriveDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGoogledriveDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGoogledriveDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGoogledriveDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["googledrive"]

    settings: ConnectorGoogledriveDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorGoogledriveDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorAirtableDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorAirtableDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorAirtableDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorAirtableDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorAirtableDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorAirtableDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["airtable"]

    settings: ConnectorAirtableDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorAirtableDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorApolloDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorApolloDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorApolloDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorApolloDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorApolloDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorApolloDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["apollo"]

    settings: ConnectorApolloDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorApolloDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorBrexDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorBrexDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorBrexDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorBrexDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorBrexDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorBrexDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["brex"]

    settings: ConnectorBrexDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorBrexDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorCodaDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorCodaDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorCodaDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorCodaDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorCodaDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorCodaDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["coda"]

    settings: ConnectorCodaDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorCodaDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorFacebookDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorFacebookDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorFacebookDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorFacebookDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorFacebookDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorFacebookDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["facebook"]

    settings: ConnectorFacebookDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorFacebookDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorFinchDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorFinchDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorFinchDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorFinchDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorFinchDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorFinchDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["finch"]

    settings: ConnectorFinchDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorFinchDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorFirebaseDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorFirebaseDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorFirebaseDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorFirebaseDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorFirebaseDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorFirebaseDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["firebase"]

    settings: ConnectorFirebaseDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorFirebaseDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorForeceiptDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorForeceiptDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorForeceiptDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorForeceiptDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorForeceiptDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorForeceiptDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["foreceipt"]

    settings: ConnectorForeceiptDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorForeceiptDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorGongDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGongDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGongDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGongDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGongDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGongDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["gong"]

    settings: ConnectorGongDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorGongDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorGreenhouseDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGreenhouseDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGreenhouseDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGreenhouseDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorGreenhouseDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGreenhouseDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["greenhouse"]

    settings: ConnectorGreenhouseDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorGreenhouseDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorHeronDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorHeronDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorHeronDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorHeronDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorHeronDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorHeronDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["heron"]

    settings: object

    id: Optional[str] = None

    connector: Optional[ConnectorHeronDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorInstagramDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorInstagramDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorInstagramDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorInstagramDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorInstagramDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorInstagramDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["instagram"]

    settings: ConnectorInstagramDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorInstagramDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorIntercomDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorIntercomDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorIntercomDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorIntercomDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorIntercomDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorIntercomDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["intercom"]

    settings: ConnectorIntercomDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorIntercomDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorJiraDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorJiraDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorJiraDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorJiraDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorJiraDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorJiraDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["jira"]

    settings: ConnectorJiraDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorJiraDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorKustomerDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorKustomerDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorKustomerDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorKustomerDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorKustomerDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorKustomerDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["kustomer"]

    settings: ConnectorKustomerDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorKustomerDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorLeverDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLeverDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLeverDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLeverDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorLeverDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLeverDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["lever"]

    settings: ConnectorLeverDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorLeverDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorLunchmoneyDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLunchmoneyDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLunchmoneyDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLunchmoneyDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorLunchmoneyDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLunchmoneyDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["lunchmoney"]

    settings: object

    id: Optional[str] = None

    connector: Optional[ConnectorLunchmoneyDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorMercuryDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorMercuryDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorMercuryDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorMercuryDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorMercuryDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorMercuryDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["mercury"]

    settings: object

    id: Optional[str] = None

    connector: Optional[ConnectorMercuryDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorMergeDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorMergeDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorMergeDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorMergeDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorMergeDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorMergeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["merge"]

    settings: ConnectorMergeDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorMergeDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorMicrosoftDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorMicrosoftDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorMicrosoftDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorMicrosoftDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorMicrosoftDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorMicrosoftDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["microsoft"]

    settings: ConnectorMicrosoftDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorMicrosoftDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorMootaDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorMootaDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorMootaDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorMootaDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorMootaDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorMootaDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["moota"]

    settings: object

    id: Optional[str] = None

    connector: Optional[ConnectorMootaDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorOnebrickDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorOnebrickDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorOnebrickDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorOnebrickDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorOnebrickDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorOnebrickDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["onebrick"]

    settings: ConnectorOnebrickDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorOnebrickDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorOutreachDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorOutreachDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorOutreachDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorOutreachDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorOutreachDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorOutreachDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["outreach"]

    settings: ConnectorOutreachDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorOutreachDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorPipedriveDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorPipedriveDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorPipedriveDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorPipedriveDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorPipedriveDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorPipedriveDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["pipedrive"]

    settings: ConnectorPipedriveDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorPipedriveDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorPlaidDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorPlaidDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorPlaidDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorPlaidDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorPlaidDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorPlaidDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["plaid"]

    settings: ConnectorPlaidDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorPlaidDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorPostgresDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorPostgresDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorPostgresDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorPostgresDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorPostgresDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorPostgresDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["postgres"]

    settings: ConnectorPostgresDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorPostgresDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorRampDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorRampDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorRampDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorRampDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorRampDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorRampDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["ramp"]

    settings: ConnectorRampDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorRampDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorRedditDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorRedditDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorRedditDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorRedditDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorRedditDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorRedditDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["reddit"]

    settings: ConnectorRedditDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorRedditDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorSalesloftDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSalesloftDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSalesloftDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSalesloftDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorSalesloftDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSalesloftDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["salesloft"]

    settings: ConnectorSalesloftDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorSalesloftDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorSaltedgeDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSaltedgeDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSaltedgeDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSaltedgeDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorSaltedgeDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSaltedgeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["saltedge"]

    id: Optional[str] = None

    connector: Optional[ConnectorSaltedgeDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorSplitwiseDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSplitwiseDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSplitwiseDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSplitwiseDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorSplitwiseDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSplitwiseDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["splitwise"]

    settings: ConnectorSplitwiseDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorSplitwiseDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorStripeDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorStripeDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorStripeDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorStripeDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorStripeDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorStripeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["stripe"]

    settings: ConnectorStripeDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorStripeDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorTellerDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTellerDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTellerDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTellerDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorTellerDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTellerDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["teller"]

    settings: ConnectorTellerDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorTellerDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorTogglDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTogglDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTogglDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTogglDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorTogglDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTogglDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["toggl"]

    settings: ConnectorTogglDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorTogglDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorTwentyDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTwentyDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTwentyDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTwentyDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorTwentyDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTwentyDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["twenty"]

    settings: ConnectorTwentyDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorTwentyDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorTwitterDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTwitterDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTwitterDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTwitterDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorTwitterDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTwitterDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["twitter"]

    settings: ConnectorTwitterDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorTwitterDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorVenmoDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorVenmoDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorVenmoDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorVenmoDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorVenmoDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorVenmoDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["venmo"]

    settings: ConnectorVenmoDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorVenmoDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorWiseDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorWiseDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorWiseDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorWiseDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorWiseDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorWiseDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["wise"]

    settings: ConnectorWiseDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorWiseDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorXeroDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorXeroDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorXeroDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorXeroDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorXeroDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorXeroDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["xero"]

    settings: ConnectorXeroDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorXeroDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorYodleeDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorYodleeDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorYodleeDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorYodleeDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorYodleeDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorYodleeDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["yodlee"]

    settings: ConnectorYodleeDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorYodleeDiscriminatedConnectionSettingsConnector] = None

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


class ConnectorZohodeskDiscriminatedConnectionSettingsConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorZohodeskDiscriminatedConnectionSettingsConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorZohodeskDiscriminatedConnectionSettingsConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorZohodeskDiscriminatedConnectionSettingsConnectorSchemas] = None

    scopes: Optional[List[ConnectorZohodeskDiscriminatedConnectionSettingsConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorZohodeskDiscriminatedConnectionSettings(BaseModel):
    connector_name: Literal["zohodesk"]

    settings: ConnectorZohodeskDiscriminatedConnectionSettingsSettings

    id: Optional[str] = None

    connector: Optional[ConnectorZohodeskDiscriminatedConnectionSettingsConnector] = None

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


GetConnectionResponse: TypeAlias = Union[
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
