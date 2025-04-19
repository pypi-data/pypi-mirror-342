# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "ListConnectionConfigsResponse",
    "ConnectorDummyOauth2DiscriminatedConnectorConfig",
    "ConnectorDummyOauth2DiscriminatedConnectorConfigConfig",
    "ConnectorDummyOauth2DiscriminatedConnectorConfigConfigOAuth",
    "ConnectorDummyOauth2DiscriminatedConnectorConfigConnector",
    "ConnectorDummyOauth2DiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorDummyOauth2DiscriminatedConnectorConfigConnectorScope",
    "ConnectorDummyOauth2DiscriminatedConnectorConfigIntegrations",
    "ConnectorSharepointonlineDiscriminatedConnectorConfig",
    "ConnectorSharepointonlineDiscriminatedConnectorConfigConfig",
    "ConnectorSharepointonlineDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorSharepointonlineDiscriminatedConnectorConfigConnector",
    "ConnectorSharepointonlineDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorSharepointonlineDiscriminatedConnectorConfigConnectorScope",
    "ConnectorSharepointonlineDiscriminatedConnectorConfigIntegrations",
    "ConnectorSlackDiscriminatedConnectorConfig",
    "ConnectorSlackDiscriminatedConnectorConfigConfig",
    "ConnectorSlackDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorSlackDiscriminatedConnectorConfigConnector",
    "ConnectorSlackDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorSlackDiscriminatedConnectorConfigConnectorScope",
    "ConnectorSlackDiscriminatedConnectorConfigIntegrations",
    "ConnectorGitHubDiscriminatedConnectorConfig",
    "ConnectorGitHubDiscriminatedConnectorConfigConfig",
    "ConnectorGitHubDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorGitHubDiscriminatedConnectorConfigConnector",
    "ConnectorGitHubDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGitHubDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGitHubDiscriminatedConnectorConfigIntegrations",
    "ConnectorQuickbooksDiscriminatedConnectorConfig",
    "ConnectorQuickbooksDiscriminatedConnectorConfigConfig",
    "ConnectorQuickbooksDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorQuickbooksDiscriminatedConnectorConfigConnector",
    "ConnectorQuickbooksDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorQuickbooksDiscriminatedConnectorConfigConnectorScope",
    "ConnectorQuickbooksDiscriminatedConnectorConfigIntegrations",
    "ConnectorGooglemailDiscriminatedConnectorConfig",
    "ConnectorGooglemailDiscriminatedConnectorConfigConfig",
    "ConnectorGooglemailDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorGooglemailDiscriminatedConnectorConfigConnector",
    "ConnectorGooglemailDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGooglemailDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGooglemailDiscriminatedConnectorConfigIntegrations",
    "ConnectorNotionDiscriminatedConnectorConfig",
    "ConnectorNotionDiscriminatedConnectorConfigConfig",
    "ConnectorNotionDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorNotionDiscriminatedConnectorConfigConnector",
    "ConnectorNotionDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorNotionDiscriminatedConnectorConfigConnectorScope",
    "ConnectorNotionDiscriminatedConnectorConfigIntegrations",
    "ConnectorLinkedinDiscriminatedConnectorConfig",
    "ConnectorLinkedinDiscriminatedConnectorConfigConfig",
    "ConnectorLinkedinDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorLinkedinDiscriminatedConnectorConfigConnector",
    "ConnectorLinkedinDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorLinkedinDiscriminatedConnectorConfigConnectorScope",
    "ConnectorLinkedinDiscriminatedConnectorConfigIntegrations",
    "ConnectorGoogledocsDiscriminatedConnectorConfig",
    "ConnectorGoogledocsDiscriminatedConnectorConfigConfig",
    "ConnectorGoogledocsDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorGoogledocsDiscriminatedConnectorConfigConnector",
    "ConnectorGoogledocsDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGoogledocsDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGoogledocsDiscriminatedConnectorConfigIntegrations",
    "ConnectorAircallDiscriminatedConnectorConfig",
    "ConnectorAircallDiscriminatedConnectorConfigConfig",
    "ConnectorAircallDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorAircallDiscriminatedConnectorConfigConnector",
    "ConnectorAircallDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorAircallDiscriminatedConnectorConfigConnectorScope",
    "ConnectorAircallDiscriminatedConnectorConfigIntegrations",
    "ConnectorGooglecalendarDiscriminatedConnectorConfig",
    "ConnectorGooglecalendarDiscriminatedConnectorConfigConfig",
    "ConnectorGooglecalendarDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorGooglecalendarDiscriminatedConnectorConfigConnector",
    "ConnectorGooglecalendarDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGooglecalendarDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGooglecalendarDiscriminatedConnectorConfigIntegrations",
    "ConnectorGooglesheetDiscriminatedConnectorConfig",
    "ConnectorGooglesheetDiscriminatedConnectorConfigConfig",
    "ConnectorGooglesheetDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorGooglesheetDiscriminatedConnectorConfigConnector",
    "ConnectorGooglesheetDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGooglesheetDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGooglesheetDiscriminatedConnectorConfigIntegrations",
    "ConnectorDiscordDiscriminatedConnectorConfig",
    "ConnectorDiscordDiscriminatedConnectorConfigConfig",
    "ConnectorDiscordDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorDiscordDiscriminatedConnectorConfigConnector",
    "ConnectorDiscordDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorDiscordDiscriminatedConnectorConfigConnectorScope",
    "ConnectorDiscordDiscriminatedConnectorConfigIntegrations",
    "ConnectorHubspotDiscriminatedConnectorConfig",
    "ConnectorHubspotDiscriminatedConnectorConfigConfig",
    "ConnectorHubspotDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorHubspotDiscriminatedConnectorConfigConnector",
    "ConnectorHubspotDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorHubspotDiscriminatedConnectorConfigConnectorScope",
    "ConnectorHubspotDiscriminatedConnectorConfigIntegrations",
    "ConnectorSalesforceDiscriminatedConnectorConfig",
    "ConnectorSalesforceDiscriminatedConnectorConfigConfig",
    "ConnectorSalesforceDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorSalesforceDiscriminatedConnectorConfigConnector",
    "ConnectorSalesforceDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorSalesforceDiscriminatedConnectorConfigConnectorScope",
    "ConnectorSalesforceDiscriminatedConnectorConfigIntegrations",
    "ConnectorLinearDiscriminatedConnectorConfig",
    "ConnectorLinearDiscriminatedConnectorConfigConfig",
    "ConnectorLinearDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorLinearDiscriminatedConnectorConfigConnector",
    "ConnectorLinearDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorLinearDiscriminatedConnectorConfigConnectorScope",
    "ConnectorLinearDiscriminatedConnectorConfigIntegrations",
    "ConnectorConfluenceDiscriminatedConnectorConfig",
    "ConnectorConfluenceDiscriminatedConnectorConfigConfig",
    "ConnectorConfluenceDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorConfluenceDiscriminatedConnectorConfigConnector",
    "ConnectorConfluenceDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorConfluenceDiscriminatedConnectorConfigConnectorScope",
    "ConnectorConfluenceDiscriminatedConnectorConfigIntegrations",
    "ConnectorGoogledriveDiscriminatedConnectorConfig",
    "ConnectorGoogledriveDiscriminatedConnectorConfigConfig",
    "ConnectorGoogledriveDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorGoogledriveDiscriminatedConnectorConfigConnector",
    "ConnectorGoogledriveDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGoogledriveDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGoogledriveDiscriminatedConnectorConfigIntegrations",
    "ConnectorAirtableDiscriminatedConnectorConfig",
    "ConnectorAirtableDiscriminatedConnectorConfigConnector",
    "ConnectorAirtableDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorAirtableDiscriminatedConnectorConfigConnectorScope",
    "ConnectorAirtableDiscriminatedConnectorConfigIntegrations",
    "ConnectorApolloDiscriminatedConnectorConfig",
    "ConnectorApolloDiscriminatedConnectorConfigConnector",
    "ConnectorApolloDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorApolloDiscriminatedConnectorConfigConnectorScope",
    "ConnectorApolloDiscriminatedConnectorConfigIntegrations",
    "ConnectorBrexDiscriminatedConnectorConfig",
    "ConnectorBrexDiscriminatedConnectorConfigConfig",
    "ConnectorBrexDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorBrexDiscriminatedConnectorConfigConnector",
    "ConnectorBrexDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorBrexDiscriminatedConnectorConfigConnectorScope",
    "ConnectorBrexDiscriminatedConnectorConfigIntegrations",
    "ConnectorCodaDiscriminatedConnectorConfig",
    "ConnectorCodaDiscriminatedConnectorConfigConnector",
    "ConnectorCodaDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorCodaDiscriminatedConnectorConfigConnectorScope",
    "ConnectorCodaDiscriminatedConnectorConfigIntegrations",
    "ConnectorFacebookDiscriminatedConnectorConfig",
    "ConnectorFacebookDiscriminatedConnectorConfigConfig",
    "ConnectorFacebookDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorFacebookDiscriminatedConnectorConfigConnector",
    "ConnectorFacebookDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorFacebookDiscriminatedConnectorConfigConnectorScope",
    "ConnectorFacebookDiscriminatedConnectorConfigIntegrations",
    "ConnectorFinchDiscriminatedConnectorConfig",
    "ConnectorFinchDiscriminatedConnectorConfigConfig",
    "ConnectorFinchDiscriminatedConnectorConfigConnector",
    "ConnectorFinchDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorFinchDiscriminatedConnectorConfigConnectorScope",
    "ConnectorFinchDiscriminatedConnectorConfigIntegrations",
    "ConnectorFirebaseDiscriminatedConnectorConfig",
    "ConnectorFirebaseDiscriminatedConnectorConfigConnector",
    "ConnectorFirebaseDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorFirebaseDiscriminatedConnectorConfigConnectorScope",
    "ConnectorFirebaseDiscriminatedConnectorConfigIntegrations",
    "ConnectorForeceiptDiscriminatedConnectorConfig",
    "ConnectorForeceiptDiscriminatedConnectorConfigConnector",
    "ConnectorForeceiptDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorForeceiptDiscriminatedConnectorConfigConnectorScope",
    "ConnectorForeceiptDiscriminatedConnectorConfigIntegrations",
    "ConnectorGongDiscriminatedConnectorConfig",
    "ConnectorGongDiscriminatedConnectorConfigConfig",
    "ConnectorGongDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorGongDiscriminatedConnectorConfigConnector",
    "ConnectorGongDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGongDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGongDiscriminatedConnectorConfigIntegrations",
    "ConnectorGreenhouseDiscriminatedConnectorConfig",
    "ConnectorGreenhouseDiscriminatedConnectorConfigConnector",
    "ConnectorGreenhouseDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorGreenhouseDiscriminatedConnectorConfigConnectorScope",
    "ConnectorGreenhouseDiscriminatedConnectorConfigIntegrations",
    "ConnectorHeronDiscriminatedConnectorConfig",
    "ConnectorHeronDiscriminatedConnectorConfigConfig",
    "ConnectorHeronDiscriminatedConnectorConfigConnector",
    "ConnectorHeronDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorHeronDiscriminatedConnectorConfigConnectorScope",
    "ConnectorHeronDiscriminatedConnectorConfigIntegrations",
    "ConnectorInstagramDiscriminatedConnectorConfig",
    "ConnectorInstagramDiscriminatedConnectorConfigConfig",
    "ConnectorInstagramDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorInstagramDiscriminatedConnectorConfigConnector",
    "ConnectorInstagramDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorInstagramDiscriminatedConnectorConfigConnectorScope",
    "ConnectorInstagramDiscriminatedConnectorConfigIntegrations",
    "ConnectorIntercomDiscriminatedConnectorConfig",
    "ConnectorIntercomDiscriminatedConnectorConfigConfig",
    "ConnectorIntercomDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorIntercomDiscriminatedConnectorConfigConnector",
    "ConnectorIntercomDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorIntercomDiscriminatedConnectorConfigConnectorScope",
    "ConnectorIntercomDiscriminatedConnectorConfigIntegrations",
    "ConnectorJiraDiscriminatedConnectorConfig",
    "ConnectorJiraDiscriminatedConnectorConfigConfig",
    "ConnectorJiraDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorJiraDiscriminatedConnectorConfigConnector",
    "ConnectorJiraDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorJiraDiscriminatedConnectorConfigConnectorScope",
    "ConnectorJiraDiscriminatedConnectorConfigIntegrations",
    "ConnectorKustomerDiscriminatedConnectorConfig",
    "ConnectorKustomerDiscriminatedConnectorConfigConfig",
    "ConnectorKustomerDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorKustomerDiscriminatedConnectorConfigConnector",
    "ConnectorKustomerDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorKustomerDiscriminatedConnectorConfigConnectorScope",
    "ConnectorKustomerDiscriminatedConnectorConfigIntegrations",
    "ConnectorLeverDiscriminatedConnectorConfig",
    "ConnectorLeverDiscriminatedConnectorConfigConfig",
    "ConnectorLeverDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorLeverDiscriminatedConnectorConfigConnector",
    "ConnectorLeverDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorLeverDiscriminatedConnectorConfigConnectorScope",
    "ConnectorLeverDiscriminatedConnectorConfigIntegrations",
    "ConnectorLunchmoneyDiscriminatedConnectorConfig",
    "ConnectorLunchmoneyDiscriminatedConnectorConfigConfig",
    "ConnectorLunchmoneyDiscriminatedConnectorConfigConnector",
    "ConnectorLunchmoneyDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorLunchmoneyDiscriminatedConnectorConfigConnectorScope",
    "ConnectorLunchmoneyDiscriminatedConnectorConfigIntegrations",
    "ConnectorMercuryDiscriminatedConnectorConfig",
    "ConnectorMercuryDiscriminatedConnectorConfigConfig",
    "ConnectorMercuryDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorMercuryDiscriminatedConnectorConfigConnector",
    "ConnectorMercuryDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorMercuryDiscriminatedConnectorConfigConnectorScope",
    "ConnectorMercuryDiscriminatedConnectorConfigIntegrations",
    "ConnectorMergeDiscriminatedConnectorConfig",
    "ConnectorMergeDiscriminatedConnectorConfigConfig",
    "ConnectorMergeDiscriminatedConnectorConfigConnector",
    "ConnectorMergeDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorMergeDiscriminatedConnectorConfigConnectorScope",
    "ConnectorMergeDiscriminatedConnectorConfigIntegrations",
    "ConnectorMicrosoftDiscriminatedConnectorConfig",
    "ConnectorMicrosoftDiscriminatedConnectorConfigConfig",
    "ConnectorMicrosoftDiscriminatedConnectorConfigConfigIntegrations",
    "ConnectorMicrosoftDiscriminatedConnectorConfigConfigIntegrationsOutlook",
    "ConnectorMicrosoftDiscriminatedConnectorConfigConfigIntegrationsSharepoint",
    "ConnectorMicrosoftDiscriminatedConnectorConfigConfigIntegrationsTeams",
    "ConnectorMicrosoftDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorMicrosoftDiscriminatedConnectorConfigConnector",
    "ConnectorMicrosoftDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorMicrosoftDiscriminatedConnectorConfigConnectorScope",
    "ConnectorMicrosoftDiscriminatedConnectorConfigIntegrations",
    "ConnectorMootaDiscriminatedConnectorConfig",
    "ConnectorMootaDiscriminatedConnectorConfigConfig",
    "ConnectorMootaDiscriminatedConnectorConfigConnector",
    "ConnectorMootaDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorMootaDiscriminatedConnectorConfigConnectorScope",
    "ConnectorMootaDiscriminatedConnectorConfigIntegrations",
    "ConnectorOnebrickDiscriminatedConnectorConfig",
    "ConnectorOnebrickDiscriminatedConnectorConfigConfig",
    "ConnectorOnebrickDiscriminatedConnectorConfigConnector",
    "ConnectorOnebrickDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorOnebrickDiscriminatedConnectorConfigConnectorScope",
    "ConnectorOnebrickDiscriminatedConnectorConfigIntegrations",
    "ConnectorOutreachDiscriminatedConnectorConfig",
    "ConnectorOutreachDiscriminatedConnectorConfigConfig",
    "ConnectorOutreachDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorOutreachDiscriminatedConnectorConfigConnector",
    "ConnectorOutreachDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorOutreachDiscriminatedConnectorConfigConnectorScope",
    "ConnectorOutreachDiscriminatedConnectorConfigIntegrations",
    "ConnectorPipedriveDiscriminatedConnectorConfig",
    "ConnectorPipedriveDiscriminatedConnectorConfigConfig",
    "ConnectorPipedriveDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorPipedriveDiscriminatedConnectorConfigConnector",
    "ConnectorPipedriveDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorPipedriveDiscriminatedConnectorConfigConnectorScope",
    "ConnectorPipedriveDiscriminatedConnectorConfigIntegrations",
    "ConnectorPlaidDiscriminatedConnectorConfig",
    "ConnectorPlaidDiscriminatedConnectorConfigConfig",
    "ConnectorPlaidDiscriminatedConnectorConfigConfigCredentials",
    "ConnectorPlaidDiscriminatedConnectorConfigConnector",
    "ConnectorPlaidDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorPlaidDiscriminatedConnectorConfigConnectorScope",
    "ConnectorPlaidDiscriminatedConnectorConfigIntegrations",
    "ConnectorPostgresDiscriminatedConnectorConfig",
    "ConnectorPostgresDiscriminatedConnectorConfigConnector",
    "ConnectorPostgresDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorPostgresDiscriminatedConnectorConfigConnectorScope",
    "ConnectorPostgresDiscriminatedConnectorConfigIntegrations",
    "ConnectorRampDiscriminatedConnectorConfig",
    "ConnectorRampDiscriminatedConnectorConfigConfig",
    "ConnectorRampDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorRampDiscriminatedConnectorConfigConnector",
    "ConnectorRampDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorRampDiscriminatedConnectorConfigConnectorScope",
    "ConnectorRampDiscriminatedConnectorConfigIntegrations",
    "ConnectorRedditDiscriminatedConnectorConfig",
    "ConnectorRedditDiscriminatedConnectorConfigConfig",
    "ConnectorRedditDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorRedditDiscriminatedConnectorConfigConnector",
    "ConnectorRedditDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorRedditDiscriminatedConnectorConfigConnectorScope",
    "ConnectorRedditDiscriminatedConnectorConfigIntegrations",
    "ConnectorSalesloftDiscriminatedConnectorConfig",
    "ConnectorSalesloftDiscriminatedConnectorConfigConfig",
    "ConnectorSalesloftDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorSalesloftDiscriminatedConnectorConfigConnector",
    "ConnectorSalesloftDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorSalesloftDiscriminatedConnectorConfigConnectorScope",
    "ConnectorSalesloftDiscriminatedConnectorConfigIntegrations",
    "ConnectorSaltedgeDiscriminatedConnectorConfig",
    "ConnectorSaltedgeDiscriminatedConnectorConfigConfig",
    "ConnectorSaltedgeDiscriminatedConnectorConfigConnector",
    "ConnectorSaltedgeDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorSaltedgeDiscriminatedConnectorConfigConnectorScope",
    "ConnectorSaltedgeDiscriminatedConnectorConfigIntegrations",
    "ConnectorSplitwiseDiscriminatedConnectorConfig",
    "ConnectorSplitwiseDiscriminatedConnectorConfigConnector",
    "ConnectorSplitwiseDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorSplitwiseDiscriminatedConnectorConfigConnectorScope",
    "ConnectorSplitwiseDiscriminatedConnectorConfigIntegrations",
    "ConnectorStripeDiscriminatedConnectorConfig",
    "ConnectorStripeDiscriminatedConnectorConfigConfig",
    "ConnectorStripeDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorStripeDiscriminatedConnectorConfigConnector",
    "ConnectorStripeDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorStripeDiscriminatedConnectorConfigConnectorScope",
    "ConnectorStripeDiscriminatedConnectorConfigIntegrations",
    "ConnectorTellerDiscriminatedConnectorConfig",
    "ConnectorTellerDiscriminatedConnectorConfigConfig",
    "ConnectorTellerDiscriminatedConnectorConfigConnector",
    "ConnectorTellerDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorTellerDiscriminatedConnectorConfigConnectorScope",
    "ConnectorTellerDiscriminatedConnectorConfigIntegrations",
    "ConnectorTogglDiscriminatedConnectorConfig",
    "ConnectorTogglDiscriminatedConnectorConfigConnector",
    "ConnectorTogglDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorTogglDiscriminatedConnectorConfigConnectorScope",
    "ConnectorTogglDiscriminatedConnectorConfigIntegrations",
    "ConnectorTwentyDiscriminatedConnectorConfig",
    "ConnectorTwentyDiscriminatedConnectorConfigConnector",
    "ConnectorTwentyDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorTwentyDiscriminatedConnectorConfigConnectorScope",
    "ConnectorTwentyDiscriminatedConnectorConfigIntegrations",
    "ConnectorTwitterDiscriminatedConnectorConfig",
    "ConnectorTwitterDiscriminatedConnectorConfigConfig",
    "ConnectorTwitterDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorTwitterDiscriminatedConnectorConfigConnector",
    "ConnectorTwitterDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorTwitterDiscriminatedConnectorConfigConnectorScope",
    "ConnectorTwitterDiscriminatedConnectorConfigIntegrations",
    "ConnectorVenmoDiscriminatedConnectorConfig",
    "ConnectorVenmoDiscriminatedConnectorConfigConfig",
    "ConnectorVenmoDiscriminatedConnectorConfigConfigProxy",
    "ConnectorVenmoDiscriminatedConnectorConfigConnector",
    "ConnectorVenmoDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorVenmoDiscriminatedConnectorConfigConnectorScope",
    "ConnectorVenmoDiscriminatedConnectorConfigIntegrations",
    "ConnectorWiseDiscriminatedConnectorConfig",
    "ConnectorWiseDiscriminatedConnectorConfigConnector",
    "ConnectorWiseDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorWiseDiscriminatedConnectorConfigConnectorScope",
    "ConnectorWiseDiscriminatedConnectorConfigIntegrations",
    "ConnectorXeroDiscriminatedConnectorConfig",
    "ConnectorXeroDiscriminatedConnectorConfigConfig",
    "ConnectorXeroDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorXeroDiscriminatedConnectorConfigConnector",
    "ConnectorXeroDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorXeroDiscriminatedConnectorConfigConnectorScope",
    "ConnectorXeroDiscriminatedConnectorConfigIntegrations",
    "ConnectorYodleeDiscriminatedConnectorConfig",
    "ConnectorYodleeDiscriminatedConnectorConfigConfig",
    "ConnectorYodleeDiscriminatedConnectorConfigConfigProxy",
    "ConnectorYodleeDiscriminatedConnectorConfigConnector",
    "ConnectorYodleeDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorYodleeDiscriminatedConnectorConfigConnectorScope",
    "ConnectorYodleeDiscriminatedConnectorConfigIntegrations",
    "ConnectorZohodeskDiscriminatedConnectorConfig",
    "ConnectorZohodeskDiscriminatedConnectorConfigConfig",
    "ConnectorZohodeskDiscriminatedConnectorConfigConfigOAuth",
    "ConnectorZohodeskDiscriminatedConnectorConfigConnector",
    "ConnectorZohodeskDiscriminatedConnectorConfigConnectorSchemas",
    "ConnectorZohodeskDiscriminatedConnectorConfigConnectorScope",
    "ConnectorZohodeskDiscriminatedConnectorConfigIntegrations",
]


