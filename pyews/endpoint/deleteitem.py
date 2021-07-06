from ..service import Operation
from ..utils.exceptions import UknownValueError


class DeleteItem(Operation):
    """DeleteItem EWS Operation deletes items in the Exchange store.
    """

    DELETE_TYPES = ['HardDelete', 'SoftDelete', 'MoveToDeletedItems']

    def __init__(self, item_id, delete_type='MoveToDeletedItems'):
        """Deletes the provided Item ID from an Exchange store.

        Args:
            item_id (str): The Item ID to delete
            delete_type (str, optional): The delete type when deleting the item. Defaults to 'MoveToDeletedItems'.
        """
        if not isinstance(item_id, list):
            item_id = [item_id]
        self.item_id = item_id
        if delete_type and delete_type not in self.DELETE_TYPES:
            UknownValueError(provided_value=delete_type, known_values=self.DELETE_TYPES)
        self.delete_type = delete_type

    def soap(self):
        item_id_list = []
        for item in self.item_id:
            item_id_list.append(self.T_NAMESPACE.ItemId(Id=item))
        return self.M_NAMESPACE.DeleteItem(
            self.M_NAMESPACE.ItemIds(
                item_id_list
            ),
            **{'DeleteType':self.delete_type}
        )
