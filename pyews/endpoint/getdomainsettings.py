from ..service.autodiscover import Autodiscover, Authentication


class GetDomainSettings(Autodiscover):
    """GetFederationInformation EWS Autodiscover endpoint
    retrieves the authenticated users federation information
    """

    def __init__(self, domain=None):
        """Retrieves the domain settings for the authenticated or provided domain.

        Args:
            user (str, optional): A user to retrieve user settings for. Defaults to None.
        """
        self.domain = domain

    def soap(self):
        return self.A_NAMESPACE.GetDomainSettingsRequestMessage(
            self.A_NAMESPACE.Request(
                self.A_NAMESPACE.Domains(
                    self.A_NAMESPACE.Domain(Authentication.credentials[0].split('@')[-1])
                ),
                self.A_NAMESPACE.RequestedSettings(
                    self.A_NAMESPACE.Setting('InternalEwsUrl'),
                    self.A_NAMESPACE.Setting('ExternalEwsUrl'),
                   
                )
            )
        )