class ConnectorDummyOauth2DiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorDummyOauth2DiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorDummyOauth2DiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorDummyOauth2DiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorDummyOauth2DiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorDummyOauth2DiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorDummyOauth2DiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorDummyOauth2DiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorDummyOauth2DiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorDummyOauth2DiscriminatedConnectorConfig(BaseModel):
    config: ConnectorDummyOauth2DiscriminatedConnectorConfigConfig

    connector_name: Literal["dummy-oauth2"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorDummyOauth2DiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorDummyOauth2DiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSharepointonlineDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorSharepointonlineDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorSharepointonlineDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorSharepointonlineDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSharepointonlineDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSharepointonlineDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSharepointonlineDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorSharepointonlineDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSharepointonlineDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorSharepointonlineDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorSharepointonlineDiscriminatedConnectorConfigConfig

    connector_name: Literal["sharepointonline"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorSharepointonlineDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorSharepointonlineDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSlackDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorSlackDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorSlackDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorSlackDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSlackDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSlackDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSlackDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorSlackDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSlackDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorSlackDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorSlackDiscriminatedConnectorConfigConfig

    connector_name: Literal["slack"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorSlackDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorSlackDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGitHubDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorGitHubDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorGitHubDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorGitHubDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGitHubDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGitHubDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGitHubDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGitHubDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGitHubDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGitHubDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorGitHubDiscriminatedConnectorConfigConfig

    connector_name: Literal["github"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGitHubDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGitHubDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorQuickbooksDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorQuickbooksDiscriminatedConnectorConfigConfig(BaseModel):
    env_name: Literal["sandbox", "production"] = FieldInfo(alias="envName")

    oauth: Optional[ConnectorQuickbooksDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorQuickbooksDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorQuickbooksDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorQuickbooksDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorQuickbooksDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorQuickbooksDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorQuickbooksDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorQuickbooksDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorQuickbooksDiscriminatedConnectorConfigConfig

    connector_name: Literal["quickbooks"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorQuickbooksDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorQuickbooksDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGooglemailDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorGooglemailDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorGooglemailDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorGooglemailDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGooglemailDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGooglemailDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGooglemailDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGooglemailDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGooglemailDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGooglemailDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorGooglemailDiscriminatedConnectorConfigConfig

    connector_name: Literal["googlemail"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGooglemailDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGooglemailDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorNotionDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorNotionDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorNotionDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorNotionDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorNotionDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorNotionDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorNotionDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorNotionDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorNotionDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorNotionDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorNotionDiscriminatedConnectorConfigConfig

    connector_name: Literal["notion"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorNotionDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorNotionDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorLinkedinDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorLinkedinDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorLinkedinDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorLinkedinDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLinkedinDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLinkedinDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLinkedinDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorLinkedinDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLinkedinDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorLinkedinDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorLinkedinDiscriminatedConnectorConfigConfig

    connector_name: Literal["linkedin"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorLinkedinDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorLinkedinDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGoogledocsDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorGoogledocsDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorGoogledocsDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorGoogledocsDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGoogledocsDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGoogledocsDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGoogledocsDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGoogledocsDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGoogledocsDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGoogledocsDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorGoogledocsDiscriminatedConnectorConfigConfig

    connector_name: Literal["googledocs"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGoogledocsDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGoogledocsDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorAircallDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorAircallDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorAircallDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorAircallDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorAircallDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorAircallDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorAircallDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorAircallDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorAircallDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorAircallDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorAircallDiscriminatedConnectorConfigConfig

    connector_name: Literal["aircall"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorAircallDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorAircallDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGooglecalendarDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorGooglecalendarDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorGooglecalendarDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorGooglecalendarDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGooglecalendarDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGooglecalendarDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGooglecalendarDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGooglecalendarDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGooglecalendarDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGooglecalendarDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorGooglecalendarDiscriminatedConnectorConfigConfig

    connector_name: Literal["googlecalendar"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGooglecalendarDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGooglecalendarDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGooglesheetDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorGooglesheetDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorGooglesheetDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorGooglesheetDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGooglesheetDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGooglesheetDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGooglesheetDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGooglesheetDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGooglesheetDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGooglesheetDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorGooglesheetDiscriminatedConnectorConfigConfig

    connector_name: Literal["googlesheet"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGooglesheetDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGooglesheetDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorDiscordDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorDiscordDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorDiscordDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorDiscordDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorDiscordDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorDiscordDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorDiscordDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorDiscordDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorDiscordDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorDiscordDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorDiscordDiscriminatedConnectorConfigConfig

    connector_name: Literal["discord"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorDiscordDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorDiscordDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorHubspotDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorHubspotDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorHubspotDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorHubspotDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorHubspotDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorHubspotDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorHubspotDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorHubspotDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorHubspotDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorHubspotDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorHubspotDiscriminatedConnectorConfigConfig

    connector_name: Literal["hubspot"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorHubspotDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorHubspotDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSalesforceDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorSalesforceDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorSalesforceDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorSalesforceDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSalesforceDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSalesforceDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSalesforceDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorSalesforceDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSalesforceDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorSalesforceDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorSalesforceDiscriminatedConnectorConfigConfig

    connector_name: Literal["salesforce"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorSalesforceDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorSalesforceDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorLinearDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorLinearDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorLinearDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorLinearDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLinearDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLinearDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLinearDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorLinearDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLinearDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorLinearDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorLinearDiscriminatedConnectorConfigConfig

    connector_name: Literal["linear"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorLinearDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorLinearDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorConfluenceDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorConfluenceDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorConfluenceDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorConfluenceDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorConfluenceDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorConfluenceDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorConfluenceDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorConfluenceDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorConfluenceDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorConfluenceDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorConfluenceDiscriminatedConnectorConfigConfig

    connector_name: Literal["confluence"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorConfluenceDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorConfluenceDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGoogledriveDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: Optional[str] = None

    client_secret: Optional[str] = None

    redirect_uri: Optional[str] = None

    scopes: Optional[List[str]] = None


class ConnectorGoogledriveDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: Optional[ConnectorGoogledriveDiscriminatedConnectorConfigConfigOAuth] = None
    """Base oauth configuration for the connector"""


class ConnectorGoogledriveDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGoogledriveDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGoogledriveDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGoogledriveDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGoogledriveDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGoogledriveDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGoogledriveDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorGoogledriveDiscriminatedConnectorConfigConfig

    connector_name: Literal["googledrive"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGoogledriveDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGoogledriveDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorAirtableDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorAirtableDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorAirtableDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorAirtableDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorAirtableDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorAirtableDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorAirtableDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["airtable"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorAirtableDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorAirtableDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorApolloDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorApolloDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorApolloDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorApolloDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorApolloDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorApolloDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorApolloDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["apollo"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorApolloDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorApolloDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorBrexDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorBrexDiscriminatedConnectorConfigConfig(BaseModel):
    apikey_auth: Optional[bool] = FieldInfo(alias="apikeyAuth", default=None)
    """API key auth support"""

    oauth: Optional[ConnectorBrexDiscriminatedConnectorConfigConfigOAuth] = None
    """Configure oauth"""


class ConnectorBrexDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorBrexDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorBrexDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorBrexDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorBrexDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorBrexDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorBrexDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorBrexDiscriminatedConnectorConfigConfig

    connector_name: Literal["brex"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorBrexDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorBrexDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorCodaDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorCodaDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorCodaDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorCodaDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorCodaDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorCodaDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorCodaDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["coda"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorCodaDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorCodaDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorFacebookDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorFacebookDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorFacebookDiscriminatedConnectorConfigConfigOAuth


class ConnectorFacebookDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorFacebookDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorFacebookDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorFacebookDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorFacebookDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorFacebookDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorFacebookDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorFacebookDiscriminatedConnectorConfigConfig

    connector_name: Literal["facebook"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorFacebookDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorFacebookDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorFinchDiscriminatedConnectorConfigConfig(BaseModel):
    client_id: str

    client_secret: str

    products: List[
        Literal["company", "directory", "individual", "ssn", "employment", "payment", "pay_statement", "benefits"]
    ]
    """
    Finch products to access, @see
    https://developer.tryfinch.com/api-reference/development-guides/Permissions
    """

    api_version: Optional[str] = None
    """Finch API version"""


class ConnectorFinchDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorFinchDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorFinchDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorFinchDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorFinchDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorFinchDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorFinchDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorFinchDiscriminatedConnectorConfigConfig

    connector_name: Literal["finch"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorFinchDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorFinchDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorFirebaseDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorFirebaseDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorFirebaseDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorFirebaseDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorFirebaseDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorFirebaseDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorFirebaseDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["firebase"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorFirebaseDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorFirebaseDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorForeceiptDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorForeceiptDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorForeceiptDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorForeceiptDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorForeceiptDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorForeceiptDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorForeceiptDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["foreceipt"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorForeceiptDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorForeceiptDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGongDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorGongDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorGongDiscriminatedConnectorConfigConfigOAuth


class ConnectorGongDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGongDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGongDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGongDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGongDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGongDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGongDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorGongDiscriminatedConnectorConfigConfig

    connector_name: Literal["gong"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGongDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGongDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorGreenhouseDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorGreenhouseDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorGreenhouseDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorGreenhouseDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorGreenhouseDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorGreenhouseDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorGreenhouseDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["greenhouse"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorGreenhouseDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorGreenhouseDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorHeronDiscriminatedConnectorConfigConfig(BaseModel):
    api_key: str = FieldInfo(alias="apiKey")


class ConnectorHeronDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorHeronDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorHeronDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorHeronDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorHeronDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorHeronDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorHeronDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorHeronDiscriminatedConnectorConfigConfig

    connector_name: Literal["heron"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorHeronDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorHeronDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorInstagramDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorInstagramDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorInstagramDiscriminatedConnectorConfigConfigOAuth


class ConnectorInstagramDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorInstagramDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorInstagramDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorInstagramDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorInstagramDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorInstagramDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorInstagramDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorInstagramDiscriminatedConnectorConfigConfig

    connector_name: Literal["instagram"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorInstagramDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorInstagramDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorIntercomDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorIntercomDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorIntercomDiscriminatedConnectorConfigConfigOAuth


class ConnectorIntercomDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorIntercomDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorIntercomDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorIntercomDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorIntercomDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorIntercomDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorIntercomDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorIntercomDiscriminatedConnectorConfigConfig

    connector_name: Literal["intercom"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorIntercomDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorIntercomDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorJiraDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorJiraDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorJiraDiscriminatedConnectorConfigConfigOAuth


class ConnectorJiraDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorJiraDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorJiraDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorJiraDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorJiraDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorJiraDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorJiraDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorJiraDiscriminatedConnectorConfigConfig

    connector_name: Literal["jira"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorJiraDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorJiraDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorKustomerDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorKustomerDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorKustomerDiscriminatedConnectorConfigConfigOAuth


class ConnectorKustomerDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorKustomerDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorKustomerDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorKustomerDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorKustomerDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorKustomerDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorKustomerDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorKustomerDiscriminatedConnectorConfigConfig

    connector_name: Literal["kustomer"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorKustomerDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorKustomerDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorLeverDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorLeverDiscriminatedConnectorConfigConfig(BaseModel):
    env_name: Literal["sandbox", "production"] = FieldInfo(alias="envName")

    oauth: ConnectorLeverDiscriminatedConnectorConfigConfigOAuth


class ConnectorLeverDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLeverDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLeverDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLeverDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorLeverDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLeverDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorLeverDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorLeverDiscriminatedConnectorConfigConfig

    connector_name: Literal["lever"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorLeverDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorLeverDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorLunchmoneyDiscriminatedConnectorConfigConfig(BaseModel):
    access_token: str = FieldInfo(alias="accessToken")


class ConnectorLunchmoneyDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorLunchmoneyDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorLunchmoneyDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorLunchmoneyDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorLunchmoneyDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorLunchmoneyDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorLunchmoneyDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorLunchmoneyDiscriminatedConnectorConfigConfig

    connector_name: Literal["lunchmoney"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorLunchmoneyDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorLunchmoneyDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorMercuryDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorMercuryDiscriminatedConnectorConfigConfig(BaseModel):
    apikey_auth: Optional[bool] = FieldInfo(alias="apikeyAuth", default=None)
    """API key auth support"""

    oauth: Optional[ConnectorMercuryDiscriminatedConnectorConfigConfigOAuth] = None
    """Configure oauth"""


class ConnectorMercuryDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorMercuryDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorMercuryDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorMercuryDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorMercuryDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorMercuryDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorMercuryDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorMercuryDiscriminatedConnectorConfigConfig

    connector_name: Literal["mercury"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorMercuryDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorMercuryDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorMergeDiscriminatedConnectorConfigConfig(BaseModel):
    api_key: str = FieldInfo(alias="apiKey")


class ConnectorMergeDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorMergeDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorMergeDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorMergeDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorMergeDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorMergeDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorMergeDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorMergeDiscriminatedConnectorConfigConfig

    connector_name: Literal["merge"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorMergeDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorMergeDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorMicrosoftDiscriminatedConnectorConfigConfigIntegrationsOutlook(BaseModel):
    enabled: Optional[bool] = None

    scopes: Optional[str] = None
    """outlook specific space separated scopes"""


class ConnectorMicrosoftDiscriminatedConnectorConfigConfigIntegrationsSharepoint(BaseModel):
    enabled: Optional[bool] = None

    scopes: Optional[str] = None
    """sharepoint specific space separated scopes"""


class ConnectorMicrosoftDiscriminatedConnectorConfigConfigIntegrationsTeams(BaseModel):
    enabled: Optional[bool] = None

    scopes: Optional[str] = None
    """teams specific space separated scopes"""


class ConnectorMicrosoftDiscriminatedConnectorConfigConfigIntegrations(BaseModel):
    outlook: Optional[ConnectorMicrosoftDiscriminatedConnectorConfigConfigIntegrationsOutlook] = None

    sharepoint: Optional[ConnectorMicrosoftDiscriminatedConnectorConfigConfigIntegrationsSharepoint] = None

    teams: Optional[ConnectorMicrosoftDiscriminatedConnectorConfigConfigIntegrationsTeams] = None


class ConnectorMicrosoftDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None
    """global microsoft connector space separated scopes"""


class ConnectorMicrosoftDiscriminatedConnectorConfigConfig(BaseModel):
    integrations: ConnectorMicrosoftDiscriminatedConnectorConfigConfigIntegrations

    oauth: ConnectorMicrosoftDiscriminatedConnectorConfigConfigOAuth


class ConnectorMicrosoftDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorMicrosoftDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorMicrosoftDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorMicrosoftDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorMicrosoftDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorMicrosoftDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorMicrosoftDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorMicrosoftDiscriminatedConnectorConfigConfig

    connector_name: Literal["microsoft"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorMicrosoftDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorMicrosoftDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorMootaDiscriminatedConnectorConfigConfig(BaseModel):
    token: str


class ConnectorMootaDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorMootaDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorMootaDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorMootaDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorMootaDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorMootaDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorMootaDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorMootaDiscriminatedConnectorConfigConfig

    connector_name: Literal["moota"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorMootaDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorMootaDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorOnebrickDiscriminatedConnectorConfigConfig(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")

    env_name: Literal["sandbox", "production"] = FieldInfo(alias="envName")

    public_token: str = FieldInfo(alias="publicToken")

    access_token: Optional[str] = FieldInfo(alias="accessToken", default=None)

    redirect_url: Optional[str] = FieldInfo(alias="redirectUrl", default=None)


class ConnectorOnebrickDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorOnebrickDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorOnebrickDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorOnebrickDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorOnebrickDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorOnebrickDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorOnebrickDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorOnebrickDiscriminatedConnectorConfigConfig

    connector_name: Literal["onebrick"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorOnebrickDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorOnebrickDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorOutreachDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorOutreachDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorOutreachDiscriminatedConnectorConfigConfigOAuth


class ConnectorOutreachDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorOutreachDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorOutreachDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorOutreachDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorOutreachDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorOutreachDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorOutreachDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorOutreachDiscriminatedConnectorConfigConfig

    connector_name: Literal["outreach"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorOutreachDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorOutreachDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorPipedriveDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorPipedriveDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorPipedriveDiscriminatedConnectorConfigConfigOAuth


class ConnectorPipedriveDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorPipedriveDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorPipedriveDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorPipedriveDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorPipedriveDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorPipedriveDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorPipedriveDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorPipedriveDiscriminatedConnectorConfigConfig

    connector_name: Literal["pipedrive"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorPipedriveDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorPipedriveDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorPlaidDiscriminatedConnectorConfigConfigCredentials(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorPlaidDiscriminatedConnectorConfigConfig(BaseModel):
    client_name: str = FieldInfo(alias="clientName")
    """
    The name of your application, as it should be displayed in Link. Maximum length
    of 30 characters. If a value longer than 30 characters is provided, Link will
    display "This Application" instead.
    """

    country_codes: List[
        Literal["US", "GB", "ES", "NL", "FR", "IE", "CA", "DE", "IT", "PL", "DK", "NO", "SE", "EE", "LT", "LV"]
    ] = FieldInfo(alias="countryCodes")

    env_name: Literal["sandbox", "development", "production"] = FieldInfo(alias="envName")

    language: Literal["en", "fr", "es", "nl", "de"]

    products: List[
        Literal[
            "assets",
            "auth",
            "balance",
            "identity",
            "investments",
            "liabilities",
            "payment_initiation",
            "identity_verification",
            "transactions",
            "credit_details",
            "income",
            "income_verification",
            "deposit_switch",
            "standing_orders",
            "transfer",
            "employment",
            "recurring_transactions",
        ]
    ]

    credentials: Optional[ConnectorPlaidDiscriminatedConnectorConfigConfigCredentials] = None


class ConnectorPlaidDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorPlaidDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorPlaidDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorPlaidDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorPlaidDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorPlaidDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorPlaidDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorPlaidDiscriminatedConnectorConfigConfig

    connector_name: Literal["plaid"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorPlaidDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorPlaidDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorPostgresDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorPostgresDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorPostgresDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorPostgresDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorPostgresDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorPostgresDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorPostgresDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["postgres"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorPostgresDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorPostgresDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorRampDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorRampDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorRampDiscriminatedConnectorConfigConfigOAuth


class ConnectorRampDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorRampDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorRampDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorRampDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorRampDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorRampDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorRampDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorRampDiscriminatedConnectorConfigConfig

    connector_name: Literal["ramp"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorRampDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorRampDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorRedditDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorRedditDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorRedditDiscriminatedConnectorConfigConfigOAuth


class ConnectorRedditDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorRedditDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorRedditDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorRedditDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorRedditDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorRedditDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorRedditDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorRedditDiscriminatedConnectorConfigConfig

    connector_name: Literal["reddit"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorRedditDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorRedditDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSalesloftDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorSalesloftDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorSalesloftDiscriminatedConnectorConfigConfigOAuth


class ConnectorSalesloftDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSalesloftDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSalesloftDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSalesloftDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorSalesloftDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSalesloftDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorSalesloftDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorSalesloftDiscriminatedConnectorConfigConfig

    connector_name: Literal["salesloft"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorSalesloftDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorSalesloftDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSaltedgeDiscriminatedConnectorConfigConfig(BaseModel):
    app_id: str = FieldInfo(alias="appId")

    secret: str

    url: Optional[str] = None


class ConnectorSaltedgeDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSaltedgeDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSaltedgeDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSaltedgeDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorSaltedgeDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSaltedgeDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorSaltedgeDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorSaltedgeDiscriminatedConnectorConfigConfig

    connector_name: Literal["saltedge"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorSaltedgeDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorSaltedgeDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorSplitwiseDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorSplitwiseDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorSplitwiseDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorSplitwiseDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorSplitwiseDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorSplitwiseDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorSplitwiseDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["splitwise"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorSplitwiseDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorSplitwiseDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorStripeDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")


class ConnectorStripeDiscriminatedConnectorConfigConfig(BaseModel):
    apikey_auth: Optional[bool] = FieldInfo(alias="apikeyAuth", default=None)
    """API key auth support"""

    oauth: Optional[ConnectorStripeDiscriminatedConnectorConfigConfigOAuth] = None
    """Configure oauth"""


class ConnectorStripeDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorStripeDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorStripeDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorStripeDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorStripeDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorStripeDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorStripeDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorStripeDiscriminatedConnectorConfigConfig

    connector_name: Literal["stripe"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorStripeDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorStripeDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorTellerDiscriminatedConnectorConfigConfig(BaseModel):
    application_id: str = FieldInfo(alias="applicationId")

    token: Optional[str] = None


class ConnectorTellerDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTellerDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTellerDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTellerDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorTellerDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTellerDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorTellerDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorTellerDiscriminatedConnectorConfigConfig

    connector_name: Literal["teller"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorTellerDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorTellerDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorTogglDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTogglDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTogglDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTogglDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorTogglDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTogglDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorTogglDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["toggl"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorTogglDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorTogglDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorTwentyDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTwentyDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTwentyDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTwentyDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorTwentyDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTwentyDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorTwentyDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["twenty"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorTwentyDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorTwentyDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorTwitterDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorTwitterDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorTwitterDiscriminatedConnectorConfigConfigOAuth


class ConnectorTwitterDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorTwitterDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorTwitterDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorTwitterDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorTwitterDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorTwitterDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorTwitterDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorTwitterDiscriminatedConnectorConfigConfig

    connector_name: Literal["twitter"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorTwitterDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorTwitterDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorVenmoDiscriminatedConnectorConfigConfigProxy(BaseModel):
    cert: str

    url: str


class ConnectorVenmoDiscriminatedConnectorConfigConfig(BaseModel):
    proxy: Optional[ConnectorVenmoDiscriminatedConnectorConfigConfigProxy] = None

    v1_base_url: Optional[str] = FieldInfo(alias="v1BaseURL", default=None)

    v5_base_url: Optional[str] = FieldInfo(alias="v5BaseURL", default=None)


class ConnectorVenmoDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorVenmoDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorVenmoDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorVenmoDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorVenmoDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorVenmoDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorVenmoDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorVenmoDiscriminatedConnectorConfigConfig

    connector_name: Literal["venmo"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorVenmoDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorVenmoDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorWiseDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorWiseDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorWiseDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorWiseDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorWiseDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorWiseDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorWiseDiscriminatedConnectorConfig(BaseModel):
    config: object

    connector_name: Literal["wise"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorWiseDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorWiseDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorXeroDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorXeroDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorXeroDiscriminatedConnectorConfigConfigOAuth


class ConnectorXeroDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorXeroDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorXeroDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorXeroDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorXeroDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorXeroDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorXeroDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorXeroDiscriminatedConnectorConfigConfig

    connector_name: Literal["xero"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorXeroDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorXeroDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorYodleeDiscriminatedConnectorConfigConfigProxy(BaseModel):
    cert: str

    url: str


class ConnectorYodleeDiscriminatedConnectorConfigConfig(BaseModel):
    admin_login_name: str = FieldInfo(alias="adminLoginName")

    client_id: str = FieldInfo(alias="clientId")

    client_secret: str = FieldInfo(alias="clientSecret")

    env_name: Literal["sandbox", "development", "production"] = FieldInfo(alias="envName")

    proxy: Optional[ConnectorYodleeDiscriminatedConnectorConfigConfigProxy] = None

    sandbox_login_name: Optional[str] = FieldInfo(alias="sandboxLoginName", default=None)


class ConnectorYodleeDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorYodleeDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorYodleeDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorYodleeDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorYodleeDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorYodleeDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorYodleeDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorYodleeDiscriminatedConnectorConfigConfig

    connector_name: Literal["yodlee"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorYodleeDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorYodleeDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


class ConnectorZohodeskDiscriminatedConnectorConfigConfigOAuth(BaseModel):
    client_id: str

    client_secret: str

    scopes: Optional[str] = None


class ConnectorZohodeskDiscriminatedConnectorConfigConfig(BaseModel):
    oauth: ConnectorZohodeskDiscriminatedConnectorConfigConfigOAuth


class ConnectorZohodeskDiscriminatedConnectorConfigConnectorSchemas(BaseModel):
    connect_input: Optional[object] = None

    connect_output: Optional[object] = None

    connection_settings: Optional[object] = None

    connector_config: Optional[object] = None

    integration_data: Optional[object] = None

    pre_connect_input: Optional[object] = None

    webhook_input: Optional[object] = None


class ConnectorZohodeskDiscriminatedConnectorConfigConnectorScope(BaseModel):
    scope: str

    description: Optional[str] = None

    display_name: Optional[str] = None


class ConnectorZohodeskDiscriminatedConnectorConfigConnector(BaseModel):
    name: str

    auth_type: Optional[Literal["BASIC", "OAUTH1", "OAUTH2", "OAUTH2CC", "API_KEY", "CUSTOM"]] = FieldInfo(
        alias="authType", default=None
    )

    display_name: Optional[str] = None

    logo_url: Optional[str] = None

    openint_scopes: Optional[List[str]] = None

    platforms: Optional[List[Literal["web", "mobile", "desktop", "local", "cloud"]]] = None

    schemas: Optional[ConnectorZohodeskDiscriminatedConnectorConfigConnectorSchemas] = None

    scopes: Optional[List[ConnectorZohodeskDiscriminatedConnectorConfigConnectorScope]] = None

    stage: Optional[Literal["alpha", "beta", "ga", "hidden"]] = None


class ConnectorZohodeskDiscriminatedConnectorConfigIntegrations(BaseModel):
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


class ConnectorZohodeskDiscriminatedConnectorConfig(BaseModel):
    config: ConnectorZohodeskDiscriminatedConnectorConfigConfig

    connector_name: Literal["zohodesk"]

    id: Optional[str] = None

    connection_count: Optional[float] = None

    connector: Optional[ConnectorZohodeskDiscriminatedConnectorConfigConnector] = None

    created_at: Optional[str] = None

    disabled: Optional[bool] = None

    display_name: Optional[str] = None

    integrations: Optional[Dict[str, ConnectorZohodeskDiscriminatedConnectorConfigIntegrations]] = None

    metadata: Optional[Dict[str, object]] = None
    """
    JSON object can can be used to associate arbitrary metadata to avoid needing a
    separate 1-1 table just for simple key values in your application. During
    updates this object will be shallowly merged
    """

    org_id: Optional[str] = None

    updated_at: Optional[str] = None


ListConnectionConfigsResponse: TypeAlias = Union[
    ConnectorDummyOauth2DiscriminatedConnectorConfig,
    ConnectorSharepointonlineDiscriminatedConnectorConfig,
    ConnectorSlackDiscriminatedConnectorConfig,
    ConnectorGitHubDiscriminatedConnectorConfig,
    ConnectorQuickbooksDiscriminatedConnectorConfig,
    ConnectorGooglemailDiscriminatedConnectorConfig,
    ConnectorNotionDiscriminatedConnectorConfig,
    ConnectorLinkedinDiscriminatedConnectorConfig,
    ConnectorGoogledocsDiscriminatedConnectorConfig,
    ConnectorAircallDiscriminatedConnectorConfig,
    ConnectorGooglecalendarDiscriminatedConnectorConfig,
    ConnectorGooglesheetDiscriminatedConnectorConfig,
    ConnectorDiscordDiscriminatedConnectorConfig,
    ConnectorHubspotDiscriminatedConnectorConfig,
    ConnectorSalesforceDiscriminatedConnectorConfig,
    ConnectorLinearDiscriminatedConnectorConfig,
    ConnectorConfluenceDiscriminatedConnectorConfig,
    ConnectorGoogledriveDiscriminatedConnectorConfig,
    ConnectorAirtableDiscriminatedConnectorConfig,
    ConnectorApolloDiscriminatedConnectorConfig,
    ConnectorBrexDiscriminatedConnectorConfig,
    ConnectorCodaDiscriminatedConnectorConfig,
    ConnectorFacebookDiscriminatedConnectorConfig,
    ConnectorFinchDiscriminatedConnectorConfig,
    ConnectorFirebaseDiscriminatedConnectorConfig,
    ConnectorForeceiptDiscriminatedConnectorConfig,
    ConnectorGongDiscriminatedConnectorConfig,
    ConnectorGreenhouseDiscriminatedConnectorConfig,
    ConnectorHeronDiscriminatedConnectorConfig,
    ConnectorInstagramDiscriminatedConnectorConfig,
    ConnectorIntercomDiscriminatedConnectorConfig,
    ConnectorJiraDiscriminatedConnectorConfig,
    ConnectorKustomerDiscriminatedConnectorConfig,
    ConnectorLeverDiscriminatedConnectorConfig,
    ConnectorLunchmoneyDiscriminatedConnectorConfig,
    ConnectorMercuryDiscriminatedConnectorConfig,
    ConnectorMergeDiscriminatedConnectorConfig,
    ConnectorMicrosoftDiscriminatedConnectorConfig,
    ConnectorMootaDiscriminatedConnectorConfig,
    ConnectorOnebrickDiscriminatedConnectorConfig,
    ConnectorOutreachDiscriminatedConnectorConfig,
    ConnectorPipedriveDiscriminatedConnectorConfig,
    ConnectorPlaidDiscriminatedConnectorConfig,
    ConnectorPostgresDiscriminatedConnectorConfig,
    ConnectorRampDiscriminatedConnectorConfig,
    ConnectorRedditDiscriminatedConnectorConfig,
    ConnectorSalesloftDiscriminatedConnectorConfig,
    ConnectorSaltedgeDiscriminatedConnectorConfig,
    ConnectorSplitwiseDiscriminatedConnectorConfig,
    ConnectorStripeDiscriminatedConnectorConfig,
    ConnectorTellerDiscriminatedConnectorConfig,
    ConnectorTogglDiscriminatedConnectorConfig,
    ConnectorTwentyDiscriminatedConnectorConfig,
    ConnectorTwitterDiscriminatedConnectorConfig,
    ConnectorVenmoDiscriminatedConnectorConfig,
    ConnectorWiseDiscriminatedConnectorConfig,
    ConnectorXeroDiscriminatedConnectorConfig,
    ConnectorYodleeDiscriminatedConnectorConfig,
    ConnectorZohodeskDiscriminatedConnectorConfig,
]
