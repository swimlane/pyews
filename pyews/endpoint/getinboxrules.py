from ..service import Operation


class GetInboxRules(Operation):
    """GetInboxRules EWS Operation retrieves inbox rules.
    """

    RESULTS_KEY = 'GetInboxRulesResponse'

    def __init__(self, user=None):
        """Retrieves inbox rules for the authenticated or specified user.

        Args:
            user (str, optional): The user to retrieve inbox rules for. Defaults to authenticated user.
        """
        self.__user = user

    def soap(self):
        if not self.__user:
            self.__user = self.credentials[0]
        return self.M_NAMESPACE.GetInboxRules(
            self.M_NAMESPACE.MailboxSmtpAddress(self.__user)
        )
