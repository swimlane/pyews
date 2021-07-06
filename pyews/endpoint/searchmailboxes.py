from ..service import Operation
from ..utils.exceptions import UknownValueError


class SearchMailboxes(Operation):
    """SearchMailboxes EWS Operation will search using a query on one or more provided
    reference id's
    """

    RESULTS_KEY = 'SearchPreviewItem'
    SEARCH_SCOPES = ['All', 'PrimaryOnly', 'ArchiveOnly']

    def __init__(self, query, reference_id, search_scope='All'):
        """Searches one or more reference id's using the provided query and search_scope.

        Args:
            query (str): The Advanced Query Syntax (AQS) to search with.
            reference_id (list): One or more mailbox reference Id's
            search_scope (str, optional): The search scope. Defaults to 'All'.

        Raises:
            UknownValueError: The provided search scope is unknown.
        """
        self.query = query
        if not isinstance(reference_id, list):
            reference_id = [reference_id]
        self.reference_id = reference_id
        if search_scope not in self.SEARCH_SCOPES:
            raise UknownValueError('The search_scope ({}) you provided is not one of {}'.format(search_scope, ','.join([x for x in self.SEARCH_SCOPES])))
        if search_scope in self.SEARCH_SCOPES:
            self.scope = search_scope

    def soap(self):
        return self.M_NAMESPACE.SearchMailboxes(
            self.M_NAMESPACE.SearchQueries(
                self.T_NAMESPACE.MailboxQuery(
                    self.T_NAMESPACE.Query(self.query),
                    self.T_NAMESPACE.MailboxSearchScopes(*self.__get_search_scope())
                )
            ),
            self.M_NAMESPACE.ResultType('PreviewOnly')
        )

    def __get_search_scope(self):
        mailbox_soap_element = []
        for item in self.reference_id:
            mailbox_soap_element.append(
                self.T_NAMESPACE.MailboxSearchScope(
                    self.T_NAMESPACE.Mailbox(item),
                    self.T_NAMESPACE.SearchScope(self.scope)
                )
            )
        return mailbox_soap_element
