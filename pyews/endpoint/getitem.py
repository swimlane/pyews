from ..service import Operation
from ..utils.exceptions import UknownValueError


class GetItem(Operation):
    """GetItem EWS Operation retrieves details about an item.
    """

    RESULTS_KEY = 'Items'
    BASE_SHAPES = [
        'IdOnly',
        'Default',
        'AllProperties'
    ]
    BODY_TYPES = [
        'Best',
        'HTML',
        'Text'
    ]

    def __init__(self, item_id, change_key=None, base_shape='AllProperties', include_mime_content=True, body_type='Best'):
        """Retrieves details about a provided item id

        Args:
            item_id (str): The item id you want to get information about.
            change_key (str, optional): The change key of the item. Defaults to None.
            base_shape (str, optional): The base shape of the returned item. Defaults to 'AllProperties'.
            include_mime_content (bool, optional): Whether or not to include MIME content. Defaults to True.
            body_type (str, optional): The item body type. Defaults to 'Best'.
        """
        self.include_mime_content = include_mime_content
        if base_shape not in self.BASE_SHAPES:
            UknownValueError(provided_value=base_shape, known_values=self.BASE_SHAPES)
        self.base_shape = base_shape
        if body_type not in self.BODY_TYPES:
            UknownValueError(provided_value=body_type, known_values=self.BODY_TYPES)
        self.body_type = body_type
        self.item_id = item_id
        self.change_key = change_key

    def soap(self):
        if self.change_key:
            item_id_string = self.T_NAMESPACE.ItemId(Id=self.item_id, ChangeKey=self.change_key)
        else:
            item_id_string = self.T_NAMESPACE.ItemId(Id=self.item_id)
        return self.M_NAMESPACE.GetItem(
            self.M_NAMESPACE.ItemShape(
                self.T_NAMESPACE.BaseShape(self.base_shape),
                self.T_NAMESPACE.IncludeMimeContent(str(self.include_mime_content).lower()),
                self.T_NAMESPACE.BodyType(self.body_type)
            ),
            self.M_NAMESPACE.ItemIds(
                item_id_string
            )
        )
