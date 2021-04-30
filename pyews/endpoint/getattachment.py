from ..service import Operation


class GetAttachment(Operation):
    """GetAttachment EWS Operation retrieves the provided attachment ID.
    """

    RESULTS_KEY = 'Attachments'

    def __init__(self, attachment_id):
        """Retrieves the provided attachment_id

        Args:
            attachment_id (str): The attachment_id to retrieve.
        """
        self.attachment_id = attachment_id

    def soap(self):
        return self.M_NAMESPACE.GetAttachment(
            self.M_NAMESPACE.AttachmentShape(
                self.T_NAMESPACE.IncludeMimeContent('true'),
                self.T_NAMESPACE.BodyType('Best')
            ),
            self.M_NAMESPACE.AttachmentIds(
                self.T_NAMESPACE.AttachmentId(Id=self.attachment_id)
            )
        )
