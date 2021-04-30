from ..service import Operation
from ..utils.exceptions import UknownValueError


class ConvertId(Operation):
    """ConvertId EWS Operation converts item and folder
    identifiers between formats.
    """

    RESULTS_KEY = '@Id'
    ID_FORMATS = [
        'EntryId',
        'EwsId',
        'EwsLegacyId',
        'HexEntryId',
        'OwaId',
        'StoreId'
    ]

    def __init__(self, user, item_id, id_type, convert_to):
        """Takes a specific user, item_id, id_type, and the 
        desired format to conver to as inputs.

        Args:
            user (str): The mailbox that the ID is associated with
            item_id (str): The item ID 
            id_type (str): The Item ID type
            convert_to (str): The format to conver the Item ID to

        Raises:
            UknownValueError: One or more provided values is unknown
        """
        self.user  = user
        self.item_id = item_id
        if id_type not in self.ID_FORMATS:
            UknownValueError(provided_value=id_type, known_values=self.ID_FORMATS)
        if  convert_to not in self.ID_FORMATS:
            UknownValueError(provided_value=convert_to, known_values=self.ID_FORMATS)
        self.id_type = id_type
        self.convert_to = convert_to

    def soap(self):
        return self.M_NAMESPACE.ConvertId(
            self.M_NAMESPACE.SourceIds(
                self.T_NAMESPACE.AlternateId(
                    Format=self.id_type, Id=self.item_id, Mailbox=self.user
                )
            ),
            DestinationFormat=self.convert_to
        )
