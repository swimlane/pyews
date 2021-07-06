from ..service import Operation


class ResolveNames(Operation):
    """ResolveNames EWS Operation attempts
    to resolve the authenticated or provided name
    """

    RESULTS_KEY = 'ResolutionSet'

    def __init__(self, user=None):
        """Resolves the authenticated or provided name

        Args:
            user (str, optional): A user to attempt to resolve. Defaults to None.
        """
        self.user = user

    def soap(self):
        if not self.user:
            self.user = self.credentials[0]
        return self.M_NAMESPACE.ResolveNames(
            self.M_NAMESPACE.UnresolvedEntry(self.user),
            **{'ReturnFullContactData':"true"}
        )
