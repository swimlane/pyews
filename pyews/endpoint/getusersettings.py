from ..service.autodiscover import Autodiscover, Authentication


class GetUserSettings(Autodiscover):
    """GetUserSettings EWS Autodiscover endpoint
    retrieves the authenticated or provided users settings
    """

    RESULTS_KEY = 'UserSettings'

    def __init__(self, user=None):
        """Retrieves the user settings for the authenticated or provided user.

        Args:
            user (str, optional): A user to retrieve user settings for. Defaults to None.
        """
        self.user = user

    def soap(self):
        if not self.user:
            self.user = Authentication.credentials[0]
        return self.A_NAMESPACE.GetUserSettingsRequestMessage(
            self.A_NAMESPACE.Request(
                self.A_NAMESPACE.Users(
                    self.A_NAMESPACE.User(
                        self.A_NAMESPACE.Mailbox(self.user)
                    )
                ),
                self.A_NAMESPACE.RequestedSettings(
                    self.A_NAMESPACE.Setting('InternalEwsUrl'),
                    self.A_NAMESPACE.Setting('ExternalEwsUrl'),
                    self.A_NAMESPACE.Setting('UserDisplayName'),
                    self.A_NAMESPACE.Setting('UserDN'),
                    self.A_NAMESPACE.Setting('UserDeploymentId'),
                    self.A_NAMESPACE.Setting('InternalMailboxServer'),
                    self.A_NAMESPACE.Setting('MailboxDN'),
                    self.A_NAMESPACE.Setting('ActiveDirectoryServer'),
                    self.A_NAMESPACE.Setting('EwsSupportedSchemas'),
                    self.A_NAMESPACE.Setting('InternalRpcClientServer'),
                    self.A_NAMESPACE.Setting('InternalEcpUrl'),
                    self.A_NAMESPACE.Setting('InternalEcpVoicemailUrl'),
                    self.A_NAMESPACE.Setting('InternalEcpEmailSubscriptionsUrl'),
                    self.A_NAMESPACE.Setting('InternalEcpTextMessagingUrl'),
                    self.A_NAMESPACE.Setting('InternalEcpDeliveryReportUrl'),
                    self.A_NAMESPACE.Setting('InternalEcpRetentionPolicyTagsUrl'),
                    self.A_NAMESPACE.Setting('InternalEcpPublishingUrl'),
                    self.A_NAMESPACE.Setting('InternalOABUrl'),
                    self.A_NAMESPACE.Setting('InternalUMUrl'),
                    self.A_NAMESPACE.Setting('InternalWebClientUrls'),
                    self.A_NAMESPACE.Setting('PublicFolderServer'),
                    self.A_NAMESPACE.Setting('ExternalMailboxServer'),
                    self.A_NAMESPACE.Setting('ExternalMailboxServerRequiresSSL'),
                    self.A_NAMESPACE.Setting('ExternalMailboxServerAuthenticationMethods'),
                    self.A_NAMESPACE.Setting('EcpVoicemailUrlFragment'),
                    self.A_NAMESPACE.Setting('EcpEmailSubscriptionsUrlFragment'),
                    self.A_NAMESPACE.Setting('EcpTextMessagingUrlFragment'),
                    self.A_NAMESPACE.Setting('EcpDeliveryReportUrlFragment'),
                    self.A_NAMESPACE.Setting('EcpRetentionPolicyTagsUrlFragment'),
                    self.A_NAMESPACE.Setting('ExternalEcpUrl'),
                    self.A_NAMESPACE.Setting('EcpPublishingUrlFragment'),
                    self.A_NAMESPACE.Setting('ExternalEcpVoicemailUrl'),
                    self.A_NAMESPACE.Setting('ExternalEcpEmailSubscriptionsUrl'),
                    self.A_NAMESPACE.Setting('ExternalEcpTextMessagingUrl'),
                    self.A_NAMESPACE.Setting('ExternalEcpDeliveryReportUrl'),
                    self.A_NAMESPACE.Setting('EcpEmailSubscriptionsUrlFragment'),
                    self.A_NAMESPACE.Setting('ExternalEcpRetentionPolicyTagsUrl'),
                    self.A_NAMESPACE.Setting('ExternalEcpPublishingUrl'),
                    self.A_NAMESPACE.Setting('ExternalOABUrl'),
                    self.A_NAMESPACE.Setting('ExternalUMUrl'),
                    self.A_NAMESPACE.Setting('ExternalWebClientUrls'),
                    self.A_NAMESPACE.Setting('CrossOrganizationSharingEnabled'),
                    self.A_NAMESPACE.Setting('AlternateMailboxes'),
                    self.A_NAMESPACE.Setting('CasVersion'),
                    self.A_NAMESPACE.Setting('InternalPop3Connections'),
                    self.A_NAMESPACE.Setting('ExternalPop3Connections'),
                    self.A_NAMESPACE.Setting('InternalImap4Connections'),
                    self.A_NAMESPACE.Setting('ExternalImap4Connections'),
                    self.A_NAMESPACE.Setting('InternalSmtpConnections'),
                    self.A_NAMESPACE.Setting('ExternalSmtpConnections'),
                    self.A_NAMESPACE.Setting('InternalServerExclusiveConnect'),
                    self.A_NAMESPACE.Setting('ExternalServerExclusiveConnect'),
                    self.A_NAMESPACE.Setting('ExchangeRpcUrl'),
                    self.A_NAMESPACE.Setting('ShowGalAsDefaultView'),
                    self.A_NAMESPACE.Setting('AutoDiscoverSMTPAddress'),
                    self.A_NAMESPACE.Setting('InteropExternalEwsUrl'),
                    self.A_NAMESPACE.Setting('ExternalEwsVersion'),
                    self.A_NAMESPACE.Setting('InteropExternalEwsVersion'),
                    self.A_NAMESPACE.Setting('MobileMailboxPolicyInterop'),
                    self.A_NAMESPACE.Setting('GroupingInformation'),
                    self.A_NAMESPACE.Setting('UserMSOnline'),
                    self.A_NAMESPACE.Setting('MapiHttpEnabled')
                )
            ),
        )
