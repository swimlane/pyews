from ..service.autodiscover import Autodiscover


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
            self.user = self.credentials[0]
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
                    self.A_NAMESPACE.Setting('MailboxDN'),
                    self.A_NAMESPACE.Setting('EwsSupportedSchemas'),
                )
            ),
        )
