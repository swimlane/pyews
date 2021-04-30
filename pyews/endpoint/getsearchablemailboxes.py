from ..service import Operation


class GetSearchableMailboxes(Operation):
    """GetSearchableMailboxes EWS Operation retrieves a
    list of searchable mailboxes the authenticated user has
    access to search.
    """

    RESULTS_KEY = 'SearchableMailbox'

    def __init__(self, search_filter=None, expand_group_memberhip=True):
        """Retrieves all searchable mailboxes the authenticated user has access to search.

        Args:
            search_filter (str, optional): A search filter. Typically used to search specific distribution groups. Defaults to None.
            expand_group_memberhip (bool, optional): Whether or not to expand group memberships. Defaults to True.
        """
        self.search_filter = self.M_NAMESPACE.SearchFilter(search_filter) if search_filter else self.M_NAMESPACE.SearchFilter()
        self.expand_group_membership = self.M_NAMESPACE.ExpandGroundMembership(str(expand_group_memberhip))

    def soap(self):
        return self.M_NAMESPACE.GetSearchableMailboxes(
            self.search_filter,
            self.expand_group_membership
        )
