from ..service import Operation


class ExpandDL(Operation):
    """ExpandDL EWS Operation expands the provided distribution list.
    """

    RESULTS_KEY = 'Items'

    def __init__(self, user):
        """Expands the provided distribution list

        Args:
            user (str): The distribution list to expand
        """
        self.user = user

    def soap(self):
        return self.M_NAMESPACE.ExpandDL(
            self.M_NAMESPACE.Mailbox(
                self.T_NAMESPACE.EmailAddress(self.user)
            )
        )
