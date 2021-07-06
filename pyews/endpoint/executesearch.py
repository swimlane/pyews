import uuid
from ..service import Operation


class ExecuteSearch(Operation):
    """ExecuteSearch EWS Operation executes a search as an Outlook client.
    """

    RESULTS_KEY = 'Items'

    def __init__(self, query, result_row_count='25', max_results_count='-1'):
        """Executes a search as an Outlook client for the authenticated user.

        Args:
            query (str): The query to search for.
            result_row_count (str, optional): The row count of results. Defaults to '25'.
            max_results_count (str, optional): The max results count. -1 equals unlimited. Defaults to '-1'.
        """
        self.query = query
        self.result_row_count = result_row_count
        self.max_results_count = max_results_count

    def soap(self):
        self.session_id = '{id}'.format(id=str(uuid.uuid4()).upper())
        return self.M_NAMESPACE.ExecuteSearch(
            self.M_NAMESPACE.ApplicationId('Outlook'),
            self.M_NAMESPACE.Scenario('MailSearch'),
            self.M_NAMESPACE.SearchSessionId(self.session_id),
            self.M_NAMESPACE.SearchScope(
                self.T_NAMESPACE.PrimaryMailboxSearchScope(
                    self.T_NAMESPACE.IsDeepTraversal('true')
                )
            ),
            self.M_NAMESPACE.Query(self.query),
            self.M_NAMESPACE.ResultRowCount(self.result_row_count),
            self.M_NAMESPACE.MaxResultsCountHint(self.max_results_count),
            self.M_NAMESPACE.ItemTypes('MailItems')
        )
