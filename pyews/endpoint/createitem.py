from ..service import Operation
from ..utils.exceptions import UknownValueError
from ..utils.attributes import FOLDER_LIST, MESSAGE_ELEMENTS


class CreateItem(Operation):
    """CreateItem EWS Operation is used to create e-mail messages
    """

    RESULTS_KEY = 'Items'
    MESSAGE_DISPOSITION = [
        'SaveOnly',
        'SendOnly',
        'SendAndSaveCopy'
    ]
    BODY_TYPES = [
        'Best',
        'HTML',
        'Text'
    ]

    __MESSSAGE_ELEMENTS = []

    def __init__(self, type='message', message_disposition='SendAndSaveCopy', save_item_to='sentitems', **kwargs):
        """Creates an e-mail message

        Args:
            type (str, optional): The type of item to create. Defaults to 'message'.
            message_disposition (str, optional): The action to take when the item is created. Defaults to 'SendAndSaveCopy'.
            save_item_to (str, optional): Where to save the created e-mail message. Defaults to 'sentitems'.
        """
        self.__process_kwargs(kwargs)
        self.type = type
        if message_disposition not in self.MESSAGE_DISPOSITION:
            UknownValueError(provided_value=message_disposition, known_values=self.MESSAGE_DISPOSITION)
        self.message_disposition = message_disposition
        if save_item_to not in FOLDER_LIST:
            self.__save_item_to = self.T_NAMESPACE.FolderId(Id=save_item_to)
        else:
            self.__save_item_to = self.T_NAMESPACE.DistinguishedFolderId(Id=save_item_to)

    def __create_message(self):
        return self.T_NAMESPACE.Message(
            *self.__MESSSAGE_ELEMENTS
        )

    def __process_kwargs(self, kwargs):
        for key,val in kwargs.items():
            for item in self._get_recursively(MESSAGE_ELEMENTS, key):
                if isinstance(item, list):
                    if val in item:
                        if key in ['ToRecipients', 'Sender', 'CcRecipients', 'BccRecipients']:
                            self.__MESSSAGE_ELEMENTS.append(self.T_NAMESPACE(key, self.T_NAMESPACE.Mailbox(self.T_NAMESPACE.EmailAddress(val))))
                        else:
                            self.__MESSSAGE_ELEMENTS.append(self.T_NAMESPACE(key, val))
                else:
                    if key in MESSAGE_ELEMENTS:
                        if key in ['ToRecipients', 'Sender', 'CcRecipients', 'BccRecipients']:
                            self.__MESSSAGE_ELEMENTS.append(self.T_NAMESPACE(key, self.T_NAMESPACE.Mailbox(self.T_NAMESPACE.EmailAddress(val))))
                        else:
                            self.__MESSSAGE_ELEMENTS.append(self.T_NAMESPACE(key, val))

    def soap(self):
        item = None
        if self.type == 'message':
            item = self.__create_message()
        return self.M_NAMESPACE.CreateItem(
            self.M_NAMESPACE.SavedItemFolderId(
                self.__save_item_to
            ),
            self.M_NAMESPACE.Items(
                item
            ),
            MessageDisposition=self.message_disposition
        )
